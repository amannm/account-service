from flask_restful import Resource, reqparse, abort
from common.error import EmailAlreadyRegistered
from core.account import Account


class AccountResource(Resource):

    def get(self):
        return {'test': 'hello world'}

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help='email of account owner')
        parser.add_argument('password', type=str, required=True, help='desired password for account access')
        args = parser.parse_args()

        try:
            Account.create(email_address=args['email'],
                           password=args['password'])
            return {
                       'email': args['email']
                   }, 201
        except EmailAlreadyRegistered as e:
            abort(409, message=e.message)
