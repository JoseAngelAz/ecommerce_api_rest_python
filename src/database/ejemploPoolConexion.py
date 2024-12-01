from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from decouple import config

# Crear el motor de SQLAlchemy con un pool de conexiones
engine = create_engine(
    f"mysql+pymysql://{config('MYSQL_USER')}:{config('MYSQL_PASSWORD')}@{config('MYSQL_HOST')}/{config('MYSQL_DB')}",
    poolclass=QueuePool,  # Clase para manejar el pool
    pool_size=10,         # Número máximo de conexiones
    max_overflow=5,       # Conexiones adicionales permitidas sobre el límite
    pool_timeout=30,      # Tiempo máximo de espera para obtener una conexión
    pool_recycle=280,     # Tiempo máximo de vida de una conexión (en segundos)
    echo=False            # Cambiar a True para habilitar logs SQL en consola
)

def get_pool_alchemy():
    """
    Obtiene una conexión desde el pool configurado.
    """
    try:
        connection = engine.connect()  # Obtiene una conexión del pool
        return connection
    except Exception as e:
        print("Error al obtener la conexión:", e)
        raise
