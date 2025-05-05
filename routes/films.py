from fastapi import APIRouter, HTTPException, Depends, UploadFile
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List
import pyd
import os
import uuid
from PIL import Image
from config import settings
import io
from auth import basic_auth

film_router=APIRouter(prefix="/movies", tags=["movies"])

@film_router.get("/", response_model=List[pyd.SchemaFilm])
def get_all_movies(db:Session=Depends(get_db)):
    movies= db.query(m.Film).all()
    return movies

@film_router.get("/{id}", response_model=pyd.SchemaFilm)
def get_one_movie(movie_id:int, db:Session=Depends(get_db)):
    movie = db.query(m.Film).filter(m.Film.id==movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    return movie

@film_router.post("/", response_model=pyd.BaseFilm)
def create_film(film:pyd.CreateFilm, db:Session=Depends(get_db),user=Depends(basic_auth)):
    film_db=db.query(m.Film).filter(m.Film.title==film.title).first()
    if film_db:
        raise HTTPException(status_code=400, detail="Фильм с таким именем уже существует")
    film_db = m.Film()
    film_db.title = film.title
    film_db.description = film.description
    film_db.release_year = film.release_year
    film_db.length = film.length
    film_db.rating = film.rating

    if film.genres:
        genres = db.query(m.Genre).filter(m.Genre.id.in_(film.genres)).all()
        if not genres:
            raise HTTPException(status_code=404, detail="Некоторые жанры не найдены")
        film_db.genres = genres
    db.add(film_db)
    db.commit()
    return film_db

@film_router.put("/image/{movie_id}", response_model=pyd.SchemaFilm)
def upload_image(movie_id:int, image:UploadFile, db:Session=Depends(get_db),user=Depends(basic_auth)):
    film_db=(
        db.query(m.Film).filter(m.Film.id==movie_id).first()
    )
    if not film_db:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    
    
    if image.content_type not in settings.ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Неверный тип файла")
    ext = image.filename.split(".")[-1].lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Недопустимое расширение файла")
    # Генерируем уникальное имя файла
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    contents = image.file.read()
    upload_dir = "files"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, unique_filename)
    if len(contents) > settings.MAX_FILE_SIZE:
        try:
            image_obj = Image.open(io.BytesIO(contents))

            # Преобразуем в RGB, если нужно
            if image_obj.mode in ("RGBA", "P"):
                image_obj = image_obj.convert("RGB")

            # Уменьшаем размер (по желанию)
            max_width, max_height = 1920, 1080
            image_obj.thumbnail((max_width, max_height))

            # Пробуем сохранить в памяти с уменьшением качества
            img_byte_arr = io.BytesIO()
            
            if ext in ["jpg", "jpeg"]:
                for quality in range(85, 10, -5):  # Попробуем от 85 до 15
                    img_byte_arr.seek(0)
                    img_byte_arr.truncate()
                    image_obj.save(img_byte_arr, format="JPEG", quality=quality, optimize=True)
                    if img_byte_arr.tell() <= settings.MAX_FILE_SIZE:
                        break

            elif ext == "png":
                # Для PNG просто оптимизируем — тут нет качества как у JPEG
                image_obj.save(img_byte_arr, format="PNG", optimize=True)

            else:
                raise HTTPException(status_code=400, detail="Неподдерживаемый формат")

            # Получаем содержимое
            img_byte_arr.seek(0)
            contents = img_byte_arr.read()

            if len(contents) > settings.MAX_FILE_SIZE:
                raise HTTPException(status_code=400, detail="Файл слишком большой, даже после сжатия")

            # Сохраняем на диск
            with open(file_path, "wb") as f:
                f.write(contents)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при обработке изображения: {e}")
    else:
        with open(file_path, "wb") as f:
                f.write(contents)
    film_db.poster= file_path
    db.commit()
    return film_db

@film_router.put("/{id}", response_model=pyd.SchemaFilm)
def update_film(movie_id:int, film:pyd.CreateFilm, db:Session=Depends(get_db),user=Depends(basic_auth)):
    movie = db.query(m.Film).filter(m.Film.id==movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    if film.title:
        movie.title = film.title
    if film.description:
        movie.description = film.description
    if film.release_year:
        movie.release_year = film.release_year
    if film.length:
        movie.length = film.length
    if film.rating:
        movie.rating = film.rating

    if film.genres:
        genres = db.query(m.Genre).filter(m.Genre.id.in_(film.genres)).all()
        if not genres:
            raise HTTPException(status_code=404, detail="Некоторые жанры не найдены")
        movie.genres = genres

    db.commit()
    return movie

@film_router.delete("/{id}")
def delete_film(movie_id:int, db:Session=Depends(get_db),user=Depends(basic_auth)):
    movie = db.query(m.Film).filter(m.Film.id==movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Фильм не найден")
    db.delete(movie)
    db.commit()
    return {"detail": "Фильм успешно удален"}