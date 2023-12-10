import bcrypt
from fastapi import HTTPException
from sqlalchemy.orm import Session
from db.models import Admin, CallableUser, PasswordModel
from schemas.users import UserIn, UserOut
from validators.email import validate_email_backend
from validators.exceptions import ValidationError
from validators.password import validate_password
from validators.phone import validate_phone_backend

# user auth flow:
# hashed_sk = hash(admin.sk, admin.salt)
# filter with hashed sk in password  table
# checkpw(password, password_obj.hashed_sk)


def validate_user(db: Session, user: UserIn):
    errors = {}

    try:
        validate_password(user.password)
    except ValidationError as err:
        errors["password"] = err.detail
    try:
        validate_email_backend(db, user.email)
    except ValidationError as err:
        errors["email"] = err.detail
    try:
        validate_phone_backend(db, user.phone_number)
    except ValidationError as err:
        errors["phone_number"] = err.detail
    if errors:
        raise HTTPException(status_code=400, detail=errors)
    return user


def create_callable_user(db: Session, user: UserIn):
    callable_user = CallableUser(email=user.email, phone_number=user.phone_number)
    db.add(callable_user)
    db.commit()
    db.refresh(callable_user)
    return callable_user


def create_admin(db: Session, callable_user: CallableUser):
    salt: bytes = bcrypt.gensalt()
    special_key: bytes = bcrypt.hashpw(callable_user.email.encode(), salt)
    admin: Admin = Admin(
        callable_user_id=callable_user.id,
        salt=salt,
        special_key=special_key,
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


def create_salted_password(db: Session, admin: Admin, password: str):
    password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    password_object = PasswordModel(
        password=password,
        hashed_special_key=bcrypt.hashpw(admin.special_key, admin.salt),
    )
    db.add(password_object)
    db.commit()
    db.refresh(password_object)
    return password_object


def create_user(db: Session, user: UserIn) -> UserOut:
    # CallableUser(**userIn)
    # admin_object(salt=GenerateSalt(), sk=hash(email, salt)
    # password_object (password=hash_with_new_salt, hashed_special_key=hash(admin.salt, admin.sk))
    validate_user(db, user)
    callable_user = create_callable_user(db, user)
    admin = create_admin(db, callable_user)
    create_salted_password(db, admin, user.password)
    response = {
        "id": callable_user.id,
        "email": callable_user.email,
        "phone_number": callable_user.phone_number,
        "created_at": admin.created_at,
        "updated_at": admin.updated_at,
    }
    return response
