from models import session, Movie, Actor, MovieActor, Director
from datetime import datetime
from sqlalchemy import func
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

def prueba():
    movies = session.query(Movie).limit(5).all()
    titulo = []
    for i in movies:
        titulo.append(i.original_title)
    return titulo


# cantidad de peliculas por mes
def obtener_cantidad_peliculas_por_mes(nombre_mes: str):
    # Diccionario para convertir nombres de meses en español a números de mes
    
    meses = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
        'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
        'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }
    
    # Convertir el nombre del mes en español a número de mes
    if nombre_mes.lower() in meses:
        numero_mes = meses[nombre_mes.lower()]
    else:
        return HTTPException(status_code=404,detail=f"El nombre del mes '{nombre_mes}' no es válido.")
    # Consulta para obtener la cantidad de películas estrenadas en un mes específico
    cantidad_peliculas = session.query(func.count(Movie.movie_id)).filter(func.month(Movie.release_date) == numero_mes).scalar()
    return JSONResponse(content={'message': f'{cantidad_peliculas} cantidad de películas fueron estrenadas en el mes de {nombre_mes}'})


# Cantidad de peliculas por dia de la semana.
def obtener_cantidad_peliculas_por_dia(nombre_dia: str):
    # Diccionario para convertir nombres de días en español a números de día de la semana (1=lunes, 7=domingo)
    dias = {
        'lunes': 2, 'martes': 3, 'miércoles': 4, 'jueves': 5,
        'viernes': 6, 'sábado': 7, 'domingo': 1
    }
    
    # Convertir el nombre del día en español a número de día de la semana
    if nombre_dia.lower() in dias:
        numero_dia = dias[nombre_dia.lower()]
    else:
        return HTTPException(status_code=404,detail=f"El nombre del dia '{nombre_dia}' no es válido.")
    # Consulta para obtener la cantidad de películas estrenadas en un día específico de la semana
    cantidad_peliculas = session.query(func.count(Movie.movie_id)).filter(func.DAYOFWEEK(Movie.release_date) == numero_dia).scalar()
    
    return JSONResponse(content={'message': f'{cantidad_peliculas} cantidad de películas fueron estrenadas en los dias {nombre_dia}s'})

# Realizar la consulta filtrando por el título de la película
def consultar_pelicula_por_titulo(titulo: str):
    try:
        pelicula = session.query(Movie).filter(Movie.title == titulo).first()
        
        if pelicula:
            return {
                'titulo': pelicula.title,
                'año_estreno': pelicula.release_year,
                'score': pelicula.vote_average
            }
        else:
            return HTTPException(status_code=404, detail=f"Película {titulo} no se encuentra en nuestra base de datos")
    except:
        return HTTPException(status_code=404, detail=f"Película {titulo} no se encuentra en nuestra base de datos")
    
# Realizar la consulta filtrando por el título de la película
def consultar_pelicula_por_titulo(titulo: str):
    pelicula = session.query(Movie).filter(Movie.title == titulo).first()
    if pelicula:
        if pelicula.vote_count >= 2000:
            return JSONResponse(content={
                'mensaje': f"La película {pelicula.title} fue estrenada en el año {pelicula.release_year}. La misma cuenta con un total de {pelicula.vote_count} valoraciones, con un promedio de {pelicula.vote_average}."})
        else:
            return {
                'mensaje': f"La película {pelicula.title} no cumple con la condición de tener al menos 2000 valoraciones."
            }
    else:
        raise HTTPException(status_code=404, detail=f"Película {titulo} no se encuentra en nuestra base de datos")
    
# Relizar consulta de las peliculas donde ha trabajado un actor.
def obtener_exito_actor(nombre: str):
    # Buscar al actor por nombre
    actor = session.query(Actor).filter(Actor.name == nombre).first()
    
    if not actor:
        raise HTTPException(status_code=404, detail=f"Actor {nombre} no encontrado")

    # Obtener las películas en las que ha participado el actor
    peliculas = session.query(Movie).join(MovieActor, Movie.movie_id == MovieActor.movie_id).filter(MovieActor.actor_id == actor.actor_id).all()

    if not peliculas:
        return JSONResponse(content={
            'mensaje': f"El actor {actor.name} no ha participado en ninguna película."
        })

    cantidad_peliculas = len(peliculas)
    retorno_total = sum(pelicula.retorno_de_inversion for pelicula in peliculas)
    promedio_retorno = retorno_total / cantidad_peliculas if cantidad_peliculas > 0 else 0

    return JSONResponse(content={
        'mensaje': f"El actor {actor.name} ha participado de {cantidad_peliculas} cantidad de filmaciones, el mismo ha conseguido un retorno de {retorno_total} con un promedio de {promedio_retorno} por filmación."
    })


def obtener_exito_director(nombre: str):
    # Buscar al director por nombre
    director = session.query(Director).filter(Director.name == nombre).first()
    
    if not director:
        raise HTTPException(status_code=404, detail="Director no encontrado")

    # Obtener las películas dirigidas por el director
    peliculas = session.query(Movie).filter(Movie.director_id == director.director_id).all()

    if not peliculas:
        return {
            'mensaje': f"El director {director.name} no ha dirigido ninguna película."
        }

    cantidad_peliculas = len(peliculas)
    retorno_total = sum(pelicula.retorno_de_inversion for pelicula in peliculas)
    promedio_retorno = retorno_total / cantidad_peliculas if cantidad_peliculas > 0 else 0

    detalles_peliculas = []
    for pelicula in peliculas:
        detalles_peliculas.append({
            'titulo': pelicula.title,
            'fecha_lanzamiento': pelicula.release_year,
            'retorno_individual': pelicula.retorno_de_inversion,
            'costo': pelicula.budget,
            'ganancia': pelicula.revenue
        })

    return {
        'mensaje': f"El director {director.name} ha dirigido {cantidad_peliculas} filmaciones, consiguiendo un retorno total de {retorno_total} con un promedio de {promedio_retorno} por filmación.",
        'detalles_peliculas': detalles_peliculas
    }

