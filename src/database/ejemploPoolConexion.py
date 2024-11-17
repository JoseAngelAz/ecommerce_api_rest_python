
from DBUtils.PooledDB import PooledDB
import pymysql

# Configuración del pool de conexiones
pool = PooledDB(
    creator=pymysql,  # Módulo de la base de datos a usar
    maxconnections=10,  # Número máximo de conexiones abiertas
    mincached=2,  # Número mínimo de conexiones a mantener abiertas en el pool
    maxcached=5,  # Número máximo de conexiones a mantener en cache
    blocking=True,  # Si True, espera si no hay conexiones disponibles
    host='localhost',  # Dirección del servidor MySQL
    user='tu_usuario',  # Usuario de la base de datos
    password='tu_contraseña',  # Contraseña del usuario
    database='tu_base_de_datos',  # Nombre de la base de datos
    charset='utf8mb4'  # Codificación de caracteres
)

# Obtener una conexión del pool
connection = pool.connection()

try:
    with connection.cursor() as cursor:
        # Ejecutar una consulta de ejemplo
        cursor.execute("SELECT VERSION()")
        result = cursor.fetchone()
        print("Versión de MySQL:", result[0])
finally:
    # Liberar la conexión de vuelta al pool
    connection.close()
