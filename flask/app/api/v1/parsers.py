from flask_restx import reqparse

pagination_arguments = reqparse.RequestParser()
pagination_arguments.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination_arguments.add_argument('per_page', type=int, required=False, choices=[10, 50, 100],
                                  default=10, help='Results per page')

sms_arguments = reqparse.RequestParser()
sms_arguments.add_argument('phone', type=str, required=False, help='Filter by phone number')

sms_status_argument = reqparse.RequestParser()
sms_status_argument.add_argument('id', type=int, required=False, help='Filter by id')