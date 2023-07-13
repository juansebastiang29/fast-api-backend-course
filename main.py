from fastapi import FastAPI, Depends, Body, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from fastapi.exceptions import HTTPException

from config.database import DatabaseSQLLite, Base, database_url
from models.movie import Movie

app = FastAPI()
app.title = "Mi Aplicación con FastAPI"
app.version = "0.0.1"

database_config = DatabaseSQLLite(database_url=database_url,Base=Base)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        
        data = validate_token(auth.credentials)
        
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="las credenciales no son validas")
    

class User(BaseModel):
    email: str
    password: str
    

class Movie(BaseModel):
    id: Optional[str] = None
    title: str = Field(default="Mi pelicula", max_length=35)
    year: int= Field(default=2022, le=2022)
    rating: float = Field(default=10, ge=1, e=10)
    category: str = Field(default="su_madre", max_length=35)
    
    class Config:
        schema_extra = {
            "example" : {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	}
        }

movies = [
    Movie(**{
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	}),
    Movie(**{
		"id": 2,
		"title": "Avatar edsadsadas",
		"overview": "En un exuberansadasdsadsate planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	}),
    Movie(**{
		"id": 3,
		"title": "Avatar fdsafdasfasd",
		"overview": "En un exuberansadasdsadsate planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	})
]

@app.post("/login", tags=['auth'])
def login(user: User) -> User:
    if user.email=="admin@gmail.com" and user.password == "admin":
        token =  create_token(data= user.dict())
        return JSONResponse(content=token)

@app.get(path='/', tags=['home'])
def message():
    return HTMLResponse("<h1>Hello World</h1>")


@app.get(path='/movies', tags=['movies'], response_model=List[Movie], status_code=200)
def get_movies() -> List[Movie]:
    return JSONResponse(status_code =  200, content= [m.dict() for m in movies])

@app.get(path='/movies/{id}', tags=['movies'], response_model=Movie, status_code=200, dependencies=[Depends(JWTBearer())])
def get_movie(id: int= Path(ge=1, le=2000))-> Movie:
    movie = next((movie for movie in movies if movie.id == id), None)
    if movie:
        return JSONResponse(status_code=200,content=movie.dict())
    else:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})

@app.get('/movies/', tags=['movies'],response_model=Movie, status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> Movie:
    
    movie = next((movie for movie in movies if movie.category == category), None)
    if movie:
        return JSONResponse(status_code=200,content=movie.dict())
    else:
        return JSONResponse(status_code=404,content={"message": "Category not found"})

@app.post('/movies', tags=['movies'], status_code=201)
def create_movie(movie: Movie) -> dict:
    res_, _ = get_idx_movie(id = movie.id, movies=movies)
    print(res_)
    if res_==0:
        movies.append(movie)
    else:
        JSONResponse(status_code=404,content={"message": "Ya existe la pelicula"})
    return JSONResponse(status_code=201, content={"message": "Se ha creado la Pelicula"})

def get_idx_movie(id: str, movies: list):
    results_ = [idx for idx, movie in enumerate(movies) if movie.id == id]
    if len(results_)>1:
        raise AssertionError("you have more than one movie")
    elif len(results_)==0:
        return 0, None
    else:
        idx_ = results_[0]
        return idx_, movies[idx_]
    
@app.put(path='/movies', tags=['movies'], response_model=List[Movie], status_code=200)
def modify_movie(id: str,movie: Movie) -> List[Movie]:
    idx_, _ = get_idx_movie(id, movies)
    if idx_>0:
        movies[idx_] = Movie(**movie.dict())
        return JSONResponse(status_code=200, content= [m.dict() for m in movies])
    elif idx_==0:
        return JSONResponse(content={"message": "Se ha creado la Pelicula"})
    else:
        return JSONResponse(status_code=404,content={"message": "Big error"})
    
@app.delete(path='/movies', tags=['movies'], response_model=List[Movie], status_code=200)
def delete_movie(id: str) -> List[Movie]: 
    idx_, _ = get_idx_movie(id, movies)
    if idx_:
        movies.pop(idx_)
        return JSONResponse(content= [m.dict() for m in movies])
    else:
        return JSONResponse(status_code=200, content={"message": "no existe la pelicula"})
