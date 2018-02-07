

class Error(Exception):
    pass


class EmailAlreadyRegistered(Error):

    def __init__(self):
        self.message = 'provided email address is already registered'


class InvalidVerificationToken(Error):

    def __init__(self):
        self.message = 'provided email verification token is invalid'


class AccountEmailNotFound(Error):

    def __init__(self):
        self.message = 'provided email is not associated with an account'


class InvalidAccountPassword(Error):

    def __init__(self):
        self.message = 'invalid password was provided while attempting account access'


class InvalidAccessToken(Error):

    def __init__(self):
        self.message = 'invalid access token provided to secured endpoint'
