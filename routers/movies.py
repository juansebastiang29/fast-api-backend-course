from fastapi import FastAPI, Depends, Body, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter

from config.database import DatabaseSQLLite, Base, database_url
from models.movie import Movie as MovieModel
from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer


movie_router = APIRouter()

database_config = DatabaseSQLLite(database_url=database_url,Base=Base)

class Movie(BaseModel):
    id: Optional[str] = None
    title: str = Field(default="Mi pelicula", max_length=35)
    year: int= Field(default=2022, le=2022)
    rating: float = Field(default=10, ge=1, e=10)
    category: str = Field(default="su_madre", max_length=35)
    overview: str = Field(default="ha su madre ", max_length=200)
    
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


@movie_router.get(path='/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = database_config.session()
    result = db.query(MovieModel).all()
    print(result)
    return JSONResponse(status_code =  200, content= jsonable_encoder(result))
    # return JSONResponse(status_code =  200, content= result)
    

@movie_router.get(path='/movies/{id}', tags=['movies'], response_model=Movie, status_code=200)
def get_movie(id: int= Path(ge=1, le=2000))-> Movie:
    
    db = database_config.session()
    movie = db.query(MovieModel).filter(MovieModel.id==id).first()
    
    if not movie:
        return JSONResponse(status_code=404, content={'message': 'No encontrado'})
    if movie:
        return JSONResponse(status_code=200,content=jsonable_encoder(movie))
    else:
        return JSONResponse(status_code=404, content={"message": "Somethign went wrong"})

@movie_router.get('/movies/', tags=['movies'],response_model=Movie, status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> Movie:
    
    db = database_config.session()
    movie = db.query(MovieModel).filter(MovieModel.category==category).all()
    
    if movie:
        return JSONResponse(status_code=200,content=jsonable_encoder(movie))
    else:
        return JSONResponse(status_code=404,content={"message": "Category not found"})

@movie_router.post('/movies', tags=['movies'], status_code=201)
def create_movie(movie: Movie) -> dict:
    db = database_config.session()
    new_movie = MovieModel(**movie.dict())
    
    db.add(new_movie)
    db.commit()
    
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
    
@movie_router.put(path='/movies', tags=['movies'], response_model=List[Movie], status_code=200)
def modify_movie(id: str,movie: Movie) -> List[Movie]:
    
    db = database_config.session()
    result_ = db.query(MovieModel).filter(MovieModel.id==id).first()
    
    if not result_:
        return JSONResponse(status_code=404,content={"message": "No encontrado"})
    
    if result_:
        result_.title = movie.title
        result_.overview = movie.overview
        result_.category = movie.category
        result_.year = movie.year
        result_.rating = movie.rating
        db.commit()
        return JSONResponse(status_code=200,content={"message": "Sehaactualizado la pelicula"})
        
    else:
        return JSONResponse(status_code=404,content={"message": "Big error"})
    
@movie_router.delete(path='/movies', tags=['movies'], response_model=List[Movie], status_code=200)
def delete_movie(id: str) -> List[Movie]: 
    
    db = database_config.session()
    result_ = db.query(MovieModel).filter(MovieModel.id==id).first()
    
    if not result_:
        return JSONResponse(status_code=404,content={"message": "No encontrado"})
    if result_:
        db.delete(result_)
        db.commit()
    
        return JSONResponse(status_code=200, content={"message": "Me borrasteeee"})
