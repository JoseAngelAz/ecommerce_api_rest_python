from flask import Blueprint, request, jsonify
import traceback
# Modelos
from src.models.UsuariosModel import Usuarios
# Logger
from src.utils.Logger import Logger
# Seguridad
from src.utils.Security import Security
# Servicios
from src.services.UsuariosService import UsuariosService

main = Blueprint('usuarios_blueprint', __name__)

@main.route('/')
def conseguir_usuarios():
    # Verificar token de autorización
    has_access = Security.verify_token(request.headers)
    if not has_access:
        return jsonify({'message': 'NO AUTORIZADO', 'success': False}), 401

    try:
        usuarios = UsuariosService.conseguir_usuarios()
        if usuarios:
            return jsonify({'usuarios': usuarios, 'message': "EXITO", 'success': True}), 200
        else:
            return jsonify({'message': 'NO ENCONTRADO', 'success': False}), 404
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': "ERROR", 'success': False}), 500

#AGREGAR UN USUARIO NUEVO
@main.route('/agregar_usuario', methods=['POST'])
def agregar_usuario():
    print('HEADER DE AGREGAR_USUARIO',request.headers)
    # Verificar token de autorización
    has_access = Security.verify_token(request.headers)
    if not has_access:
        return jsonify({'message': 'NO AUTORIZADO', 'success': False}), 401

    try:
        print("acabamos de entrar en try de usuariosRoute")
        # Validar si el cuerpo de la solicitud es válido
        if not request.json:
            return jsonify({'message': 'Petición inválida: falta cuerpo JSON', 'success': False}), 400
        print("pasamos dentro del try del usuariosRoute")

        # Validar y extraer datos del JSON
        datos_usuario = request.json
        print("datos del usuario insertado: ",datos_usuario)
        campos_requeridos = ['nombre', 'correo', 'contrasena', 'rol']
        for campo in campos_requeridos:
            if campo not in datos_usuario:
                return jsonify({'message': f'Falta el campo: {campo}', 'success': False}), 400
        print("pasamos la validacion de campos del json.request")
        # Crear instancia del usuario
        _new_user = Usuarios(
            usuario_id=0,
            nombre=datos_usuario['nombre'],
            correo=datos_usuario['correo'],
            contrasena=datos_usuario['contrasena'],
            rol=datos_usuario['rol'],
            fecha_registro=None
        )
        print("Usuario recibido del request en la ruta: ", _new_user)

        # Llamar al servicio para agregar el usuario
        added_user = UsuariosService.agregar_usuario(_new_user)
        if added_user is not None:
            return jsonify({'message': 'EXITO', 'success': True, 'usuario': added_user}), 201
        else:
            return jsonify({'message': 'No se guardó el usuario', 'success': False}), 500

    except KeyError as ex:
        return jsonify({'message': f'Falta el campo: {str(ex)}', 'success': False}), 400

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': 'Error interno del servidor', 'success': False}), 500
    
#MODIFICAR USUARIO POR ID
@main.route('/modificar_usuario', methods=['PUT'])
def modificar_usuario():
    print('HEADER DE MODIFICAR_USUARIO', request.headers)
    # Verificar token de autorización
    has_access = Security.verify_token(request.headers)
    if not has_access:
        return jsonify({'message': 'NO AUTORIZADO', 'success': False}), 401

    try:
        # Validar si el cuerpo de la solicitud es válido
        if not request.json:
            return jsonify({'message': 'Petición inválida: falta cuerpo JSON', 'success': False}), 400

        # Extraer datos del JSON
        datos = request.json
        campos_requeridos = ['usuario_id', 'nombre', 'correo', 'contrasena', 'rol']
        for campo in campos_requeridos:
            if campo not in datos:
                return jsonify({'message': f'Falta el campo: {campo}', 'success': False}), 400

        # Crear instancia del usuario
        _user = Usuarios(
            usuario_id=datos['usuario_id'],
            nombre=datos['nombre'],
            correo=datos['correo'],
            contrasena=datos['contrasena'],
            rol=datos['rol'],
            fecha_registro=None  # No se necesita para la modificación
        )
        print("Usuario a modificar:", _user.to_json())

        # Llamar al servicio para modificar el usuario
        result = UsuariosService.modificar_usuario(_user)
        if result is not None:
            return jsonify({'message': 'EXITO', 'success': True}), 200
        else:
            return jsonify({'message': 'No se modificó el usuario', 'success': False}), 500

    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': 'Error interno del servidor', 'success': False}), 500


#ELIMINAR USUARIO POR ID
@main.route('/eliminar_usuario', methods=['DELETE'])
def eliminar_usuario():
    print('HEADER DE ELIMINAR_USUARIO', request.headers)
    # Verificar token de autorización
    has_access = Security.verify_token(request.headers)
    if not has_access:
        return jsonify({'message': 'NO AUTORIZADO', 'success': False}), 401

    try:
        # Validar si el cuerpo de la solicitud es válido
        if not request.json:
            return jsonify({'message': 'Petición inválida: falta cuerpo JSON', 'success': False}), 400

        # Extraer el ID del usuario del cuerpo del request
        datos = request.json
        if 'usuario_id' not in datos:
            return jsonify({'message': 'Falta el campo usuario_id', 'success': False}), 400

        usuario_id = datos['usuario_id']
        print("Este id esta en la ruta: ", usuario_id)

        # Llamar al servicio para eliminar el usuario
        result = UsuariosService.eliminar_usuario(usuario_id)
        if result is not None:
            return jsonify({'message': 'EXITO', 'success': True}), 200
        else:
            return jsonify({'message': 'No se eliminó el usuario', 'success': False}), 500
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message': 'Error interno del servidor', 'success': False}), 500
