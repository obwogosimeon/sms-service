import logging
import os
import traceback

from distutils.util import strtobool
from dotenv import load_dotenv
from flask_restx import Api
from sqlalchemy.orm.exc import NoResultFound

from app.api.version import api_version

log = logging.getLogger(__name__)
load_dotenv()


api = Api(
    version=api_version, 
    title='SMS Service REST API',
    description='A REST API to our SMS Service.'
)


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not bool(strtobool(os.getenv('DEBUG'))):
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404
