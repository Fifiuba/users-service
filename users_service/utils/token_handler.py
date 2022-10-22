import os
from jose import jwt

if "RUN_ENV" in os.environ.keys() and os.environ["RUN_ENV"] == "test":
    JWT_SECRET_KEY = "testcase"
    ALGORITHM = "HS256"
else:
    JWT_SECRET_KEY = "superscreatekey"  # os.getenv("JWT_SECRET_KEY")
    ALGORITHM = "HS256"  # os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = 5


def create_access_token(user_id: int, user: bool) -> str:

    # expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"user_id": user_id, "user": user}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    decoded_jwt = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])

    return decoded_jwt
