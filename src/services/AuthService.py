"""Se conecta a la baes de datos para hacer la verificacion del usuario"""
from pprint import pprint
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
        #intentamos una coneccion
        try:
            connection = get_connection()
#creamos una var de usuario autenticado inicializado en None para luego llenarlo y devolverlo al final
            authenticated_user = None
#del metodo cursor lo renombramos como cursor para usarlo despues
            with connection.cursor() as cursor:
#ejecutamos la sentencia sql embebida o un procedimiento almacenado en este caso y le pasamos los params que pide el PROCALMACENADO
#Procedimiento almacenado funcionando bien.
                cursor.execute('call verificar_usuario(%s, %s)', (user.correo, user.contrasena))
#guardamos en var row lo que cursor encontro de un registro
                row = cursor.fetchone()
                print("Este es el ROW",row)
#validamos que row no este vacio
                if row != None:
#aqui inicializamos la var para usuario autenticado con la instancia del modelo y le pasamos a los parametros del modelo
#los argumentos que traemos de la consulta sql que vienen en la variable row
# Convertir row[4] (fecha_registro) a formato ISO 8601 o cualquier otro formato
                    fecha_registro = row[4].strftime('%Y-%m-%d %H:%M:%S') if isinstance(row[4], datetime) else None
                    authenticated_user = Usuarios(int(row[0]), row[1], row[2], None, fecha_registro)
                    print("El usuario autenticado: ",dir(authenticated_user))
#cerramos la conexion a la base de datos
            connection.close()
#retornamos la var para usuario autenticado ya inicializada para que se consuma desde donde sea al ejecutarse esta funcion
            return authenticated_user
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
