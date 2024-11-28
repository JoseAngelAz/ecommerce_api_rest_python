from datetime import datetime
import traceback

# Database
from src.database.db_mysql import get_connection
# Logger
from src.utils.Logger import Logger
# Models
from src.models.UsuariosModel import Usuarios

class UsuariosService:

#CONSULTAR TODOS LOS USUARIOS (FUNCIONA)
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

#CONSULTAR USUARIO POR ID (FUNCIONA)
    @classmethod
    def consultar_usuario_por_id(cls, usuario_id):
        """
        Consulta un usuario por su ID.
        """
        try:
            connection = get_connection()
            if not connection:
                raise Exception("No se pudo conectar a la base de datos.")

            with connection.cursor() as cursor:
                # Llama al procedimiento almacenado para consultar el usuario por ID
                cursor.callproc('consultar_usuario_por_id', (usuario_id,))
                resultset = cursor.fetchone()

                if resultset:
                    # Construye el modelo de usuario desde los resultados
                    fecha_registro = resultset[5].strftime('%Y-%m-%d %H:%M:%S') if isinstance(resultset[5], datetime) else None
                    usuario = Usuarios(
                        int(resultset[0]),  # usuario_id
                        resultset[1],       # nombre
                        resultset[2],       # correo
                        None,               # contrasena (opcional ocultar en respuestas)
                        resultset[4],       # rol
                        fecha_registro      # fecha_registro
                    )
                    return usuario.to_json()  # Retorna en formato JSON
                else:
                    return None  # Usuario no encontrado

        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return None
        finally:
            if 'connection' in locals() and connection:
                connection.close()


#AGREGAR UN USUARIO NUEVO (# LANZA ERROR PERO SI INSERTA EL REGISTRO)
    @classmethod
    def agregar_usuario(cls, user):
        try:
            connection = get_connection()
            if not connection:
                raise Exception("No se pudo conectar a la base de datos.")
            
            #usuario_nuevo = Usuarios(0, user.nombre, user.correo, user.contrasena, user.rol, None)
            with connection.cursor() as cursor:
                print("el user que viene al servicio: ",user)
                cursor.callproc('agregar_usuario', (user.nombre, user.correo, user.contrasena, user.rol))
                # Confirmar si el procedimiento tuvo éxito
                if cursor.rowcount == 0:
                    print("el cursor rowcount: ",cursor.rowcount)
                    raise Exception("El procedimiento no insertó el usuario.")
            
            connection.commit()
            return {'message': "Usuario Agregado"}
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return None
        finally:
            if 'connection' in locals() and connection:
                connection.close()

#MODIFICAR UN USUARIO POR ID (FUNCIONA)
    @classmethod
    def modificar_usuario(cls, user):
        try:
            print("Estamos en el SERVICIO :este es el user que viene del route:", user.to_json())
            connection = get_connection()
            if not connection:
                raise Exception("No se pudo conectar a la base de datos.")

            with connection.cursor() as cursor:
                cursor.callproc('modificar_usuario', (
                    user.usuario_id,
                    user.nombre,
                    user.correo,
                    user.contrasena,
                    user.rol
                ))
                # Confirmar si el procedimiento tuvo éxito
                if cursor.rowcount == 0:
                    raise Exception("No se modificó el usuario. Verifique el ID proporcionado.")
            
            connection.commit()
            return {'message': "Usuario Modificado"}
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return None
        finally:
            if 'connection' in locals() and connection:
                connection.close()

#ELIMINAR USUARIO POR ID (FUNCIONA)
    @classmethod
    def eliminar_usuario(cls, usuario_id):
        print("Este es el id que viene al servicio", usuario_id)
        try:
            connection = get_connection()
            if not connection:
                raise Exception("No se pudo conectar a la base de datos.")

            with connection.cursor() as cursor:
                cursor.callproc('eliminar_usuario', (usuario_id,))
                # Confirmar si el procedimiento tuvo éxito
                if cursor.rowcount == 0:
                    raise Exception("No se encontró el usuario para eliminar o no se eliminó correctamente.")
            
            connection.commit()
            return {'message': "Usuario eliminado"}
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return None
        finally:
            if 'connection' in locals() and connection:
                connection.close()