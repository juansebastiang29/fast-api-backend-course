from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from config.database import DatabaseSQLLite, Base, database_url
from jwt_manager import create_token

from middlewares.error_handler import ErrorHandler

from routers.movies import movie_router
from routers.user import user_router


app = FastAPI()
app.title = "Mi Aplicación con FastAPI"
app.version = "0.0.1"
app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)


database_config = DatabaseSQLLite(database_url=database_url,Base=Base)


@app.get(path='/', tags=['home'])
def message():
    """get the fake message

    Returns:
        _type_: HTML response
    """
    return HTMLResponse("<h1>Hello World</h1>")
