from fastapi import FastAPI
from routes.films import film_router
from routes.genres import genre_router

app = FastAPI()
app.include_router(film_router)
app.include_router(genre_router)