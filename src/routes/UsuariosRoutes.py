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


@main.route('/agregar_usuario', methods=['POST'])
def agregar_usuario():
    print('HEADER DE AGREGAR_USUARIO',request.headers)
    # Verificar token de autorización
    has_access = Security.verify_token(request.headers)
    if not has_access:
        return jsonify({'message': 'NO AUTORIZADO', 'success': False}), 401

    try:
        print("estamos dentro del try del usuariosRoute")
        # Validar si el cuerpo de la solicitud es válido
        if not request.json:
            return jsonify({'message': 'Petición inválida: falta cuerpo JSON', 'success': False}), 400
        print("pasamos dentro del try del usuariosRoute")

        # Validar y extraer datos del JSON
        datos_usuario = request.json
        campos_requeridos = ['nombre', 'correo', 'contrasena', 'rol']
        for campo in campos_requeridos:
            if campo not in datos_usuario:
                return jsonify({'message': f'Falta el campo: {campo}', 'success': False}), 400

        # Crear instancia del usuario
        _user = Usuarios(
            id=0,
            nombre=datos_usuario['nombre'],
            correo=datos_usuario['correo'],
            contrasena=datos_usuario['contrasena'],
            rol=datos_usuario['rol'],
            fecha_creacion=None
        )
        print("Usuario recibido del request: ", _user)

        # Llamar al servicio para agregar el usuario
        added_user = UsuariosService.agregar_usuario(_user)
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
