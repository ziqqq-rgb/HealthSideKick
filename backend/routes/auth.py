from fastapi import APIRouter, Depends, HTTPException,  status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database.database import get_db
from models.user import User

from utilities.auth import hash_password, verify_password, create_access_token
from logger import logger

router = APIRouter()

class UserSignUp(BaseModel):
    username: str
    password: str
    email: str

class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/signup")
def signup(user: UserSignUp, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    hased_password = hash_password(user.password)
    new_user = User(
        username = user.username,
        email = user.email,
        hashed_password = hased_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(f"New user signed up: {user.email}")
    return {"message": "User created successfully", "user_id": new_user.id}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    access_token = create_access_token( data={ "sub": str(db_user.id), "username": db_user.username } )

    logger.info(f"User logged in: {user.email}")
    return {"access_token": access_token, "token_type": "bearer"}

