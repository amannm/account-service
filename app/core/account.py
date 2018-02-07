
import uuid
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

        # start email verification process
        Account.start_email_verification(account_id, email_address)

    @staticmethod
    def complete_email_verification(verification_token):

        # TODO: complete the email verification process
        VerificationData.verify(verification_token)

    @staticmethod
    def start_email_verification(account_id, email_address):

        # start or restart email verification process
        verification_token = str(uuid.uuid4())
        VerificationData.create(verification_token, account_id, email_address)
        EmailGateway.send_email_verification(email_address, verification_token)
