import requests

from pydantic import BaseModel, validator
from decouple import config


HUNTER_API_KEY = config('HUNTER_API_KEY')


class UserRegister(BaseModel):
    username: str
    password: str
    email: str

    @validator('email')
    def validate_email(cls, email):
        # validating email using emailhunter
        response = requests.get(
            f'https://api.hunter.io/v2/email-verifier?email={email}&api_key={HUNTER_API_KEY}'
        )
        if response.json()['data']['status'] == 'invalid':
            raise ValueError('Invalid email')
        elif response.status_code != 200:
            raise ValueError(
                'Problems with email verification. Try again later')
        return email


class UserLogin(BaseModel):
    username: str
    password: str
