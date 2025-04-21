from fastapi import APIRouter, HTTPException, Depends
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List
import pyd

genre_router=APIRouter(prefix="/genres", tags=["genres"])

@genre_router.get("/", response_model=List[pyd.BaseGenre])
def get_all_genre(db:Session=Depends(get_db)):
    genres= db.query(m.Genre).all()
    return genres

@genre_router.post("/", response_model=pyd.CreateGenre)
def create_genre(genre:pyd.CreateGenre, db:Session=Depends(get_db)):
    genre_db=db.query(m.Genre).filter(m.Genre.name==genre.name).first()
    if genre_db:
        raise HTTPException(status_code=400, detail="Жанр с таким именем уже существует")
    genre_db = m.Genre()
    genre_db.name = genre.name
    genre_db.description = genre.description
    db.add(genre_db)
    db.commit()
    return genre_db
