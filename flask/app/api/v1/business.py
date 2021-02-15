import os
from datetime import timedelta, datetime

import africastalking
import requests

from flask import current_app
from app.database import db
from app.database.models import SMSMessage, SMSLog, SMSBroadcast, SMSBroadcastMessage, SMSBroadcastSubscription


# SMS ###################################################################
def create_sms(data):
    # response list
    response = []

    # NOTE::phone number is a list
    phone_numbers_list = data.get('phone_numbers')

    # create sms messages per phone number in the phone_numbers_list
    for phone_number in phone_numbers_list:
        sms_message = SMSMessage(
            provider_id=data.get('provider_id'),
            broadcast_message_id=data.get('broadcast_message_id'),
            phone=phone_number,
            send_at=data.get('send_at'),
            sent=data.get('sent'),
            message=data.get('message')
        )

        try:
            db.session.add(sms_message)
            db.session.flush()

            # create initial sms status of Queued
            sms_log_entry = SMSLog(
                sms_id=sms_message.id,
                at_status_code='Queued'
            )

            db.session.add(sms_log_entry)
            db.session.commit()
            db.session.refresh(sms_message)

            response.append(sms_message)
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e, exc_info=True)

    return response


# AFRICASTALKING STATUS #######################################################
def create_africastalking_status(data):
    sms_id = data.get('id')

    sms = SMSMessage.query.filter_by(africastalking_sms_id=sms_id).one()

    sms_log = SMSLog(
        sms_id=sms.id,
        status=data.get('status'),
        network_code=data.get('network_code'),
        failure_reason=data.get('failure_reason')
    )

    db.session.add(sms_log)
    db.session.commit()
    return sms_log


# AT BALANCE ############################################################
def get_at_account_balance():
    username = os.getenv("AT_USERNAME")
    api_key = os.getenv("AT_API_KEY")

    balance = 0

    africastalking.initialize(username, api_key)

    try:
        # Fetch the application data
        application = africastalking.Application
        user_data = application.fetch_application_data()

        balance_string = user_data['UserData']['balance']

        if balance_string:
            # split, balance format is KES XX
            balance_list = balance_string.split(' ')

            balance = float(balance_list[1])
    except Exception as e:
        current_app.logger.error(e, exc_info=True)
        balance = 0

    return balance


# SEND MAIL ALERT #######################################################
def send_balance_mail_alert():
    account_balance = get_at_account_balance()
    balance_alert_level = os.getenv('BALANCE_ALERT_LEVEL')
    balance_alert_email = os.getenv('BALANCE_ALERT_EMAIL')

    # TODO: Uncomment this when in production to allow for email alerts
    # balance below alert level
    # if account_balance < float(balance_alert_level):
    #     mail_server = os.getenv('MAIL_SERVER')
    #     mail_port = os.getenv('MAIL_PORT')
    #     mail_use_ssl = os.getenv('MAIL_USE_SSL')
    #     mail_username = os.getenv('MAIL_USERNAME')
    #     mail_password = os.getenv('MAIL_PASSWORD')
    #
    #     # update current app configuration with mail options
    #     current_app.config.update(
    #         DEBUG=os.getenv('DEBUG'),
    #         MAIL_SERVER=mail_server,
    #         MAIL_PORT=mail_port,
    #         MAIL_USE_SSL=mail_use_ssl,
    #         MAIL_USERNAME=mail_username,
    #         MAIL_PASSWORD=mail_password
    #     )
    #
    #     mail = Mail(current_app)
    #
    #     msg = Message(
    #         "AT Account Balance Alert",
    #         sender=mail_username,
    #         recipients=[balance_alert_email]
    #     )
    #     msg.body = "Current Balance KES {:0,.0f} is below alert level of KES {:0,.0f}. Please top up.".format(
    #         account_balance,
    #         float(balance_alert_level)
    #     )
    #
    #     mail.send(msg)

    return {
        'alert_level': 'KES {:0,.0f}'.format(float(balance_alert_level)),
        'current_balance': 'KES {:0,.0f}'.format(account_balance)
    }


# BROADCAST ###################################################################
def create_broadcast(data):
    broadcast = SMSBroadcast(
        provider_id = data.get('provider_id'),
        name = data.get('name'),
        description = data.get('description'),
        is_published = data.get('is_published')
    )

    db.session.add(broadcast)
    db.session.commit()
    return broadcast


