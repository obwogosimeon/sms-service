import logging

from flask import request
from flask_restx import Resource

from app.api.restx import api
from app.api.v1.parsers import pagination_arguments
from app.api.v1.serializers import page_of_broadcast_subscriptions, broadcast_subscription
from app.api.v1.business import create_broadcast_subscription, update_broadcast_subscription, delete_broadcast_subscription
from app.database.models import SMSBroadcastSubscription

log = logging.getLogger(__name__)
ns = api.namespace('broadcast/subscription')


@ns.route('')
class BroadcastSubscriptionCollection(Resource):
    @api.expect(pagination_arguments)
    @api.marshal_list_with(page_of_broadcast_subscriptions)
    def get(self):
        pagination_args = pagination_arguments.parse_args(request)
        page = pagination_args.get('page', 1)
        per_page = pagination_args.get('per_page', 10)
        broadcast_subscriptions_query = SMSBroadcastSubscription.query

        return broadcast_subscriptions_query.paginate(page, per_page, error_out=False)

    @api.expect(broadcast_subscription)
    @api.marshal_with(broadcast_subscription)
    @api.response(201, 'Broadcast subscription successfully created.')
    def post(self):
        data = request.json
        sms = create_broadcast_subscription(data)
        return sms, 201


@ns.route('/<int:id>')
@api.response(404, 'Broadcast subscription not found.')
class BroadcastSubscriptionItemCollection(Resource):

    @api.marshal_with(broadcast_subscription)
    def get(self, id):
        return SMSBroadcastSubscription.query.filter(SMSBroadcastSubscription.id == id).one()

    @api.expect(broadcast_subscription)
    @api.marshal_with(broadcast_subscription)
    @api.response(204, 'Broadcast subscription successfully updated.')
    @api.response(404, 'Broadcast subscription not found.')
    def put(self, id):
        data = request.json
        broadcast = update_broadcast_subscription(id, data)
        return broadcast, 204

    @api.response(204, 'Broadcast subscription successfully deleted.')
    @api.response(404, 'Broadcast subscription not found.')
    def delete(self, id):
        delete_broadcast_subscription(id)
        return None, 204