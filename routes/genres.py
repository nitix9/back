from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List
import pyd

genre_router=APIRouter(prefix="/genres", tags=["genres"])