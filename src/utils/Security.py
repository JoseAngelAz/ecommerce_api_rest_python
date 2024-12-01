"""Sera usado en AuthRoutes"""
from decouple import config

import datetime
import jwt
import pytz
import traceback

#Logger
from src.utils.Logger import Logger

class Security():

    secret = config('JWT_KEY')
    
    tz = pytz.timezone("America/El_Salvador")
    dt = datetime.datetime.now(tz=tz)
    @classmethod
    def generate_token(cls, authenticated_user):
        try:
            payload = {
                    'iat': cls.dt,
                    'exp': cls.dt + datetime.timedelta(days=7),
                    'correo': authenticated_user.correo,
                    'nombre':authenticated_user.nombre,
                    'rol':authenticated_user.rol
            }
            #retorna token con payload, llave secreta y el tipo de algoritmo a aplicar en el token
            token =  jwt.encode(payload, cls.secret, algorithm="HS256")
            return token
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
        
    @classmethod
    def verify_token(cls, headers):
        try:
            if 'Authorization' in headers.keys():
                authorization = headers['Authorization']
                encoded_token = authorization.split(" ")[1]
                if (len(encoded_token) > 0  and (encoded_token.count('.') == 2)):
                    try:
                        payload = jwt.decode(encoded_token, cls.secret, algorithms=["HS256"])
                        rol = payload['rol']
                        if 'Admin' in rol:
                            return True
                        return False
                    except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                        return False 
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())

