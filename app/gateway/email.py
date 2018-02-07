import smtplib
from flask import g
from urllib.parse import urlencode
from email.message import EmailMessage


class EmailGateway:

    @staticmethod
    def send_email_verification(email_address, verification_token):
        email_verification_url = 'https://account.example.com/verification/email/' + urlencode(verification_token)

        message = EmailMessage()
        message['Subject'] = "Email verification for your example.com account"
        message['From'] = 'verification@example.com'
        message['To'] = email_address
        message.set_content("""\
            <div>
                <p>Click the below link to verify your email ({{email}})</p>
                <p><a href="{email_verification_url}">{email_verification_url}</a></p>
                <p>Thanks</p>
            </div>
        """.format(email_verification_url=email_verification_url))

        with smtplib.SMTP(
                host=g.smtp_config['host'],
                port=g.smtp_config['port']) as server:
            server.login(
                user=g.smtp_config['user'],
                password=g.smtp_config['password'])
            server.send_message(message)
