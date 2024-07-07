from sqlalchemy import create_engine, Column, Integer, String, Float, INTEGER, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship



#engine = create_engine('mysql+pymysql://root:root@localhost/movies')
engine = create_engine('sqlite:///data/movies.db')

conn = engine.connect()
Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movie'

    budget = Column(Float)
    movie_id = Column(INTEGER, primary_key=True)
    overview = Column(String)
    popularity = Column(INTEGER)
    release_date = Column(DateTime)
    revenue = Column(Float)
    runtime = Column(Float)
    title = Column(String)
    vote_average = Column(Float)
    vote_count = Column(Float)
    genres_clean = Column(String)
    production_companies_clean = Column(String)
    production_countries_clean = Column(String)
    retorno_de_inversion = Column(Float)
    release_year = Column(INTEGER)
    director_id = Column(Integer, ForeignKey('unique_directors.director_id'))
    director = relationship('Director', back_populates='movies')
    actors = relationship('Actor', secondary='movie_actor', back_populates='movies')

class Actor(Base):
    __tablename__ = 'unique_actors'

    actor_id = Column(Integer, primary_key=True)
    name = Column(String)
    movies = relationship('Movie', secondary='movie_actor', back_populates='actors')

class Director(Base):
    __tablename__ = 'unique_directors'

    director_id = Column(Integer, primary_key=True)
    name = Column(String)
    movies = relationship('Movie', back_populates='director')

class MovieActor(Base):
    __tablename__ = 'movie_actor'

    movie_id = Column(Integer, ForeignKey('movie.movie_id'), primary_key=True)
    actor_id = Column(Integer, ForeignKey('unique_actors.actor_id'), primary_key=True)

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

# Crear la sesión
Session = sessionmaker(bind=engine)
session = Session()

Session = sessionmaker(engine)
session = Session()


