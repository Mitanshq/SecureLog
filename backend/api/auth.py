from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.schemas.users import UserCreate
from backend.schemas.users import UserLogin
from backend.databases.db import get_db
from backend.services.auth_service import register_user, login_user
from backend.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    print("API HIT")   # 👈 ADD THIS
    print(user)
    
    new_user = register_user(db, user.username, user.email, user.password)

    if not new_user:
        raise HTTPException(status_code=400, detail="User already exists")

    return {
        "message": "Registered successfully",
        "user_id": new_user.id
    }


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = login_user(db, user.email, user.password)

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "user_id": db_user.id
    }


@router.get("/user/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }