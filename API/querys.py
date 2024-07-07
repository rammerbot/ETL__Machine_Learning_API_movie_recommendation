from models import session, Movie, Actor, MovieActor, Director
from datetime import datetime
from sqlalchemy import func, extract
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from ml import get_recommendations, data
from sklearn.metrics.pairwise import cosine_similarity

# Obtener peliculas estrenadas un
def obtener_cantidad_peliculas_por_mes(nombre_mes):

    meses = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
        'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
        'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }
    # Validacion de si el mes esta escrito correctamente.
    if nombre_mes.lower() in meses:
        numero_mes = meses[nombre_mes.lower()]
    else:
        raise HTTPException(status_code=404, detail=f"El nombre del mes '{nombre_mes.capitalize()}' no es válido.")

    # Utilizar extract para extraer el mes en SQLite
    cantidad_peliculas = session.query(func.count(Movie.movie_id)).filter(extract('month', Movie.release_date) == numero_mes).scalar()

    return JSONResponse(content={'message': f'{cantidad_peliculas} cantidad de películas fueron estrenadas en el mes de {nombre_mes.capitalize()}'})


# Obtener la cantidad de peliculas estrenadas un dia de la semana en particular.
def obtener_cantidad_peliculas_por_dia(nombre_dia: str):
    dias = {
        'lunes': 1, 'martes': 2, 'miercoles': 3, 'jueves': 4,
        'viernes': 5, 'sábado': 6, 'domingo': 0
    }

    if nombre_dia.lower() in dias:
        numero_dia = dias[nombre_dia.lower()]
    else:
        raise HTTPException(status_code=404, detail=f"El nombre del día '{nombre_dia.capitalize()}' no es válido.")

    # Utilizar strftime('%w', ...) para obtener el día de la semana en SQLite
    cantidad_peliculas = session.query(func.count(Movie.movie_id)).filter(func.strftime('%w', Movie.release_date) == str(numero_dia)).scalar()

    return JSONResponse(content={'message': f'{cantidad_peliculas} cantidad de películas fueron estrenadas en día {nombre_dia.capitalize()}'})


#Realizar la consulta filtrando por el título de la película
def consultar_pelicula_por_titulo(titulo: str):
    try:
        pelicula = session.query(Movie).filter(Movie.title == titulo.lower()).first()
        
        if pelicula:
            return {
                'titulo': pelicula.title.capitalize(),
                'año_estreno': pelicula.release_year,
                'score': pelicula.vote_average
            }
        else:
            raise HTTPException(status_code=404, detail=f"Película {titulo.capitalize()} no se encuentra en nuestra base de datos")
    except:
        raise HTTPException(status_code=404, detail=f"Película {titulo.capitalize()} no se encuentra en nuestra base de datos")


    

# Realizar la consulta filtrando por el título de la película
def consultar_pelicula_por_titulo(titulo: str):
    pelicula = session.query(Movie).filter(Movie.title == titulo.lower()).first()
    if pelicula:
        if pelicula.vote_count >= 2000:
            return JSONResponse(content={
                'mensaje': f"La película {pelicula.title.capitalize()} fue estrenada en el año {pelicula.release_year}. La misma cuenta con un total de {pelicula.vote_count} valoraciones, con un promedio de {pelicula.vote_average}."})
        else:
            return {
                'mensaje': f"La película {pelicula.title.capitalize()} no cumple con la condición de tener al menos 2000 valoraciones."
            }
    else:
        raise HTTPException(status_code=404, detail=f"Película {titulo.capitalize()} no se encuentra en nuestra base de datos")


# Obtener el exito del actor.
def obtener_exito_actor(nombre:str):
    
    actor = session.query(Actor).filter(Actor.name == nombre.lower()).first()
    if actor:
        # Obtener todas las películas del actor
        actor.movies = session.query(Movie).join(MovieActor).filter(MovieActor.actor_id == actor.actor_id).all()
        
        # Calcular el éxito del actor
        cantidad_pelis = len(actor.movies)
        retorno_total = sum(movie.retorno_de_inversion for movie in actor.movies if movie.retorno_de_inversion is not None)
        promedio_retorno = retorno_total / cantidad_pelis if cantidad_pelis > 0 else 0
        
        # Formatear el mensaje de retorno
        mensaje = f"El actor {actor.name.capitalize()} ha participado en {cantidad_pelis} películas. Ha conseguido un retorno total de {retorno_total:.2f} con un promedio de {promedio_retorno:.2f} por película."
        
        return mensaje
    raise HTTPException(status_code=404, detail=f"El actor {nombre.capitalize()} no se encuentra en nuestra base de datos")


def obtener_exito_director(nombre: str):
    # Buscar al director por nombre
    director = session.query(Director).filter(Director.name == nombre.lower()).first()
    
    if not director:
        raise HTTPException(status_code=404, detail="Director no encontrado")

    # Obtener las películas dirigidas por el director
    peliculas = session.query(Movie).filter(Movie.director_id == director.director_id).all()

    if not peliculas:
        raise HTTPException(status_code=404, detail= f'El director {director.name} no ha dirigido ninguna película.')

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


# Sistema de Recomendacion
def recommender(movie: str):
    title = movie
    recommendations = get_recommendations(title.lower(), data)
    return {
        'message': f"Recomendaciones para '{title}':\n",
        'recommendations': recommendations
    }