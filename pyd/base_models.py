from pydantic import BaseModel, Field
from datetime import datetime
class BaseGenre(BaseModel):
    id:int = Field(example=1)
    name:str = Field(example="Комедия")
    description:str = Field(example="Смешной фильм")
    

class BaseFilm(BaseModel):
    id:int = Field(example=1)
    title:str = Field(example="Зеленая миля")
    release_year:int = Field(example=1999)
    length:int = Field(example=120)
    rating:int = Field(example=10)
    description:str = Field(example="Фильм о тюремной жизни")
    poster:str|None = Field(example="https://example.com/poster.jpg")
    created_at:datetime = Field(example="2023-01-01T00:00:00Z")