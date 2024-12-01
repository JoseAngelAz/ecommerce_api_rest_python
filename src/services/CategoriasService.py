import traceback
from datetime import datetime

from src.utils.Logger import Logger

from src.models.CategoriasModel import Categorias
from src.database.ejemploPoolConexion import get_pool_alchemy

class CategoriasService():
    @classmethod
    def consultar_categorias(cls):
        try:
            conexion = get_pool_alchemy()
            categorias = []
            with conexion as cursor:
                cursor.execute('SELECT * FROM categorias')
                resulset = cursor.fetchall()
                print(resulset)
                for row in resulset:
                    fecha_creacion = row[3].strftime('%Y-%m-%d %H:%M:%S') if isinstance(row[3], datetime) else None
                    categoria = Categorias(int(row[0]),row[1],row[2],fecha_creacion)
                    categorias.append(categoria.categorias_to_json())
            conexion.close()
            return categorias
        except Exception as e:
            Logger.add_to_log("error",str(e))
            Logger.add_to_log("error", traceback.format_exc())