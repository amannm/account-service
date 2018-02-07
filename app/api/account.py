from flask_restful import Resource, reqparse, abort
from common.error import EmailAlreadyRegistered, InvalidAccessToken, InvalidVerificationToken, InvalidAccountPassword, \
    AccountEmailNotFound
from core.account import Account


class RegistrationResource(Resource):

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('email_address', type=str, required=True, help='email address of account owner')
        parser.add_argument('password', type=str, required=True, help='desired password for account access')
        args = parser.parse_args()

        try:
            Account.create(email_address=args['email_address'],
                           password=args['password'])
            return {
                       'email_address': args['email_address']
                   }, 201
        except EmailAlreadyRegistered as e:
            abort(409, message=e.message)


class AccessTokenResource(Resource):

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('email_address', type=str, required=True, help='email address of account owner')
        parser.add_argument('password', type=str, required=True, help='password for account access')
        args = parser.parse_args()

        try:
            Account.generate_access_token(email_address=args['email_address'],
                                          password=args['password'])
            return {
                       'email_address': args['email_address']
                   }, 201
        # TODO: don't reveal which of the two is wrong
        except AccountEmailNotFound as e:
            abort(400, message=e.message)
        except InvalidAccountPassword as e:
            abort(400, message=e.message)


class VerificationResource(Resource):

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('access_token', type=str, required=True, help='access token for authenticated caller')
        parser.add_argument('email_address', type=str, required=True, help='email address requiring validation')
        args = parser.parse_args()

        try:
            Account.start_email_verification(access_token=args['access_token'],
                                             email_address=args['email_address'])
            return {
                       'email_address': args['email_address']
                   }, 201
        except EmailAlreadyRegistered as e:
            abort(409, message=e.message)
        except InvalidAccessToken as e:
            abort(401, message=e.message)

    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('verification_token', type=str, required=True, help='verification token provided in email')
        args = parser.parse_args()

        verification_token = args['verification_token']

        try:
            Account.complete_email_verification(verification_token)
            return {
                       'email_address': args['email_address']
                   }, 200
        except InvalidVerificationToken as e:
            abort(400, message=e.message)
