from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.db.db import SessionLocal
from app.domain.models.user_model import UserCreate
from app.application.auth_service import register_user
from app.domain.models.user_model import UserLogin
from app.application.auth_service import login_user
from app.infrastructure.db.db  import get_db
from app.infrastructure.jwt.auth_utils import create_access_token
router = APIRouter()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return register_user(user, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Registration failed: " + str(e))

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
   
    return login_user(user.email, user.password, db) 