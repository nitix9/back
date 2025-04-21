from pydantic import BaseModel, Field

class CreateGenre(BaseModel):
    name:str = Field(example="Комедия")
    description:str = Field(example="Смешной фильм")
    

class CreateFilm(BaseModel):
    title:str = Field(example="Зеленая миля")
    release_year:int = Field(example=1999)
    length:int = Field(example=120)
    rating:int = Field(example=10)
    description:str = Field(example="Фильм о тюремной жизни")
    genres:list[int] = Field(example=[1, 2],min_length=1)