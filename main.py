from fastapi import FastAPI, Query
import random
import math
app=FastAPI()

@app.get("/")
def read_root():
    return{"Hello":"NIKITA"}

@app.get("/about_me")
def show_about_me(c:int,a:int = None,b:int=6):
    return{
        'name':'Nikitos Bandito',
        'years':'49',
        'work':'Banditos',
        'hobby':'No hobby',
        's':a+b,
    }

@app.get('/random_num')
def show_random_num():
    return{'rand_num':random.randint(0,100)}

@app.get('/square_tr')
def show_square_tr(a:int=Query(gt=0),b:int=Query(gt=0),c:int=Query(gt=0)):
    p=(a+b+c)/2
    if (a>b+c or b>a+c or c>b+a):
        return {'Ошибка':'Сторона не может быть больше суммы двух сторон'}
    else:
        return{'square':math.sqrt(p*(p-a)*(p-b)*(p-c))}