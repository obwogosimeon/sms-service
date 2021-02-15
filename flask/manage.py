import logging
import os

from logging.handlers import RotatingFileHandler

from app.database import db
from app.seeds.broadcast_message_seeder import seed as seed_broadcast_message
from app.seeds.broadcast_seeder import seed as seed_broadcast
from app.seeds.clean_up import clean as database_cleanup
from app.seeds.sms_log_seeder import seed as seed_sms_log
from app.seeds.broadcast_subscriptions_seeder import seed as seed_broadcast_subscription

# seeding scripts
from app.seeds.sms_seeder import seed as seed_sms
from dotenv import load_dotenv
from distutils.util import strtobool
from flask_migrate import Migrate, MigrateCommand
from flask_script import Server, Manager
from flask_seeder import FlaskSeeder

from app import application

load_dotenv()


db_manager = Manager(usage='database commands')
migrate = Migrate(application, db, directory=os.getenv('MIGRATION_DIR'))

seeder = FlaskSeeder()
seeder.init_app(application, db)

manager = Manager(application)
manager.add_command("runserver", Server(port=5000))
manager.add_command("database", db_manager)
manager.add_command('db', MigrateCommand)


@manager.command
def seed_database():
    # database cleanup
    database_cleanup()

    # database seeding
    print("starting database seeding")
    seed_sms()
    seed_broadcast()
    seed_broadcast_message()
    seed_broadcast_subscription()
    seed_sms_log()
    print("done seeding database")


if __name__ == "__main__":
    file_handler = RotatingFileHandler('./error.log', maxBytes=1024 * 1024 * 100, backupCount=20)

    if bool(strtobool(os.getenv('DEBUG'))):
        application.logger.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.DEBUG)
    else:
       application.logger.setLevel(logging.WARN) 
       file_handler.setLevel(logging.WARN)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    application.logger.addHandler(file_handler)

    manager.run()
