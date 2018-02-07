from passlib.hash import bcrypt


class Security:

    @staticmethod
    def encrypt_password(password):
        return bcrypt.using(rounds=12).hash(password)
