import os
from datetime import datetime, timedelta

from jose import jwt

if "RUN_ENV" in os.environ.keys() and os.environ["RUN_ENV"] == "test":
    JWT_SECRET_KEY = "testcase"
    ALGORITHM = "HS256"
else:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = 5




def create_access_token(user_id: int, user: bool) -> str:

    expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "user_id": user_id, "user": user}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def decode_token(token):
    decoded_jwt = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])

    return decoded_jwt
