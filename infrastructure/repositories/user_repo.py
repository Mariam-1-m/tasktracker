from sqlalchemy import Column, Integer, String, Date ,Boolean
from app.infrastructure.db.db import Base
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    photo = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    job = Column(String, nullable=True)
    birthday = Column(Date, nullable=True)
    location = Column(String, nullable=True)
    relation = Column(String, nullable=True)
    education = Column(String, nullable=True)
    is_admin = Column(Boolean, nullable=True)

def get_user_by_email(db, email: str):
    return db.query(User).filter(User.email == email).first() 
