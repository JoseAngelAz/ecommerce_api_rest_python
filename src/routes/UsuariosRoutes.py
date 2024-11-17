from flask import Blueprint, request, jsonify

import traceback

#Logger
from src.utils.Logger import Logger
#security
from src.utils.Security import Security
#services
from src.services.UsuariosService import UsuariosService

main = Blueprint('usuarios_blueprint', __name__)

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
