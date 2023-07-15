from jose import jwt
from decouple import config


SECRET_KEY = config('SECRET_KEY')


def create_token(user_id) -> str:
    """
    Create JWT token
    """
    payload = {
        "user_id": user_id,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def decode_token(token: str) -> dict:
    """
    Decode JWT token
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.JWTError:
        return None
