from models.movie import Movie as MovieModel
from typing import List
from schemas.movie import Movie

from sqlalchemy.orm.session import Session

from fastapi.responses import JSONResponse



class MovieService:
    """this class implements the movie services
    """
    def __init__(self, database_connection: Session) -> None:
        self.database_connection = database_connection

    def get_movies(self):
        """_summary_
        """
        return self.database_connection.query(MovieModel).all()

    def get_movie(self, movie_id):
        """_summary_

        Args:
            id (str): movie id

        Returns:
            _type_: _description_
        """
        return self.database_connection.query(MovieModel).filter(MovieModel.id==movie_id).first()
    
    def get_movie_by_category(self, category: str) -> List[MovieModel]:
        """_summary_
        Args:
            category (_type_): _description_
        """
        
        return self.database_connection.query(MovieModel).filter(MovieModel.category==category).all()
    
    def create_movie(self, movie: Movie):
        """_summary_
        """
        #parse movie
        new_movie_obj  = MovieModel(**movie.dict())
        self.database_connection.add(new_movie_obj)
        print(movie)
        self.database_connection.commit()
        return
    
    def update_movie(self, id: int, data: Movie):
        movie = self.database_connection.query(MovieModel).filter(MovieModel.id==id).first()
        movie.title = data.title
        movie.overview = data.overview
        movie.year = data.year
        movie.rating = data.rating
        movie.category = data.category
        
        self.database_connection.commit()
        return
    
    def delete_movie(self, movie_id: int):
        movie_to_delete = self.database_connection.query(MovieModel).filter(MovieModel.id==movie_id).first()
        if not movie_to_delete:
            return JSONResponse(status_code=404,content={"message": "No encontrado"})
        self.database_connection.delete(movie_to_delete)
        self.database_connection.commit()
        return