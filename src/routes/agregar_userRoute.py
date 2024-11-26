from flask import Blueprint, request, jsonify

import traceback
#user
from src.models.UserModel import User
#Logger
from src.utils.Logger import Logger
#security
from src.utils.Security import Security
#services
from src.services.UsuariosService import UsuariosService

main = Blueprint('add_user_blueprint', __name__)

@main.route('/')
def conseguir_usuarios():
    has_access = Security.verify_token(request.headers)#aqui ira en bearertoken en el encabezado

    if has_access:
        try:
            usuarios = UsuariosService.conseguir_usuarios()
            if (len(usuarios)>0):
                return jsonify({'usuarios': usuarios, 'message':"EXITO",'success':True})
            else:
                return jsonify({'mensaje':'NO ENCONTRADO', 'success':True})
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return jsonify({'message':"ERROR", 'success':False})
    else:
        response = jsonify({'message':'NO AUTORIZADO'})
        return response, 401

@main.route('/agregar_user', methods=['POST'])
def agregar_user():
        #has_access = Security.verify_token(request.headers)
   
        nombre = request.json['nombre']
        correo = request.json['correo']
        contrasena = request.json['contrasena']
        rol = request.json['rol']
        _user = User(0,nombre, correo, contrasena,rol,)
        print("auth routes: ",_user)

        added_user = UsuariosService.agregar_usuario(_user)
        if added_user != None:
            return jsonify({'success':True, 'usuario':added_user})
        else:
            response = jsonify({'message':'NO SE GUARDO EL USUARIO'})
            return response, 401
    
