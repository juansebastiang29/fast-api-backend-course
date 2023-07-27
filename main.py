from fastapi import FastAPI, Depends, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import List
from jwt_manager import create_token, validate_token
from fastapi.encoders import jsonable_encoder

from config.database import DatabaseSQLLite, Base, database_url
from middlewares.error_handler import ErrorHandler


from routers.movies import movie_router

app = FastAPI()
app.title = "Mi Aplicación con FastAPI"
app.version = "0.0.1"
app.add_middleware(ErrorHandler)
app.include_router(movie_router)

database_config = DatabaseSQLLite(database_url=database_url,Base=Base)

class User(BaseModel):
    email: str
    password: str
    


@app.post("/login", tags=['auth'])
def login(user: User) -> User:
    if user.email=="admin@gmail.com" and user.password == "admin":
        token =  create_token(data= user.dict())
        return JSONResponse(content=token)

@app.get(path='/', tags=['home'])
def message():
    return HTMLResponse("<h1>Hello World</h1>")

