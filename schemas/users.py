# {
#   "is_otp_verification": false,
#   "password": "abeer5066$",
#   "email": "user@example.com",
#   "phone_number": "1968971251"
# }

from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserIn(BaseModel):
    is_otp_verification: bool
    password: str
    email: EmailStr
    phone_number: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    phone_number: str
    created_at: datetime
    updated_at: datetime


class Login(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access: str
