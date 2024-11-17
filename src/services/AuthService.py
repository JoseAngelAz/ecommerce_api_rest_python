import traceback

from pymysql import Connection

#database
from src.database.db_mysql import get_connection
#Logger
from src.utils.Logger import Logger
#Models
from src.models.UserModel import User

class AuthService():

    @classmethod
    def login_user(cls,user):
        try:
            connection = get_connection()
            authenticated_user = None
            with connection.cursor() as cursor:
                cursor.execute('sp_verifyUsuario(%s, %s)', (user.correo, user.contrasena))
                row = cursor.fetchone()
                if row != None:
                    authenticated_user = User(int(row[0]), row[1], row[2], row[3])
            connection.close()
            return authenticated_user
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
