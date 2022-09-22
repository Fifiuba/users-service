import re
from users_service.database import exceptions

validator = re.compile(r"^(Baerer\s)(.*)")


def is_auth(headers):
    header = headers.get("authorization")
    if header is None or not validator.match(header):
        raise exceptions.UnauthorizeUser


def get_token(headers):
    header = headers.get("authorization")
    _b, token = validator.search(header).groups()
    return token
