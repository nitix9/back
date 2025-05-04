from fastapi import HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from database import get_db
import models

security = HTTPBasic()

def basic_auth(credentials: HTTPBasicCredentials = Depends(security),db:Session=Depends(get_db)):
    user_db = db.query(models.User).filter(models.User.username == credentials.username).first()
    if not user_db:
        raise HTTPException(
            status_code=401,
            detail="Пользователь не найден"
        )
    if user_db.hashed_password == credentials.password:
        return user_db
    
    raise HTTPException(
        status_code=401,
        detail="Invalid credentials"
    )