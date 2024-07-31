# Proyecto Machine Learning Operatios - Modelos de Recomendacion de Peliculas

<p align="center">
  <img src="https://github.com/rammerbot/ETL__Machine_Learning_API_movie_recommendation/assets/123994694/0a4786e1-228a-49d5-be08-439598fa4fe0" alt="Imagen 1" style="width:200px; height:200px; margin:10px;">
  <img src="https://github.com/rammerbot/ETL__Machine_Learning_API_movie_recommendation/assets/123994694/030cdb40-685c-45c7-981c-36ba4ac446db" alt="Imagen 2" style="width:200px; height:200px; margin:10px;">
</p>

-------

## Introduccion:
Este proyecto tiene como objetivo la implementacion de un sistema de recomendación de películas utilizando técnicas de vectorización de texto y similitud del coseno de machine learning. 
<br>
El proyecto abarca desde la limpieza de datos (ETL), creación de una API con FastAPI, análisis estadístico de los datos (EDA), creación y entrenamiento del modelo acorde a las exigencias y despliegue del mismo en la plataforma de render.

---

## Tabla de Contenidos
- Descripcion del Proyecto
- Sintesis de la Carga y Transformación (ETL) de los Datos
- Creación de la API con FastAPI
- Sintesis del Análisis Estadístico de Datos (EDA) Aplicado
- Explicacion del Modelo de Recomendación
- Conclusión
- Requisitos Previos
- Instalación


------------
## Descripcion del proyecto

Para el siguiente proyecto se requirio la implementacion de un modelo de recomendacion de peliculas utilizando <strong>Machine Learning</strong>, contando con 2 archivos de formato csv <strong>(movies_dataset.csv y credits.csv)</strong> con aproximadamente 45.000 filas de datos en brutos por cada data set, la tarea principal de dicho proyecto se basa hacer uso de diferentes tipos de herramientas para realizar la limpieza y preparacion de los datos <strong>(ETL)</strong>  para ser consultados mediante una API y obtener a traves de ella diferentes detalles sobre las peliculas, sus directores y quienes actuaron en ella. 
<br>
Tambien se requiere realizar un <strong>Analisis Estadistico de los Datos (EDA) </strong>para ser usado por el departamente de Analitycs con el fin de seleccionar, entrenar e implementar correctamente el modelo a utilizar.

A continuacion se explica de manera sencilla como fue el proceso de elaboracion y como descargar para probar o implementar el modelo resultado.

---

## Sintesis de la Carga y Transformación (ETL) de los Datos

