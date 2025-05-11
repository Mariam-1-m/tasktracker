from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str  # plain for now; will hash later
    photo: Optional[str] = None
    phone:Optional[str] = None
    is_admin:Optional[bool] = None
    job: Optional[str] = None
    birthday: Optional[date] = None
    location: Optional[str] = None
    relation: Optional[str] = None
    education: Optional[str] = None

class UserInDB(BaseModel):
    id: int
    username: str
    email: str
    password_hash: str

from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class AboutUpdateRequest(BaseModel):
    birthday: Optional[date]
    location: Optional[str]
    relation: Optional[str]
    job: Optional[str]
    education: Optional[str]
    website: Optional[str]
