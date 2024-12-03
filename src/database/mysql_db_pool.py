from decouple import config
from mysql.connector import pooling
from mysql.connector import connect

import pymysql

# Configuración del pool de conexiones


def create_pool_connection():
    """
    Obtiene una conexión desde el pool.
    """
    try:
        db_config = {
                'host':'localhost',
                'user':'root',
                'password':'root',
                'database':'test_api_v1',
                'port':3306
        }
        conexionpool = pooling.MySQLConnectionPool(pool_name = "mi_uno",pool_size = 50, autocommit=True,pool_reset_session=True, **db_config)
        return conexionpool
    except Exception as e:
        print("Error al obtener la conexión:", e)
        raise
