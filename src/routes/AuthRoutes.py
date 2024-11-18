from flask import Blueprint, request, jsonify
import traceback
#Logger
from src.utils.Logger import Logger
#Models
from src.models.UsuariosModel import Usuarios

from src.utils.Security import Security
#servicios
from src.services.AuthService import AuthService

main = Blueprint('auth_blueprint', __name__)

#endpint para autenticar 
@main.route('/', methods=['POST'])
def login():
    try:
#hacemos la comprobacion mandando un correo y una contrasena por medio de un json
        correo = request.json['correo']
        contrasena = request.json['contrasena']


        _user = Usuarios(0,None, correo, contrasena)
        authenticated_user = AuthService.login_user(_user)

        if authenticated_user != None:
            encoded_token = Security.generate_token(authenticated_user)
            return jsonify({'success':True, 'token':encoded_token})
        else:
            response = jsonify({'message':'NO AUTORIZADO'})
            return response, 401
    except Exception as e:
        return jsonify({'message':"ERROR", 'success':False})
