from typing import List
from .base_models import *

class SchemaFilm(BaseFilm):
    genres: List[BaseGenre]

class SchemaGenre(BaseGenre):
    films: List[BaseFilm]