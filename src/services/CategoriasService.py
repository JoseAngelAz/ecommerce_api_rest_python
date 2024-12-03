import traceback
from datetime import datetime

from src.utils.Logger import Logger

from src.models.CategoriasModel import Categorias
from src.database.mysql_db_pool import create_pool_connection

class CategoriasService():
    @classmethod
    def consultar_categorias(cls):
        try:
            connection = create_pool_connection()
            if not connection:
                raise Exception("No se pudo conectar a la base de datos.")
            
            categorias = []
            with connection.cursor() as cursor:
                cursor.execute('call consultar_categorias()')
                resulset = cursor.fetchall()
                print(resulset)
                for row in resulset:
                    fecha_creacion = row[3].strftime('%Y-%m-%d %H:%M:%S') if isinstance(row[3], datetime) else None
                    categoria = Categorias(int(row[0]),row[1],row[2],fecha_creacion)
                    categorias.append(categoria.categorias_to_json())
            connection.close()
            return categorias
        except Exception as e:
            Logger.add_to_log("error",str(e))
            Logger.add_to_log("error", traceback.format_exc())