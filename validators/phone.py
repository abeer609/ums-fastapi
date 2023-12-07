from sqlalchemy.orm import Session
from db.models import CallableUser
from validators.exceptions import ValidationError


def validate_phone_backend(db: Session, phone_number: str):
    phone_exists = (
        db.query(CallableUser).filter(CallableUser.phone_number == phone_number).first()
    )
    if phone_exists:
        raise ValidationError("this phone number is already taken")
