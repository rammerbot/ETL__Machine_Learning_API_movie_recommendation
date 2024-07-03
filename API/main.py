from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

app.title = "Movie Reccomendation - Machine Learning"
app.version = "1.0 Alfa"

# Url de Bienvenida
@app.get("/", tags=['Home'])
def home():

    return {'message': 'Welcome'}

# Vista de cantidad de filmaciones mes
@app.get("/cant_mes/", tags=['Search'])
def cantidad_filmaciones_mes(mes:str):
    return {'message': f'{211} cantidad de películas fueron estrenadas en el mes de {122}'}

# Vista de cantidad de filmaciones dia
@app.get("/cant_dia/", tags=['Search'])
def cantidad_filmaciones_dia(dia:str):
    return {'message': f'{211} cantidad de películas fueron estrenadas en los dias {122}'}

# Vista de cantidad de filmaciones por score titulo
@app.get("/score_titulo/", tags=['Search'])
def score_titulo(movie:str):
    return {'message': f' La película {212} fue estrenada en el año X con un score/popularidad de {121}'}

# Vista de cantidad de filmaciones mes
@app.get("/votos_titulo/", tags=['Search'])
def votos_titulo(movie:str):
    return {'message': f'La película {111} fue estrenada en el año X. La misma cuenta con un total de {222} valoraciones, con un promedio de {333}'}

# Vista de cantidad de filmaciones mes
@app.get("/get_actor/", tags=['Search'])
def get_actor(actor:str):
    return {'message': f'Ejemplo de retorno: El actor {33} ha participado de {32} cantidad de filmaciones, el mismo ha conseguido un retorno de {31} con un promedio de {13} por filmación'}

# Vista de cantidad de filmaciones mes
@app.get("/get_director/", tags=['Search'])
def get_director(director:str):
    return {'message': f'{211} cantidad de películas fueron estrenadas en el mes de {122}'}