En el archivo <strong>ETL_EDA/ETL.ipynb</strong> del repositoriose se puede observar a mayor detalle los pasos referenciados en esta parte.
<br>
Originalmente se han recibido dos archivos en formato csv que contenian los datos para el proyecto, sin embargo dichos datos se encontraban en bruto, es decir, no estaban normalizados o con un formato adecuado para trabajar, para ello se procedio a aplicar diferentes tecnicas y herramientas para transformar y acceder a los datos y de este modo extraer solo los necesarios para el proyecto,  asi como tambien eliminar columnas que no aportarian algun tipo de relevancia al proyecto como tal. Se realizo valuacion y eliminacion de duplicados, eliminacion o reemplazo de nulos segun sea pertinente, creacion de tablas nuevas y carga a una base de datos tipo sql para poder crear relaciones entre las tablas tener una consulta mas eficiente.
![image](https://github.com/rammerbot/ETL__Machine_Learning_API_movie_recommendation/assets/123994694/8a9bccfb-8c36-4f19-8b26-5f04b7e160b2)
![image](https://github.com/rammerbot/ETL__Machine_Learning_API_movie_recommendation/assets/123994694/1dfb00ff-a814-46d3-bd16-7555961a08a0)
![image](https://github.com/rammerbot/ETL__Machine_Learning_API_movie_recommendation/assets/123994694/bceff1b5-bac0-4bdb-9099-6be7893248e8)




---
## Creación de la API con FastAPI

En la carpeta del proyecto <strong>API</strong> se puede observar a mayor detalle los pasos referenciados en esta parte.
<br>
Se procede a la creacion de la API con la libreria FastAPI, utilizando los datos previamente procesados  y guardado en una base de datos, en el paso del ETL, esta api se conecta a la base de datos usando la libreria de <strong>sqlalchemy</strong> para poder hacer consultas directamente.
Se configuraron 6 endpoints que representan las consultas a realizarse:

- peliculas por mes.
- peliculas por dia.
- score de pelicula.
- votacion de pelicula.
- consulta de actor.
- consulta de director.

  ![image](https://github.com/rammerbot/ETL__Machine_Learning_API_movie_recommendation/assets/123994694/12dcda0d-9b92-45a3-bf1d-11639bb88b06)


Una vez culminada la construccion de la API se procede a realizar un Deploy en Render.
<br>
API en render: [API_machine_learning](http://etl-machine-learning-api-movie.onrender.com/docs "API_machine_learning")
![image](https://github.com/rammerbot/ETL__Machine_Learning_API_movie_recommendation/assets/123994694/b3651ff4-ce85-45d9-a633-e2ccbdba1577)


Adicionalmente se agrego un FrontEnd para visualizarla de manera mas dinamica y agradabe:
<br>
API_Front : [Front](http://movies-ght7.onrender.com/ "Front")
![image](https://github.com/rammerbot/ETL__Machine_Learning_API_movie_recommendation/assets/123994694/2eb99b8a-e34c-46ec-bea3-cd84b07732c2)


---
## Sintesis del Análisis Estadístico de Datos (EDA) Aplicado

En el archivo <strong>ETL_EDA/EDA.ipynb</strong> del repositorio se puede observar a mayor detalle los pasos referenciados en esta parte.
<br>
Previamente en el paso del ETL se habia realizado un adelanto de las operaciones de limpieza y normalizacion de los datos, en este punto se pretende dar un enfoque a los datos mas orientado hacia modelo de machine learning a realizar, como por ejemplo evaluar los datos numericos y ver que importancia aportan a nuestro modelo de recomendacion, realizar nubes de palabras y analizar sus patrones, en base a esto elegir las columnas adecuadas para crear una tabla de tados preprocesados que se usaran posteriormente en el modelo.
![image](https://github.com/rammerbot/ETL__Machine_Learning_API_movie_recommendation/assets/123994694/766025cc-f904-4a13-a489-207f4c6df442)
![image](https://github.com/rammerbot/ETL__Machine_Learning_API_movie_recommendation/assets/123994694/98d59280-174d-481d-a885-b80e621c88e2)


---

## Explicacion del Modelo de Recomendación

Para el modelo de recomendacion se decidio usar <strong>TfidfVectorizer</strong> para vectorizar y <strong>cosine_similarity</strong> para las recomendaciones usando los datos preprocesados previamente en el paso EDA.
<br>
El codigo puede encontrarse en el modulo <strong>mi.py</strong> dentro de la  carpeta <strong>/API</strong>.
<br>
para la ejecucion del codigo se realizo una actualizacion la API creada previamente. Se configuro el modulo de modo que al iniciar el servidor de la Api se entrena automaticamente el modelo y a traves de un endpoint se llama a una funcion que realiza la consulta al modelo arrojando las 5 peliculas con mayor grado de similitud en un orden descendente segun el nivel de coincidencia.
![image](https://github.com/rammerbot/ETL__Machine_Learning_API_movie_recommendation/assets/123994694/57aad9ee-bebb-48cd-9762-97a599f2a59d)
![image](https://github.com/rammerbot/ETL__Machine_Learning_API_movie_recommendation/assets/123994694/b7ba5a35-72bd-4ce9-b77d-609f03f9d967)



---

## Conclusión
<strong>El proyecto de Machine Learning Operations - Modelos de Recomendación de Películas</strong>  ha sido un reto de amplio espectro pues abarca múltiples aspectos esenciales dentro del area de la programacion en Datas Science. A través de este proyecto, se ha implementado un sistema robusto utilizando técnicas avanzadas de vectorización de texto (TF-IDF) y similitud del coseno para proporcionar recomendaciones precisas de películas.
<br>
Este proyecto no solo cumple con los objetivos iniciales de desarrollar un sistema de recomendación de películas, sino que también establece una base sólida para futuras expansiones y mejoras.
<br>
La implementación de una API y su despliegue en la nube aseguran la escalabilidad y accesibilidad del sistema. Además, la metodología utilizada para el ETL, EDA y la construcción del modelo puede ser adaptada y mejorada para incorporar datos adicionales o técnicas más avanzadas en el futuro.
En resumen,  este el proyecto Machine Learning  ha sido un éxitoso ya que cuenta con un sistema funcional y eficaz que puede ser utilizado tanto por desarrolladores como por analistas para obtener recomendaciones de películas basadas en datos procesados y analizados de manera rigurosa.

---

Requisitos Previos
Antes de iniciar, asegúrate de tener instalados los siguientes software:

- Git
- Python 3.8+
- pip (gestor de paquetes de Python)
###### librerias de Python
- pandas
- nltk
- sklearn
- scipy
- fastapi
- sqlalchemy
- pymysql


## Instalación

> Clona el repositorio:

```
git clone https://github.com/rammerbot/ETL__Machine_Learning_API_movie_recommendation.git
```

> instalar librerias

```python
pip install -r requirements.txt
```

> ejecutar main.py

```python
uviconr main:app --reload
```


## Autor:
Rammer Gomez
 ### Contacto:
[LinkedIn](https://www.linkedin.com/in/rammer-gomez/)
