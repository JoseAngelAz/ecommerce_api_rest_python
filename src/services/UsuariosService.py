from datetime import datetime
import traceback

# Database
from src.database.db_mysql import get_connection
# Logger
from src.utils.Logger import Logger
# Models
from src.models.UsuariosModel import Usuarios

class UsuariosService:

    @classmethod
    def conseguir_usuarios(cls):
        try:
            connection = get_connection()
            if not connection:
                raise Exception("No se pudo conectar a la base de datos.")
            
            usuarios = []
            with connection.cursor() as cursor:
                cursor.execute('call consultar_usuarios()')
                resultset = cursor.fetchall()
                for row in resultset:
                    fecha_registro = row[5].strftime('%Y-%m-%d %H:%M:%S') if isinstance(row[5], datetime) else None
                    usuario = Usuarios(int(row[0]), row[1], row[2], str(row[3]), row[4], fecha_registro)
                    usuarios.append(usuario.to_json())
            return usuarios
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return None
        finally:
            if 'connection' in locals() and connection:
                connection.close()

    @classmethod
    def agregar_usuario(cls, user):
        try:
            connection = get_connection()
            if not connection:
                raise Exception("No se pudo conectar a la base de datos.")
            
            usuario_nuevo = Usuarios(0, user.nombre, user.correo, user.contrasena, user.rol, None)
            with connection.cursor() as cursor:
                cursor.execute('call agregar_usuario(%s, %s, %s, %s)', 
                               (user.nombre, user.correo, user.contrasena, user.rol))
                # Confirmar si el procedimiento tuvo éxito
                if cursor.rowcount == 0:
                    raise Exception("El procedimiento no insertó el usuario.")
            
            connection.commit()
            return {'message': "Usuario Agregado", 'usuario': usuario_nuevo.to_json()}
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return None
        finally:
            if 'connection' in locals() and connection:
                connection.close()
