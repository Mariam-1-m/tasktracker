from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.infrastructure.db.db import get_db
from app.infrastructure.repositories.user_repo import User
from app.infrastructure.jwt.jwt_handler import SECRET_KEY, ALGORITHM ,decode_access_token # ensure these exist in your project

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print("Token received:", token)
    try:
        payload = decode_access_token(token)
        print("Decoded payload:", payload)
        user_id = payload.get("user_id")
        if user_id is None:
            print("Missing user_id")
            raise HTTPException(status_code=401, detail="Missing user_id in token")
    except JWTError as e:
        print("JWT decode failed:", str(e))
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    print("User from DB:", user)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


