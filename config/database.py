import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path

sqllite_file_name = "database.sqlite"

#leer el path en el q se encuentra el script actual
base_dir = Path(__file__).resolve().parent.parent

#declare the database url
database_url = f"sqlite:///{os.path.join(base_dir,sqllite_file_name)}"


Base = declarative_base()

class DatabaseSQLLite:
    
    def __init__(self, database_url: str, Base) -> None:
        self.database_url  = database_url
        print(database_url)
        self.Base = Base
        self.start_database_session()
    
    def start_database_session(self):
        self.engine = create_engine(self.database_url, echo=True)
        self.session = sessionmaker(bind=self.engine)
        self.Base.metadata.create_all(bind=self.engine)
        

