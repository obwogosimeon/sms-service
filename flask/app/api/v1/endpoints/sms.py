import logging

from flask import request
from flask_restx import Resource

from app.api.restx import api
from app.api.v1.parsers import pagination_arguments, sms_arguments
from app.api.v1.serializers import page_of_sms, sms, sms_status, sms_post
from app.api.v1.business import create_sms
from app.database.models import SMSMessage

log = logging.getLogger(__name__)
ns = api.namespace('sms')


@ns.route('')
class SMSCollection(Resource):
    @api.expect(pagination_arguments, sms_arguments)
    @api.marshal_list_with(page_of_sms)
    def get(self):
        pagination_args = pagination_arguments.parse_args(request)
        page = pagination_args.get('page', 1)
        per_page = pagination_args.get('per_page', 10)
        sms_args = sms_arguments.parse_args(request)
        phone = sms_args.get('phone')
        sms_query = SMSMessage.query

        if phone:
            sms_query = sms_query.filter(SMSMessage._phone.contains(phone))

        return sms_query.paginate(page, per_page, error_out=False)

    @api.expect(sms_post)
    @api.marshal_with(sms)
    @api.response(201, 'Service successfully created.')
    def post(self):
        data = request.json
        sms = create_sms(data)
        return sms, 201


@ns.route('/<int:id>')
@api.response(404, 'SMS not found.')
class SMSItemCollection(Resource):

    @api.marshal_with(sms_status)
    def get(self, id):
        return SMSMessage.query.filter(SMSMessage.id == id).one()