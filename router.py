from datetime import datetime, timedelta
from fastapi import APIRouter, Cookie, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db.models import CallableUser
from dependency.auth import get_current_user_auth_header, get_current_user_cookie
from dependency.db import get_db
from schemas.users import Login, Token, UserIn, UserOut
from services.auth import authenticate, generate_token
from services.register import create_user

router = APIRouter()


@router.post("/admin/register", response_model=UserOut)
async def register(userIn: UserIn, db: Session = Depends(get_db)):
    """
    Register new user
    """
    res = create_user(db, userIn)
    return res


@router.post("/admin/login", response_model=Token)
async def login_user(user: Login, db: Session = Depends(get_db)):
    user = authenticate(db, user.email, user.password)
    if user:
        # login
        payload = {
            "iss": "http://localhost:8000",
            "sub": user.email,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(minutes=10),
        }
        token = generate_token(payload)
        response = JSONResponse({"token": token}, status_code=200)
        response.set_cookie(
            "access",
            token,
            max_age=60 * 2,
            samesite="lax",
        )
        return response
    else:
        return HTTPException(
            status_code=401, detail={"error": "Invalid email or password"}
        )


@router.get("/admin/me")
async def get_user(
    db: Session = Depends(get_db), email=Depends(get_current_user_auth_header)
):
    current_user = db.query(CallableUser).filter(CallableUser.email == email).first()
    return current_user
