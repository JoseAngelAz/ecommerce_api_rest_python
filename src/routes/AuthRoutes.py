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

#endpint para autenticar con metodo POST
@main.route('/', methods=['POST'])
def login():
    try:
#hacemos la comprobacion mandando un correo y una contrasena por medio de un json
        correo = request.json['correo']
        contrasena = request.json['contrasena']

#cramos una var _user y la inicializamos con el modelo Usuarios y le pasamos los argumentos q pide
#le pasamos 0 y None para el id y el nombre pues solo nos interesa ingresar bien el correo y contrasena que vengan
#del request
        _user = Usuarios(0,None, correo, contrasena)
#creamos una var authenticated_user y la inicializamos con la respuesta que nos ofrece el metodo del servicio AuthService
#recordemos que este servicio nos devuelve un objeto usuario autenticado(authenticated_user) pero este a su ves nos pide 
#el correo y contrasena para devolver el usuario autenticado, por eso le pasamos como parametro _user, que tiene un id 0
#solo para rellenar y un None para el nombre que no nos interesa en este paso, pero si le pasamos el correo y contrasena
#correctos que nos lee al ejecutar el metodo http put en donde ahi nos pasan por json el "correo":"corre@ggj.com", 
#"contrasena":"password"

        authenticated_user = AuthService.login_user(_user)
        print(authenticated_user)
#comprobamos que el usuario autenticado no este vacio
        if authenticated_user != None:
#con el metodo generar token de la clase Security creamos el token y lo guardamos en la var ecoded_token
            encoded_token = Security.generate_token(authenticated_user)
#retornamos un jsonify con dos objetos, success en True y token que contendra en su valor el token codificado
            return jsonify({'success':True, 'token':encoded_token})
        else:
#Si el usuario no trae las claves de acceso o es vacio devolvera un jason con el mensaje de no autorizado y una respuesta 401
            response = jsonify({'message':'NO AUTORIZADO'})
            return response, 401
    except Exception as ex:
        Logger.add_to_log("error", str(ex))
        Logger.add_to_log("error", traceback.format_exc())
        return jsonify({'message':"ERROR", 'success':False})
