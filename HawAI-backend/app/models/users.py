from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserIn(BaseModel):
    email: EmailStr
    password: str


class UserDB(BaseModel):
    id: Optional[str]
    email: EmailStr
    password_hash: str
    created_at: datetime = datetime.utcnow()


class UserOut(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime


