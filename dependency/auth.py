from fastapi import Cookie, HTTPException, Request
import jwt
import os

from validators.exceptions import ValidationError

# from jwt.exceptions import


def get_current_user_auth_header(request: Request):
    jwt_header = request.headers.get("Authorization")
    if not jwt_header:
        raise HTTPException(status_code=401, detail="Missing access token")
    jwt_header = jwt_header.split(" ")
    header = jwt_header[0]
    token = jwt_header[-1]
    if header != "Bearer":
        raise HTTPException(status_code=401, detail="Bad header type")
    try:
        decoded = validate_token(token)
    except ValidationError as err:
        raise HTTPException(status_code=400, detail=err.detail)
    return decoded.get("sub")
    # try:
    # except Exception as e:


def get_current_user_cookie(request: Request):
    access_token = request.cookies.get("access")
    if not access_token:
        raise HTTPException(status_code=401, detail="Missing access token")
    try:
        decoded = validate_token(access_token)
    except ValidationError as err:
        raise HTTPException(status_code=400, detail=err.detail)
    return decoded.get("sub")


def validate_token(token: str):
    try:
        key = os.environ.get("SECRET_KEY")
        if not key:
            raise EnvironmentError("cant find SECRET_KEY in env")
        decoded = jwt.decode(token, key=key, algorithms=["HS256"])
    except (
        jwt.ExpiredSignatureError,
        jwt.InvalidSignatureError,
        jwt.InvalidTokenError,
    ):
        raise ValidationError(detail="Token is invalid/expired")
    return decoded
