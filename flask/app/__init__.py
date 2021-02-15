import os
from datetime import datetime

import africastalking

from app import settings
from app.api.restx import api
from app.api.v1.business import get_at_account_balance
from app.api.v1.endpoints.at_balance import ns as balance_namespace
from app.api.v1.endpoints.at_sms_log import ns as at_sms_log_namespace
from app.api.v1.endpoints.broadcast_message import ns as broadcast_message_namespace
from app.api.v1.endpoints.broadcast_subscription import ns as broadcast_subscription_namespace
from app.api.v1.endpoints.broadcasts import ns as broadcasts_namespace
from app.api.v1.endpoints.sms import ns as sms_namespace
from app.database import db
from app.database.models import SMSMessage, SMSLog
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask import Blueprint, Flask, current_app
from flask_apscheduler import APScheduler as _BaseAPScheduler


class APScheduler(_BaseAPScheduler):
    def run_job(self, id, jobstore=None):
        with self.app.app_context():
            super().run_job(id=id, jobstore=jobstore)


application = Flask(__name__)


def run_queued_messages():
    with application.app_context():
        sms_messages = SMSMessage.query.filter(
            SMSMessage.last_status == 'Queued', # TODO: Fix this, its actually not filtering on the model
            SMSMessage.send_at <= datetime.now(),
            SMSMessage.sent == False
        ).all()

        for sms_message in sms_messages:
            id = sms_message.id
            phone_number = sms_message.phone
            message = sms_message.message

            username = os.getenv("AT_USERNAME")
            api_key = os.getenv("AT_API_KEY")
            short_code = os.getenv("AT_SENDER_SHORT_CODE")

            # account balance
            # if balance is low
            # create sms and log as queued
            # else send sms
            #account_balance = get_at_account_balance()
            #print('account balance: ', account_balance)

            # TODO::Uncomment this on production, its only here because we are using sandbox which does not have a balance
            #if account_balance <= 0:
            #    return

            try:
                africastalking.initialize(username, api_key)
                sms = africastalking.SMS

                response = sms.send(message, [phone_number], short_code)

                # process response
                recipients = response['SMSMessageData']['Recipients']

                sms_entry = SMSMessage.query.filter_by(id=id).first()
                sms_entry.at_sms_id = recipients[0]['messageId']
                sms_entry.at_sms_cost = recipients[0]['cost']
                status_code = recipients[0]['statusCode']

                # status code 101 means sent
                if status_code == 101:
                    sms_message.sent = True

                db.session.flush()

                sms_log_entry = SMSLog(
                    sms_id=sms_entry.id,
                    at_status_code=recipients[0]['status']
                )

                db.session.add(sms_log_entry)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(e, exc_info=True)


def configure_app(flask_app):
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_DATABASE = os.getenv("DB_DATABASE")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    flask_app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['RESTX_SWAGGER_UI_DOC_EXPANSION'] = settings.RESTX_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTX_VALIDATE'] = settings.RESTX_VALIDATE
    flask_app.config['RESTX_MASK_SWAGGER'] = settings.RESTX_MASK_SWAGGER
    flask_app.config['RESTX_ERROR_404_HELP'] = settings.RESTX_ERROR_404_HELP
    flask_app.config['SCHEDULER_JOBSTORES'] = {
        'default': SQLAlchemyJobStore(
            url=flask_app.config['SQLALCHEMY_DATABASE_URI'],
            tableschema=os.getenv('SCHEMA_NAME')
        ),
    }
    # do not allow for api access job management
    flask_app.config['SCHEDULER_API_ENABLED'] = False
    flask_app.config['JOBS'] = [
        {
            'id': 'c2322554-7c8a-4540-99e9-2ded1ac4f75f',
            'func': run_queued_messages,
            'trigger': 'interval',
            'seconds': 10,
            'replace_existing': True
        }
    ]
    flask_app.config['SCHEDULER_EXECUTORS'] = {
        'default': {
            'type': 'threadpool', 
            'max_workers': 2
        }
    }
    flask_app.config['SCHEDULER_JOB_DEFAULTS'] = {
        'coalesce': False,
        'max_instances': 1
    }


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
    api.init_app(blueprint)
    api.add_namespace(sms_namespace)
    api.add_namespace(at_sms_log_namespace)
    api.add_namespace(balance_namespace)
    api.add_namespace(broadcasts_namespace)
    api.add_namespace(broadcast_message_namespace)
    api.add_namespace(broadcast_subscription_namespace)

    flask_app.register_blueprint(blueprint)

    db.init_app(flask_app)


initialize_app(application)
db.application = application

scheduler = APScheduler()
scheduler.init_app(application)
scheduler.start()
