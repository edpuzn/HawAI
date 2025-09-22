from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Response, Request
from passlib.hash import bcrypt
from pydantic import BaseModel, EmailStr
import jwt
from app.db.mongo import get_db
from app.config import settings


router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterIn(BaseModel):
    email: EmailStr
    password: str


class LoginIn(BaseModel):
    email: EmailStr
    password: str


async def create_jwt(user_id: str):
    exp = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    return jwt.encode({"sub": user_id, "exp": exp}, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


@router.post("/register")
async def register(data: RegisterIn, db=Depends(get_db)):
    users = db["users"]
    exists = await users.find_one({"email": data.email})
    if exists:
        raise HTTPException(status_code=400, detail="email exists")
    pw = bcrypt.hash(data.password)
    doc = {"email": data.email, "password_hash": pw, "created_at": datetime.utcnow()}
    res = await users.insert_one(doc)
    return {"id": str(res.inserted_id), "email": data.email}


@router.post("/login")
async def login(data: LoginIn, response: Response, db=Depends(get_db)):
    users = db["users"]
    user = await users.find_one({"email": data.email})
    if not user or not bcrypt.verify(data.password, user.get("password_hash")):
        raise HTTPException(status_code=401, detail="invalid credentials")
    token = await create_jwt(str(user["_id"]))
    response.set_cookie("access_token", token, httponly=True, samesite="Lax")
    return {"ok": True}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"ok": True}


def require_user_id(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="no token")
    try:
        data = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
        return data.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="invalid token")


@router.get("/me")
async def me(user_id: str = Depends(require_user_id)):
    return {"id": user_id}


