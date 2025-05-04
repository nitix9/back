from fastapi import FastAPI
from routes.films import film_router
from routes.genres import genre_router
from routes.users import user_router
from fastapi.staticfiles import StaticFiles
app = FastAPI()
app.include_router(film_router)
app.include_router(genre_router)
app.include_router(user_router)
app.mount("/files", StaticFiles(directory="files"), name="files")