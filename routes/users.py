from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List
import pyd
from auth import basic_auth

user_router=APIRouter(prefix="/users", tags=["users"])

@user_router.get("/", response_model=List[pyd.BaseUser])
def get_all_users(db:Session=Depends(get_db),user=Depends(basic_auth)):
    users= db.query(m.User).all()
    return users

@user_router.post("/", response_model=pyd.BaseUser)
def user_reg(create_user: pyd.CreateUser, db:Session=Depends(get_db)):
    user_db=db.query(m.User).filter(m.User.username==create_user.username).first()
    if user_db:
        raise HTTPException(status_code=400, detail="User already exists")
    user_db=m.User()
    user_db.username=create_user.username
    user_db.hashed_password=create_user.password
    user_db.email=create_user.email
    db.add(user_db)
    db.commit()
    return user_db
