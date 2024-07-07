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
nltk.download('punkt')
nltk.download('stopwords')


# Mostrar las primeras filas del DataFrame
print(data.head())

# Preprocesar texto
stop_words = set(stopwords.words('english'))

def preprocess(text):
    if pd.isna(text):
        return ""
    text = text.lower()
    words = word_tokenize(text)
    words = [word for word in words if word.isalnum() and word not in stop_words]
    return ' '.join(words)

# Aplicar preprocesamiento a las columnas relevantes
columns_to_preprocess = ['title', 'production_companies_clean', 'production_countries_clean', 'genres_clean', 'overview', 'name']
for column in columns_to_preprocess:
    data[f'processed_{column}'] = data[column].apply(preprocess)

# Vectorizar las columnas preprocesadas usando TF-IDF
tfidf_vectorizers = {}
tfidf_matrices = []
for column in columns_to_preprocess:
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(data[f'processed_{column}'])
    tfidf_vectorizers[column] = vectorizer
    tfidf_matrices.append(tfidf_matrix)

# Combinar todas las matrices TF-IDF en una sola matriz

combined_tfidf_matrix = hstack(tfidf_matrices)

# Calcular la similitud del coseno entre las películas
cosine_similarities = cosine_similarity(combined_tfidf_matrix, combined_tfidf_matrix)

def get_recommendations(title, cosine_similarities, data, top_n=5):
    # Verificar si el título existe en el DataFrame
    if title not in data['title'].values:
        return f"La película '{title}' no se encuentra en la base de datos."
    
    # Encontrar el índice de la película dada
    idx = data[data['title'] == title].index[0]
    
    # Obtener las similitudes de la película dada con todas las demás películas
    sim_scores = list(enumerate(cosine_similarities[idx]))
    
    # Ordenar las películas por similitud y seleccionar las más similares
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Obtener los índices de las películas más similares
    sim_scores = sim_scores[1:top_n+1]
    movie_indices = [i[0] for i in sim_scores]
    
    # Devolver los títulos de las películas recomendadas
    return data['title'].iloc[movie_indices]