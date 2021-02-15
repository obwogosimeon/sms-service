from flask_restx import Resource

from app.api.restx import api
from app.api.v1.serializers import africastalking_balance
from app.api.v1.business import send_balance_mail_alert


ns = api.namespace('africastalking/balance')


@ns.route('')
class AfricasTalkingBalanceCollection(Resource):

    @api.marshal_with(africastalking_balance)
    def get(self):
        return send_balance_mail_alert()