from sqlalchemy import create_engine, Column, Integer, String, Float, INTEGER, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine('mysql+pymysql://root:root@localhost/movies')


conn = engine.connect()
Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movie'

    budget = Column(Float)
    movie_id = Column(INTEGER, primary_key=True)       
    original_title = Column(String)     
    overview = Column(String)     
    popularity = Column(INTEGER)    
    release_date = Column(DateTime)
    revenue = Column(Float)   
    runtime = Column(Float) 
    status = Column(String)     
    title = Column(String)    
    vote_average = Column(Float)       
    vote_count = Column(Float)      
    genres_clean = Column(String)     
    collection_clean = Column(String)
    director_id = Column(INTEGER)       
    production_companies_clean = Column(String)     
    production_countries_clean = Column(String)      
    spoken_languages_clean = Column(String)        
    retorno_de_inversion = Column(Float)      
    release_year = Column(INTEGER)  

class Actor(Base):
    __tablename__ = 'unique_actors'
    name = Column(String)
    actor_id = Column(INTEGER, primary_key=True)

class Director(Base):

    __tablename__ = 'director'
    name = Column(String)
    movie_id = Column(INTEGER)
    director_id = Column(INTEGER, primary_key=True)

class MovieActor(Base):
    __tablename__ = 'movie_actor'
    movie_id = Column(INTEGER, primary_key=True)
    actor_id = Column(INTEGER, primary_key=True)

Session = sessionmaker(engine)
session = Session()
