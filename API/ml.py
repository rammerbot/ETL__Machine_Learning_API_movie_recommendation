# Importaciones de sklearn para el modelo de recomendacion.
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from scipy.sparse import hstack

# importar sqlalchemy.
from sqlalchemy import create_engine

# importar pandas.
import pandas as pd

# Import desde models.
from models import engine

#engine = create_engine('sqlite:///data/movies.db')

# Cargar datos a Dataframe.
data = pd.read_sql('machine_learning', engine)

'''Las lineas comentadas a contiuacion pertenecen al preprocesamiento de los
datos, la intencion es realizarlo una vez y guardar los datos, de esta manera se
asegura que el consumo de recursos no sera afectado cada vez que se inicie el servidor'''
# Descargar recursos necesarios de nltk.
# nltk.download('punkt')
# nltk.download('stopwords')

# # Preprocesar texto.
# stop_words = set(stopwords.words('english'))

# def preprocess(text):
#     if pd.isna(text):
#         return ""
#     text = text.lower()
#     words = word_tokenize(text)
#     words = [word for word in words if word.isalnum() and word not in stop_words]
#     return ' '.join(words)

# # Definir las columnas a procesar.
columnas_a_procesar = ['title', 'production_companies_clean', 'production_countries_clean', 'genres_clean', 'overview', 'name']

# # Aplicar preprocesamiento a cada columna y mantener las palabras procesadas en columnas individuales.
# for column in columns_to_preprocess:
#     data[f'processed_{column}'] = data[column].apply(preprocess)

## Guardar en base de datos.
# data.to_sql('machine_learning', engine, if_exists='replace')

# Vectorizar cada columna procesada usando TF-IDF.
dic_vectorizadores = {}
list_matrices = []

# Vectorizar los datos con Tfid.
for column in columnas_a_procesar:
    vectorizer = TfidfVectorizer(max_features=31000)
    matrizado = vectorizer.fit_transform(data[f'processed_{column}'])
    dic_vectorizadores[column] = vectorizer
    list_matrices.append(matrizado)

# Combinar todas las matrices TF-IDF en una sola matriz si es necesario.
combinacion_matrices = hstack(list_matrices).tocsr() if len(list_matrices) > 1 else list_matrices[0]

# Calcular la similitud del coseno bajo demanda.
def calcular_similitud_coseno(indice_x, matrix):
    return cosine_similarity(matrix[indice_x], matrix).flatten()

# Obtener recomendacion.
def get_recommendations(title, data, top_n=5):
    if title not in data['title'].values:
        return f"La película '{title}' no se encuentra en la base de datos."
    
    indice_x = data[data['title'] == title].index[0]
    resultados = calcular_similitud_coseno(indice_x, combinacion_matrices)
    
    resultados = list(enumerate(resultados))
    resultados = sorted(resultados, key=lambda x: x[1], reverse=True)
    
    resultados = resultados[1:top_n+1]
    movie_indices = [i[0] for i in resultados]
    return data['title'].iloc[movie_indices].tolist()

   
    
 
