from pydantic import EmailStr
from sqlalchemy.orm import Session
from db.models import CallableUser
from validators.exceptions import ValidationError


def validate_email_backend(db: Session, email: EmailStr):
    email_exists = db.query(CallableUser).filter(CallableUser.email == email).first()
    if email_exists:
        raise ValidationError("this email is already taken")
