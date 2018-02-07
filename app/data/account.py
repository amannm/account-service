import psycopg2
from flask import g
from psycopg2 import errorcodes
from common.error import EmailAlreadyRegistered


class AccountData:

    @staticmethod
    def create(email,
               password_hash):

        query = """
            INSERT INTO account
              (email, password)
            VALUES 
              (%s, %s)
            RETURNING id;
        """

        account_id = None

        with g.db.cursor() as cursor:
            try:
                cursor.execute(query, (email, password_hash))
                account_id = cursor.fetchone()[0]
                g.db.commit()
            except psycopg2.Error as e:
                if e.pgcode == errorcodes.UNIQUE_VIOLATION:
                    raise EmailAlreadyRegistered()
                else:
                    raise e

        return account_id
