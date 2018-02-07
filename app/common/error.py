

class Error(Exception):
    pass


class EmailAlreadyRegistered(Error):

    def __init__(self):
        self.message = 'provided email address is already registered'


class InvalidEmailVerification(Error):

    def __init__(self):
        self.message = 'provided email verification token is invalid'