def update_broadcast(id, data):
    provider_id = data.get('provider_id')
    name = data.get('name')
    description = data.get('description')
    is_published = data.get('is_published')

    broadcast = SMSBroadcast.query.filter(SMSBroadcast.id == id).one()

    if provider_id: broadcast.provider_id = provider_id
    if name: broadcast.name = name
    if description: broadcast.description = description
    if is_published: broadcast.is_published = is_published

    db.session.add(broadcast)
    db.session.commit()
    return broadcast


def delete_broadcast(id):
    broadcast = SMSBroadcast.query.filter(SMSBroadcast.id == id).one()
    db.session.delete(broadcast)
    db.session.commit()


# BROADCAST MESSAGES ###################################################################
def create_broadcast_message(data):
    broadcast_message = SMSBroadcastMessage(
        broadcast_id = data.get('broadcast_id'),
        subject = data.get('subject'),
        message = data.get('message'),
        send_on_day_relative = data.get('send_on_day_relative'),
        send_on_day_absolute = data.get('send_on_day_absolute')
    )

    db.session.add(broadcast_message)
    db.session.commit()
    return broadcast_message


def update_broadcast_message(id, data):
    broadcast_id = data.get('broadcast_id')
    subject = data.get('subject')
    message = data.get('message')
    send_on_day_relative = data.get('send_on_day_relative')
    send_on_day_absolute = data.get('send_on_day_absolute')

    broadcast_message = SMSBroadcastMessage.query.filter(SMSBroadcastMessage.id == id).one()

    if broadcast_id: broadcast_message.farmer_id = broadcast_id
    if subject: broadcast_message.subject = subject
    if message: broadcast_message.message = message
    if send_on_day_relative: broadcast_message.send_on_day_relative = send_on_day_relative
    if send_on_day_absolute: broadcast_message.send_on_day_absolute = send_on_day_absolute

    db.session.add(broadcast_message)
    db.session.commit()
    return broadcast_message


def delete_broadcast_message(id):
    broadcast_message = SMSBroadcastMessage.query.filter(SMSBroadcastMessage.id == id).one()
    db.session.delete(broadcast_message)
    db.session.commit()


# BROADCAST SUBSCRIPTION ###################################################################
def create_broadcast_subscription(data):
    broadcast_subscription = SMSBroadcastSubscription(
        broadcast_id = data.get('broadcast_id'),
        farmer_id = data.get('farmer_id'),
        day_zero = data.get('day_zero')
    )

    # schedule message
    # get broadcast and schedule job
    broadcast = SMSBroadcast.query.filter_by(id=data.get('broadcast_id')).first()
    if broadcast:
        if broadcast.send_on_day_absolute:
            # add job
            job_id = f'broadcast_{broadcast.id}'
            absolute_day_time = broadcast.send_on_day_absolute.strftime('%Y-%m-%dT%H:%M')
            job_time = datetime.strptime(str(absolute_day_time), '%Y-%m-%dT%H:%M')

            # add job to scheduler
        elif broadcast.send_on_day_relative:
            broadcast_relative_date = (data.get('day_zero') + timedelta(days=broadcast.send_on_day_relative)).strftime('%Y-%m-%dT%H:%M')
            job_time = datetime.strptime(str(broadcast_relative_date), '%Y-%m-%dT%H:%M')
            job_id = f'broadcast_{broadcast.id}'

            # add job to scheduler

    db.session.add(broadcast_subscription)
    db.session.commit()
    return broadcast_subscription


def update_broadcast_subscription(id, data):
    broadcast_id = data.get('broadcast_id')
    farmer_id = data.get('farmer_id')
    day_zero = data.get('day_zero')

    broadcast_subscription = SMSBroadcastSubscription.query.filter(SMSBroadcastSubscription.id == id).one()

    if broadcast_id: broadcast_subscription.broadcast_id = broadcast_id
    if farmer_id: broadcast_subscription.farmer_id = farmer_id
    if day_zero: broadcast_subscription.day_zero = day_zero

    db.session.add(broadcast_subscription)
    db.session.commit()
    return broadcast_subscription


def delete_broadcast_subscription(id):
    broadcast_subscription = SMSBroadcastSubscription.query.filter(SMSBroadcastSubscription.id == id).one()
    db.session.delete(broadcast_subscription)
    db.session.commit()


# scheduling/broadcast features
def get_farmer_phone_number(farmer_id):
    registry_url = os.getenv('REGISTRY_URL')
    farmer_detail_url = f'{registry_url}/farmers/{farmer_id}'

    r = requests.get(farmer_detail_url)
    data = r.json()

    if r.status_code != 200:
        return 0

    return data['phone']


# auto assign farmer
