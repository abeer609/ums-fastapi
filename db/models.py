from datetime import datetime
from sqlalchemy import (
    Column,
    ForeignKey,
    DateTime,
    LargeBinary,
    String,
    Boolean,
    Integer,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class CallableUser(Base):
    __tablename__ = "callable_users"
    id = Column(Integer, primary_key=True, index=True)
    is_superuser = Column(Boolean, default=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone_number = Column(String(10), unique=True)
    is_staff = Column(Boolean, default=True)
    admin = relationship("Admin", backref="admin", uselist=False)


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    callable_user_id = Column(ForeignKey("callable_users.id", ondelete="CASCADE"))
    is_active = Column(Boolean, default=False)
    salt = Column(LargeBinary, nullable=True)
    special_key = Column(LargeBinary, unique=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    is_auto_password = Column(Boolean, default=False)


class PasswordModel(Base):
    __tablename__ = "password_table"
    id = Column(Integer, primary_key=True)
    password = Column(LargeBinary(length=255))
    hashed_special_key = Column(LargeBinary(length=255), index=True)
    is_enabled = Column(Boolean, default=True)
