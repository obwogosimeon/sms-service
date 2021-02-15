import logging

from flask import request
from flask_restx import Resource

from app.api.restx import api
from app.api.v1.parsers import pagination_arguments
from app.api.v1.serializers import page_of_broadcast_messages, broadcast_message
from app.api.v1.business import create_broadcast_message, update_broadcast_message, delete_broadcast_message
from app.database.models import SMSBroadcastMessage

log = logging.getLogger(__name__)
ns = api.namespace('broadcast/message')


@ns.route('')
class BroadcastMessageCollection(Resource):
    @api.expect(pagination_arguments)
    @api.marshal_list_with(page_of_broadcast_messages)
    def get(self):
        pagination_args = pagination_arguments.parse_args(request)
        page = pagination_args.get('page', 1)
        per_page = pagination_args.get('per_page', 10)
        broadcast_message_query = SMSBroadcastMessage.query

        return broadcast_message_query.paginate(page, per_page, error_out=False)

    @api.expect(broadcast_message)
    @api.marshal_with(broadcast_message)
    @api.response(201, 'Broadcast Message successfully created.')
    def post(self):
        data = request.json
        sms = create_broadcast_message(data)
        return sms, 201


@ns.route('/<int:id>')
@api.response(404, 'Broadcast Message not found.')
class BroadcastMessageItemCollection(Resource):

    @api.marshal_with(broadcast_message)
    def get(self, id):
        return SMSBroadcastMessage.query.filter(SMSBroadcastMessage.id == id).one()

    @api.expect(broadcast_message)
    @api.marshal_with(broadcast_message)
    @api.response(204, 'Broadcast Message successfully updated.')
    @api.response(404, 'Broadcast Message not found.')
    def put(self, id):
        data = request.json
        broadcast_message = update_broadcast_message(id, data)
        return broadcast_message, 204

    @api.response(204, 'Broadcast Message successfully deleted.')
    @api.response(404, 'Broadcast Message not found.')
    def delete(self, id):
        delete_broadcast_message(id)
        return None, 204