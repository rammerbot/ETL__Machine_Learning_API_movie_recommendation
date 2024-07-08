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

# Import desde models
from models import engine

#engine = create_engine('sqlite:///data/movies.db')

# Cargar datos a Dataframe.
data = pd.read_sql('machine_learning', engine)

# Descargar recursos necesarios de nltk
# nltk.download('punkt')
# nltk.download('stopwords')

# # Preprocesar texto
# stop_words = set(stopwords.words('english'))

# def preprocess(text):
#     if pd.isna(text):
#         return ""
#     text = text.lower()
#     words = word_tokenize(text)
#     words = [word for word in words if word.isalnum() and word not in stop_words]
#     return ' '.join(words)


# # Definir las columnas a procesar
columns_to_preprocess = ['title', 'production_companies_clean', 'production_countries_clean', 'genres_clean', 'overview', 'name']

# # Aplicar preprocesamiento a cada columna y mantener las palabras procesadas en columnas individuales
# for column in columns_to_preprocess:
#     data[f'processed_{column}'] = data[column].apply(preprocess)


# Vectorizar cada columna procesada usando TF-IDF
tfidf_vectorizers = {}
tfidf_matrices = []

for column in columns_to_preprocess:
    vectorizer = TfidfVectorizer(max_features=31000)
    tfidf_matrix = vectorizer.fit_transform(data[f'processed_{column}'])
    tfidf_vectorizers[column] = vectorizer
    tfidf_matrices.append(tfidf_matrix)

# Combinar todas las matrices TF-IDF en una sola matriz si es necesario
combined_tfidf_matrix = hstack(tfidf_matrices).tocsr() if len(tfidf_matrices) > 1 else tfidf_matrices[0]

# Calcular la similitud del coseno bajo demanda
def calculate_cosine_similarity(idx, matrix):
    return cosine_similarity(matrix[idx], matrix).flatten()

def get_recommendations(title, data, top_n=5):
    if title not in data['title'].values:
        return f"La película '{title}' no se encuentra en la base de datos."
    
    idx = data[data['title'] == title].index[0]
    sim_scores = calculate_cosine_similarity(idx, combined_tfidf_matrix)
    
    sim_scores = list(enumerate(sim_scores))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    sim_scores = sim_scores[1:top_n+1]
    movie_indices = [i[0] for i in sim_scores]
    list_ = []
    for i in data['title'].iloc[movie_indices]:
        list_.append(i)

    return list_
    
 
