from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.infrastructure.repositories.user_repo import User
from app.domain.models.user_model import UserCreate
from app.infrastructure.db.db import SessionLocal
from fastapi import HTTPException
from app.infrastructure.repositories.user_repo import get_user_by_email
from app.infrastructure.jwt.auth_utils import verify_password, create_access_token


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def register_user(user_data: UserCreate, db: Session):
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email or username already exists")
    hashed_password = pwd_context.hash(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        photo=user_data.photo,
        job=user_data.job,
        birthday=user_data.birthday,
        location=user_data.location,
        relation=user_data.relation,
        education=user_data.education,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    access_token = create_access_token(data={"user_id": db_user.id})
    return {"access_token": access_token, "token_type": "bearer"}
    

def login_user(email: str, password: str, db):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
