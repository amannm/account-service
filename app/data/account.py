import psycopg2
from flask import g
from psycopg2 import errorcodes
from common.error import EmailAlreadyRegistered
from common.error import AccountEmailNotFound


class AccountData:

    @staticmethod
    def create(email_address,
               password_hash):

        query = """
            INSERT INTO account
              (email_address, password)
            VALUES 
              (%s, %s)
            RETURNING id;
        """

        account_id = None

        with g.db.cursor() as cursor:
            try:
                cursor.execute(query, (email_address, password_hash))
                account_id = cursor.fetchone()[0]
                g.db.commit()
            except psycopg2.Error as e:
                if e.pgcode == errorcodes.UNIQUE_VIOLATION:
                    raise EmailAlreadyRegistered()
                else:
                    raise e

        return account_id

    @staticmethod
    def lookup_by_email(email_address):

        query = """
            SELECT
                id, password
            FROM
                account
            WHERE
                email_address = %s
        """

        result = None

        with g.db.cursor() as cursor:
            try:
                cursor.execute(query, email_address)
                result = cursor.fetchone()
                if result is None:
                    raise AccountEmailNotFound()
            except psycopg2.Error as e:
                raise e

        return result
