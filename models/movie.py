from config.database import Base
from sqlalchemy import Column as col
from sqlalchemy import Integer, String, Float


class Movie(Base):
    
    __tablename__ = "movies"
    
    # table fields
    id = col(Integer, primary_key=True)
    title = col(String)
    overview = col(String)
    year = col(Integer)    
    rating = col(Float)
    category = col(String)
    