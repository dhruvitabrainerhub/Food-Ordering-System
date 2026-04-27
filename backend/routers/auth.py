from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import UserCreate, UserLogin, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])
pwd = CryptContext(schemes=["bcrypt"])
SECRET = "supersecretkey123"


def create_token(data: dict):
    data["exp"] = datetime.utcnow() + timedelta(hours=24)
    return jwt.encode(data, SECRET, algorithm="HS256")


def get_current_user(token: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        user = db.query(User).filter(User.id == payload["id"]).first()
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(
        name=user.name,
        email=user.email,
        password=pwd.hash(user.password),
        phone=user.phone,
        address=user.address,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token = create_token({"id": new_user.id, "is_admin": new_user.is_admin})
    return {"token": token, "user": UserOut.from_orm(new_user)}


@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not pwd.verify(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token({"id": user.id, "is_admin": user.is_admin})
    return {"token": token, "user": UserOut.from_orm(user)}
