import logging

from flask import request
from flask_restx import Resource

from app.api.restx import api
from app.api.v1.parsers import pagination_arguments
from app.api.v1.serializers import page_of_broadcasts, sms_broadcast
from app.api.v1.business import create_broadcast, update_broadcast, delete_broadcast
from app.database.models import SMSBroadcast

log = logging.getLogger(__name__)
ns = api.namespace('broadcast')


@ns.route('')
class BroadcastCollection(Resource):
    @api.expect(pagination_arguments)
    @api.marshal_list_with(page_of_broadcasts)
    def get(self):
        pagination_args = pagination_arguments.parse_args(request)
        page = pagination_args.get('page', 1)
        per_page = pagination_args.get('per_page', 10)
        broadcasts_query = SMSBroadcast.query

        return broadcasts_query.paginate(page, per_page, error_out=False)

    @api.expect(sms_broadcast)
    @api.marshal_with(sms_broadcast)
    @api.response(201, 'Broadcast successfully created.')
    def post(self):
        data = request.json
        sms = create_broadcast(data)
        return sms, 201


@ns.route('/<int:id>')
@api.response(404, 'Broadcast not found.')
class BroadcastItemCollection(Resource):

    @api.marshal_with(sms_broadcast)
    def get(self, id):
        return SMSBroadcast.query.filter(SMSBroadcast.id == id).one()

    @api.expect(sms_broadcast)
    @api.marshal_with(sms_broadcast)
    @api.response(204, 'Broadcast successfully updated.')
    @api.response(404, 'Broadcast not found.')
    def put(self, id):
        data = request.json
        broadcast = update_broadcast(id, data)
        return broadcast, 204

    @api.response(204, 'Broadcast successfully deleted.')
    @api.response(404, 'Broadcast not found.')
    def delete(self, id):
        delete_broadcast(id)
        return None, 204