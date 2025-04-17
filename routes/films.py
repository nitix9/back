from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List
import pyd

film_router=APIRouter(prefix="/movies", tags=["movies"])

@film_router.get("/", response_model=List[pyd.SchemaFilm])
def get_all_movies(db:Session=Depends(get_db)):
    movies= db.query(m.Film).all()
    return movies