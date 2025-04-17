from sqlalchemy.orm import Session
from database import engine
import models as m

m.Base.metadata.drop_all(bind=engine)  # Drop all tables
m.Base.metadata.create_all(bind=engine)

with Session(bind=engine) as session:
    g1=m.Genre(name='комедия', description='смешной жанр')
    session.add(g1)
    p1= m.Film(title='приключения паддингтона',release_year=2023,length=120, rating=10,description='приключения медвежонка',genres=[g1],poster='https://example.com/poster.jpg')
    session.add(p1)
    p2= m.Film(title='Босс-молокосос',release_year=2023,length=120, rating=10,description='приключения малыша',genres=[g1],poster='https://example.com/poster.jpg')
    session.add(p2)
    session.commit()