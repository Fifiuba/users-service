class UserInfoException(Exception):
    ...

class UserAlreadyExists(UserInfoException):
    def __init__(self):
        self.status_code = 409  # conflic
        self.details = "The user already exists"
