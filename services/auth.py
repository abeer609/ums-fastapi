from datetime import datetime, timedelta
import os
import bcrypt
from dotenv import load_dotenv
from fastapi import HTTPException
import jwt
from pydantic import EmailStr
from sqlalchemy.orm import Session
from db.models import Admin, CallableUser, PasswordModel

load_dotenv()


def authenticate(db: Session, email: EmailStr, password: str) -> CallableUser:
    callable_object: CallableUser = (
        db.query(CallableUser).filter(CallableUser.email == email).first()
    )
    if not callable_object:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    admin: Admin = callable_object.admin
    is_correct: bool = check_password(db, password, admin)
    if not is_correct:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not admin.is_active:
        raise HTTPException(status_code=403, detail="user is not active")
    return callable_object


# Todo: check_password should not know about db
def check_password(db: Session, password: str, admin: Admin) -> bool:
    hashed_special_key: bytes = bcrypt.hashpw(admin.special_key, admin.salt)
    password_object: PasswordModel = (
        db.query(PasswordModel)
        .filter(PasswordModel.hashed_special_key == hashed_special_key)
        .first()
    )
    if password_object:
        return bcrypt.checkpw(password.encode(), password_object.password)
    return False


# Todo: generate token should not know about user
def generate_token(user: CallableUser) -> str:
    payload = {
        "iss": "http://localhost:8000",
        "sub": user.email,
        "exp": datetime.utcnow() + timedelta(minutes=10),
    }
    key: str = os.environ.get("SECRET_KEY")
    token: str = jwt.encode(payload, key=key)
    return token
