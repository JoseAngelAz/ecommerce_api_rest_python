"""Se conecta a la baes de datos para hacer la verificacion del usuario"""
import traceback

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
                cursor.execute('call pa_identificar_usuario_v2(%s, %s)', (user.correo, user.contrasena))
#guardamos en var row lo que cursor encontro de un registro
                row = cursor.fetchone()
#validamos que row no este vacio
                if row != None:
#aqui inicializamos la var para usuario autenticado con la instancia del modelo y le pasamos a los parametros del modelo
#los argumentos que traemos de la consulta sql que vienen en la variable row
                    authenticated_user = Usuarios(int(row[0]), row[1], row[2], row[3])
                    print("usuario autenticado: ",authenticated_user)
#cerramos la conexion a la base de datos
            connection.close()
#retornamos la var para usuario autenticado ya inicializada para que se consuma desde donde sea al ejecutarse esta funcion
            return authenticated_user
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
