import traceback
from datetime import datetime
#database
from src.database.db_mysql import get_connection
#Logger 
from src.utils.Logger import Logger
#Models
from src.models.ProductosModel import Productos

class ProductosService():
    @classmethod
    def conseguir_productos(cls):
        try:
            connection = get_connection()
            productos = []
            with connection.cursor() as cursor:
                cursor.execute('call consultar_productos()')
                resultset = cursor.fetchall()
                for row in resultset:
                    fecha_registro = row[6].strftime('%Y-%m-%d %H:%M:%S') if isinstance(row[6], datetime) else None
                    producto = Productos(int(row[0]),row[1],row[2],float(row[3]),int(row[4]),int(row[5]),fecha_registro)
                    productos.append(producto.to_json())
            connection.close()
            return productos
        except Exception as e:
            Logger.add_to_log("error",str(e))
            Logger.add_to_log("error", traceback.format_exc())
