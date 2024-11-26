"""Se conecta a la baes de datos para hacer la verificacion del usuario"""
import traceback
from datetime import datetime
#databases
from src.database.db_mysql import get_connection
#Logger
from src.utils.Logger import Logger
#Models
from src.models.UsuariosModel import Usuarios

class AuthService():

    @classmethod
    def login_user(cls,user):
        try:
            connection = get_connection()
            authenticated_user = None
            with connection.cursor() as cursor:
                cursor.execute('call consultar_usuario(%s, %s)', (user.correo, user.contrasena))
                row = cursor.fetchone()
                if row != None:
                    fecha_registro = row[5].strftime('%Y-%m-%d %H:%M:%S') if isinstance(row[5], datetime) else None
                    authenticated_user = Usuarios(int(row[0]), row[1], row[2], None,row[4],fecha_registro)
                    print("El usuario autenticado: ",dir(authenticated_user))
            connection.close()
            return authenticated_user
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
