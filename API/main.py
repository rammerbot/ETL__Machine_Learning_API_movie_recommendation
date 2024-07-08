from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from querys import (obtener_cantidad_peliculas_por_mes, obtener_cantidad_peliculas_por_dia, 
                    consultar_pelicula_por_score, consultar_pelicula_por_titulo, obtener_exito_actor,
                    obtener_exito_director, recommender
                    )

app = FastAPI()

    
app.title = "Movie Reccomendation - Machine Learning"
app.version = "1.0 Alfa"

# Configurar middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Url de Bienvenida
@app.get("/", tags=['Home'])
def home():
    return {'message': 'Bienvenido'}

# Vista de cantidad de filmaciones mes
@app.get("/cant_mes/", tags=['Search'])
def cantidad_filmaciones_mes(mes:str):
    peliculas = obtener_cantidad_peliculas_por_mes(mes)
    return peliculas

# Vista de cantidad de filmaciones dia
@app.get("/cant_dia/", tags=['Search'])
def cantidad_filmaciones_dia(dia:str):
    peliculas = obtener_cantidad_peliculas_por_dia(dia)
    return peliculas

# Vista de cantidad de filmaciones por score titulo
@app.get("/score_titulo/", tags=['Search'])
def score_titulo(titulo_de_la_filmación:str):
    pelicula = consultar_pelicula_por_score(titulo_de_la_filmación)
    return pelicula

# Vista de cantidad de filmaciones mes
@app.get("/votos_titulo/", tags=['Search'])
def votos_titulo(titulo_de_la_filmación:str):
    pelicula = consultar_pelicula_por_titulo(titulo_de_la_filmación)
    return pelicula

# Vista de cantidad de filmaciones mes
@app.get("/get_actor/", tags=['Search'])
def get_actor(nombre_actor:str):
    actor = obtener_exito_actor(nombre_actor)
    return actor

# Vista de cantidad de filmaciones mes
@app.get("/get_director/", tags=['Search'])
def get_director(nombre_director:str):
    director = obtener_exito_director(nombre_director)
    return director

# Recomendar peliculas
@app.get("/recommender/", tags=['Search'])
def recomendacion(titulo:str):
    titulo = titulo.lower()
    recomendacion = recommender(titulo)
    return recomendacion
