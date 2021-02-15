import logging

from flask import request
from flask_restx import Resource

from app.api.restx import api
from app.api.v1.business import create_africastalking_status
from app.api.v1.serializers import africastalking_sms_log

log = logging.getLogger(__name__)
ns = api.namespace('africastalking/status', description='Used by Africa\'s Talking as callback URL to push status updates')


@ns.route('')
class AfricasTalkingStatusCollection(Resource):
    @api.expect(africastalking_sms_log)
    @api.marshal_with(africastalking_sms_log)
    @api.response(201, 'Service successfully created.')
    def post(self):
        data = request.json
        status = create_africastalking_status(data)
        return status, 201
