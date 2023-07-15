from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from core.db import SessionLocal

from .jwt import create_token, decode_token
from .models import User
from .schemas import UserLogin, UserRegister

router = APIRouter()


@router.post("/register")
async def register_user(user: UserRegister):
    user = User(username=user.username, password=user.password)
    with SessionLocal() as session:
        session.add(user)
        try:
            session.commit()
        except IntegrityError:
            return JSONResponse({"message": "User already exists"}, status_code=400)
    return JSONResponse({"message": "User registered successfully"}, status_code=201)


@router.post("/login")
async def login_user(user: UserLogin):
    with SessionLocal() as session:
        user = session.query(User).filter(
            User.username == user.username,
            User.password == user.password
        ).first()

    if user:
        token = create_token(user.id)
        return JSONResponse({"token": token}, status_code=200)
    return JSONResponse({"message": "Invalid credentials"}, status_code=401)
