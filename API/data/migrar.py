import pandas as pd
from sqlalchemy import create_engine

# Configuración de la conexión a MySQL
mysql_engine = create_engine('mysql+pymysql://root:root@localhost/movies')

# Configuración de la conexión a SQLite
sqlite_engine = create_engine('sqlite:///movies.db')

# Obtener los nombres de las tablas en la base de datos MySQL
tables = pd.read_sql("SHOW TABLES", mysql_engine).values.flatten()

# Transferir cada tabla a la base de datos SQLite
for table in tables:
    print(f"Transfiriendo tabla {table}...")
    # Leer los datos de la tabla en MySQL
    df = pd.read_sql(f'SELECT * FROM {table}', mysql_engine)
    
    # Verificar si la tabla contiene datos
    if not df.empty:
        print(f"La tabla {table} contiene {len(df)} registros.")
        # Escribir los datos en la base de datos SQLite
        df.to_sql(table, sqlite_engine, if_exists='replace', index=False)
        print(f"Tabla {table} transferida con éxito.")
    else:
        print(f"La tabla {table} está vacía y no se transferirá.")

df = pd.read_sql('SELECT * FROM movie LIMIT 10', sqlite_engine)
print(df)