from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.database import get_db
from models.user import User

import os 
from datetime import datetime, timedelta, timezone
import bcrypt  
import jwt
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str) -> str:

    password_bytes = password.encode('utf-8')[:72]
    
    salt = bcrypt.gensalt()

    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    
    return hashed_bytes.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:

    plain_password_bytes = plain_password.encode('utf-8')[:72]
    
    hashed_password_bytes = hashed_password.encode('utf-8')
    
    return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        
    except jwt.PyJWTError:
        raise credentials_exception
    
    user = db.quesry(User).filter(User.id == int(user_id_str)).first()
    if user is None:
        raise credentials_exception
    
    return user