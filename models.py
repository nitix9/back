from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime,DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
film_genre = Table(
    "film_genre",
    Base.metadata,
    Column("film_id", ForeignKey("films.id"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id"), primary_key=True)
)

class Film(Base):
    __tablename__ = "films"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    release_year = Column(Integer, nullable=False)
    length = Column(Integer, nullable=False)
    rating = Column(DECIMAL, nullable=False)
    description = Column(String(255), nullable=True)
    poster=Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    genres = relationship("Genre", secondary="film_genre", back_populates="films")

class Genre(Base):
    __tablename__ = "genres"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    films = relationship("Film", secondary="film_genre", back_populates="genres")

