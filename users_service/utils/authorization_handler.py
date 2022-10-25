import re
from users_service.database import exceptions

validator = re.compile(r"^(Bearer\s)(.*)")


def is_auth(headers):
    header = headers.get("authorization")
    if header is None:
        print("no me llego un header")
        raise exceptions.UnauthorizeUser
    if not validator.match(header):
        print("No soy un header valido")
        raise exceptions.UnauthorizeUser


def get_token(headers):
    header = headers.get("authorization")
    _b, token = validator.search(header).groups()
    return token

def is_admin(user):
    if user != "admin":
        raise exceptions.UnauthorizeUser
    