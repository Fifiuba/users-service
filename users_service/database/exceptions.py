class UserInfoException(Exception):
    ...


class PassengerAlreadyExists(UserInfoException):
    def __init__(self):
        self.status_code = 409  # conflic
        self.detail = "The passenger already exists"


class DriverAlreadyExists(UserInfoException):
    def __init__(self):
        self.status_code = 409  # conflic
        self.detail = "The driver already exists"


class UserAlreadyExists(UserInfoException):
    def __init__(self):
        self.status_code = 409  # conflic
        self.detail = "The user already exists"


class UserWrongLoginInformation(UserInfoException):
    def __init__(self):
        self.status_code = 401  # conflic
        self.detail = "The username/password is incorrect"


class PassengerNotFoundError(UserInfoException):
    def __init__(self):
        self.status_code = 404  # conflic
        self.detail = "The passenger does not exists"


class DriverNotFoundError(UserInfoException):
    def __init__(self):
        self.status_code = 404  # conflic
        self.detail = "The driver does not exists"


class UnauthorizeUser(UserInfoException):
    def __init__(self):
        self.status_code = 401
        self.detail = "The user is not authorize"


class UserNotFoundError(UserInfoException):
    def __init__(self):
        self.status_code = 404  # conflic
        self.detail = "The user does not exists"


class UserIsBlock(UserInfoException):
    def __init__(self):
        self.status_code = 409  # conflic
        self.detail = "The user is block"
