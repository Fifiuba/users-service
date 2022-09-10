class UserInfoException(Exception):
    ...


class UserAlreadyExists(UserInfoException):
    def __init__(self):
        self.status_code = 409  # conflic
        self.detail = "The user already exists"


class PassengerNotFoundError(UserInfoException):
    def __init__(self):
        self.status_code = 404  # conflic
        self.detail = "The passenger does not exists"


class DriverNotFoundError(UserInfoException):
    def __init__(self):
        self.status_code = 404  # conflic
        self.detail = "The driver does not exists"
