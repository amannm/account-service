
import uuid

from common.error import InvalidAccountPassword
from data.account import AccountData
from data.verification import VerificationData
from gateway.email import EmailGateway
from common.security import Security


class Account:

    @staticmethod
    def create(email_address, password):

        # TODO: validate inputs

        # persist a new unverified account
        password_hash = Security.encrypt_password(password)
        account_id = AccountData.create(email_address, password_hash)

    @staticmethod
    def generate_access_token(email_address, password):
        result = AccountData.lookup_by_email(email_address)
        if Security.check_password(password, result[1]):
            credentials_object = {'account_id': result[0]}
            return Security.generate_access_token(credentials_object)
        else:
            raise InvalidAccountPassword()

    @staticmethod
    def start_email_verification(access_token, email_address):

        # authenticate and determine account to (re)associate with provided email address
        credentials = Security.extract_access_token_credentials(access_token)

        # (re)start email verification process
        verification_token = str(uuid.uuid4())
        VerificationData.create(verification_token, credentials.account_id, email_address)
        EmailGateway.send_email_verification(email_address, verification_token)

    @staticmethod
    def complete_email_verification(verification_token):

        # TODO: complete the email verification process
        VerificationData.verify(verification_token)
