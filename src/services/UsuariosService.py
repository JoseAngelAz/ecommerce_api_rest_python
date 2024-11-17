import traceback

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
                cursor.execute('SELECT * FROM Usuarios')
                resultset = cursor.fetchall()
                for row in resultset:
                    usuario = Usuarios(int(row[0]), row[1], row[2], row[3])
                    usuarios.append(usuario.to_json())
            connection.close()
            return usuarios
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
