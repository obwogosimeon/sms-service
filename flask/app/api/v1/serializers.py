from flask_restx import fields
from app.api.restx import api


pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})

sms = api.model('SMS', {
    'id': fields.String,
    'phone': fields.String,
    'message': fields.String,
    'last_status': fields.String(attribute="last_status"),
    'status_date': fields.String(attribute="status_date"),
    'send_at': fields.DateTime,
    'provider_id': fields.String
})

sms_post = api.model('SMSPost', {
    'phone_numbers': fields.List(fields.String),
    'message': fields.String(required=True),
    'send_at': fields.DateTime(required=True),
    'provider_id': fields.String(required=True)
})

page_of_sms = api.inherit('Page of SMS', pagination, {
    'items': fields.List(fields.Nested(sms))
})

sms_status = api.model('SMS Status', {
    'id': fields.String(readonly=True),
    'status': fields.String(readonly=True, attribute="last_status")
})

africastalking_sms_log = api.model('SMS Log', {
    'id': fields.String(required=True),
    'status': fields.String(required=True),
    'phoneNumber': fields.String(required=True),
    'networkCode': fields.String(required=True),
    'failureReason': fields.String(required=True)
})

africastalking_balance = api.model('AT Account Balance', {
    'alert_level': fields.String(readonly=True),
    'current_balance': fields.String(readonly=True)
})

sms_broadcast = api.model('Broadcast', {
    'id': fields.String(readonly=True),
    'provider_id': fields.String(required=True),
    'name': fields.String(required=True),
    'description': fields.String(required=True),
    'is_published': fields.Boolean(required=True)
})

page_of_broadcasts = api.inherit('Page of Broadcasts', pagination, {
    'items': fields.List(fields.Nested(sms_broadcast))
})

broadcast_message = api.model('Broadcast Message', {
    'id': fields.String(readonly=True),
    'broadcast_id': fields.String(required=True),
    'subject': fields.String(required=True),
    'message': fields.String(required=True),
    'send_on_day_relative': fields.Integer(required=False),
    'send_on_day_absolute': fields.DateTime(required=False)
})

page_of_broadcast_messages = api.inherit('Page of Day Zeros', pagination, {
    'items': fields.List(fields.Nested(broadcast_message))
})

broadcast_subscription = api.model('Broadcast Subscription', {
    'id': fields.String(readonly=True),
    'broadcast_id': fields.String(required=True),
    'farmer_id': fields.String(required=True),
    'day_zero': fields.DateTime(required=False)
})

page_of_broadcast_subscriptions = api.inherit('Page of Broadcast Subscriptions', pagination, {
    'items': fields.List(fields.Nested(broadcast_subscription))
})