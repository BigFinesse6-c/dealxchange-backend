# app/schemas/user.py
from pydantic import BaseModel
from typing import Optional
from app.models.user import UserRole
from enum import Enum

class UserRead(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    role: UserRole  # ✅ Must include role
    is_active: bool
    approved: bool
    is_admin: bool 
    approved: bool

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: Optional[str]
    role: Optional[UserRole] = UserRole.buyer

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

