import traceback
from datetime import datetime

#databse
from src.database.db_mysql import get_connection
#Logger
from src.utils.Logger import Logger
#Models
from src.models.UsuariosModel import Usuarios

class UsuariosService():
    @classmethod
    def conseguir_usuarios(cls):
        try:
            connection = get_connection()
            usuarios = []
            with connection.cursor() as cursor:
                cursor.execute('call consultar_usuarios()')
                resultset = cursor.fetchall()
                for row in resultset:
                    # Convertir row[5] (fecha_registro) a formato ISO 8601 o cualquier otro formato
                    fecha_registro = row[5].strftime('%Y-%m-%d %H:%M:%S') if isinstance(row[5], datetime) else None
                    usuario = Usuarios(int(row[0]), row[1], row[2], str(row[3]),row[4],fecha_registro)
                    #mostrar en consola los usuarios
                    usuarios.append(usuario.to_json())
            connection.close()
            return usuarios
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
