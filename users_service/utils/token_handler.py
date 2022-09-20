import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = 'superscreatekey' #os.environ.get('JWT_SECRET_KEY')   # should be kept secret


def create_access_token(user_id: int, user: bool) -> str:

    expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "user_id": user_id, "user": user}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def decode_token(token):
    decoded_jwt = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])

    return decoded_jwt