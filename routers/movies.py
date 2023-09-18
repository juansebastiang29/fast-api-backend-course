from fastapi import Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter

from config.database import DatabaseSQLLite, Base, database_url
from models.movie import Movie as MovieModel
from middlewares.jwt_bearer import JWTBearer

from services.movie import MovieService

from schemas.movie import Movie

movie_router = APIRouter()

database_config = DatabaseSQLLite(database_url=database_url,Base=Base)



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
    result = MovieService(database_connection=db).get_movies()
    result = db.query(MovieModel).all()
    print(result)
    return JSONResponse(status_code =  200, content= jsonable_encoder(result))

@movie_router.get(path='/movies/{id}', tags=['movies'], response_model=Movie, status_code=200)
def get_movie(id: int= Path(ge=1, le=2000))-> Movie:
    
    db = database_config.session()
    movie = MovieService(database_connection=db).get_movie(movie_id = id)
    
    if not movie:
        return JSONResponse(status_code=404, content={'message': 'No encontrado'})
    if movie:
        return JSONResponse(status_code=200,content=jsonable_encoder(movie))
    else:
        return JSONResponse(status_code=404, content={"message": "Something went wrong"})

@movie_router.get('/movies/', tags=['movies'],response_model=Movie, status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> Movie:
    
    db = database_config.session()
    movie = MovieService(database_connection=db).get_movie_by_category(category = category)
    
    if movie:
        return JSONResponse(status_code=200,content=jsonable_encoder(movie))
    else:
        return JSONResponse(status_code=404,content={"message": "Category not found"})

@movie_router.post('/movies', tags=['movies'], status_code=201)
def create_movie(movie: Movie) -> dict:
    db = database_config.session()
    # try:
    MovieService(database_connection=db).create_movie(movie=movie)
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
    result_ = MovieService(database_connection=db).get_movie(movie_id=id)
    if not result_:
        return JSONResponse(status_code=404,content={"message": "Movie not found"})
    
    MovieService(database_connection=db).update_movie(id=id, data=movie)
    return JSONResponse(status_code=200,content={"message": "Sehaactualizado la pelicula"})
    
@movie_router.delete(path='/movies', tags=['movies'], response_model=List[Movie], status_code=200)
def delete_movie(id: str) -> List[Movie]: 
    
    db = database_config.session()
    
    MovieService(database_connection=db).delete_movie(movie_id=id)
    return JSONResponse(status_code=200, content={"message": "Me borrasteeee"})
