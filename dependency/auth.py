from fastapi import HTTPException, Request
import jwt
import os

# from jwt.exceptions import


def get_current_user(request: Request):
    jwt_header = request.headers.get("Authorization")
    if not jwt_header:
        raise HTTPException(status_code=401, detail="Missing access token")
    jwt_header = jwt_header.split(" ")
    header = jwt_header[0]
    token = jwt_header[-1]
    if header != "Bearer":
        raise HTTPException(status_code=401, detail="Bad header type")
    try:
        key = os.environ.get("SECRET_KEY")
        decoded = jwt.decode(token, key=key, algorithms=["HS256"])
    except (
        jwt.ExpiredSignatureError,
        jwt.InvalidSignatureError,
        jwt.InvalidTokenError,
    ):
        raise HTTPException(status_code=401, detail="Token is invalid/expired")

    return decoded.get("sub")
    # try:
    # except Exception as e:
