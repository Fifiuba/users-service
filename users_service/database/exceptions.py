class UserInfoException(Exception):
    ...

class PassengerAlreadyExists(UserInfoException):
    def __init__(self):
        self.status_code = 409  # conflic
        self.detail = "The passenger already exists"

class DriverAlreadyExists(UserInfoException):
    def __init__(self):
        self.status_code = 409  # conflic
        self.detail = "The passenger already exists"

class UserAlreadyExists(UserInfoException):
    def __init__(self,user_id):
        self.status_code = 409  # conflic
        self.detail = "The user already exists"
        self.user = user


class PassengerNotFoundError(UserInfoException):
    def __init__(self):
        self.status_code = 404  # conflic
        self.detail = "The passenger does not exists"


class DriverNotFoundError(UserInfoException):
    def __init__(self):
        self.status_code = 404  # conflic
        self.detail = "The driver does not exists"
