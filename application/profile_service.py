from sqlalchemy.orm import Session
from app.infrastructure.repositories.user_repo import User
from app.application.auth_service import verify_password
from passlib.context import CryptContext
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def update_profile(db: Session, user_id: int, data: dict):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    for key, value in data.items():
        if hasattr(user, key):
            setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def update_about(db: Session, user_id: int, data: dict):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    allowed_fields = ["birthday", "location", "relation", "job", "education", "website"]

    for key in allowed_fields:
        if key in data and hasattr(user, key):
            setattr(user, key, data[key])

    db.commit()
    db.refresh(user)
    return user

def change_password(db: Session, user_id: int, current_password: str, new_password: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not verify_password(current_password, user.password_hash):
        return None
    user.password_hash = pwd_context.hash(new_password)
    db.commit()
    return user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False
