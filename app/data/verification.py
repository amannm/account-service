import psycopg2
from flask import g
from psycopg2 import errorcodes
from common.error import InvalidEmailVerification


class VerificationData:

    @staticmethod
    def create(verification_token, account_id, email_address):

        cancel_outstanding_query = """
            UPDATE
                email_verification
            SET
                status = 2
            WHERE
                status = 0 AND
                account_id = %s
        """

        insert_new_query = """
            INSERT INTO
                email_verification (verification_token, account_id, email_address)
            VALUES
                (%s, %s, %s)
        """

        with g.db.cursor() as cursor:
            try:
                cursor.execute(cancel_outstanding_query, account_id)
                cursor.execute(insert_new_query, (verification_token, account_id, email_address))
                g.db.commit()
            except psycopg2.Error as e:
                raise e

    @staticmethod
    def verify(verification_token):

        query = """
            UPDATE
                email_verification
            SET
                status = 1
            WHERE
                status = 0 AND
                verification_token = %s
        """

        with g.db.cursor() as cursor:
            try:
                cursor.execute(query, verification_token)
                if cursor.rowcount == 0:
                    g.db.rollback()
                    raise InvalidEmailVerification()
                g.db.commit()
            except psycopg2.Error as e:
                raise e
