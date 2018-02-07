from passlib.hash import bcrypt
from flask import g
import jwt

from common.error import InvalidAccessToken


class Security:

    # TODO: load secret from external resource like etcd at runtime

    @staticmethod
    def encrypt_password(password):
        return bcrypt.using(rounds=12).hash(password)

    @staticmethod
    def check_password(password, password_hash):
        return bcrypt.verify(password, password_hash)

    @staticmethod
    def generate_access_token(credentials_object):
        return jwt.encode(credentials_object, g.token_secret, algorithm='HS256')

    @staticmethod
    def extract_access_token_credentials(access_token):
        try:
            return jwt.decode(access_token, g.token_secret, algorithms=['HS256'])
        except jwt.InvalidTokenError as e:
            raise InvalidAccessToken()
