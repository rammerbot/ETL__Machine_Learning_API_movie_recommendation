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

# Vectorizar la columna combinada usando TF-IDF
vectorizer = TfidfVectorizer(max_features=31000)  # Ajusta max_features según tus necesidades
combined_tfidf_matrix = vectorizer.fit_transform(data['combined_text'])

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
    
    return data['title'].iloc[movie_indices]