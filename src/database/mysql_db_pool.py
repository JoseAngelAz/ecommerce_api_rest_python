from decouple import config
from dbutils.pooled_db import PooledDB
import pymysql

# Configuración del pool de conexiones
pool = PooledDB(
    creator=pymysql,  # Conector de base de datos
    maxconnections=10,  # Máximo número de conexiones en el pool
    mincached=2,       # Conexiones abiertas que se mantienen en espera
    maxcached=5,       # Máximo número de conexiones en caché
    blocking=True,     # Esperar conexiones disponibles en caso de saturación
    host=config('MYSQL_HOST'),
    user=config('MYSQL_USER'),
    password=config('MYSQL_PASSWORD'),
    database=config('MYSQL_DB'),
)

def pool_util_connection():
    """
    Obtiene una conexión desde el pool.
    """
    try:
        return pool.connection()
    except Exception as e:
        print("Error al obtener la conexión:", e)
        raise
