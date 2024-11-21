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
    
    @classmethod
    def generate_token(cls, authenticated_user):
        try:
            payload = {
                    'iat': datetime.datetime.now(tz=cls.tz),
                    'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(minutes=10),
                    'correo': authenticated_user.correo,
                    'contrasena':authenticated_user.contrasena,
                    'roles':['Administrator', 'Editor']
            }
            #retorna token con payload, llave secreta y el tipo de algoritmo a aplicar en el token
            token =  jwt.encode(payload, cls.secret, algorithm="HS256")
            print(payload)
            print("Este es el TOKEN",token)
            return token
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
        
    @classmethod
    def verify_token(cls, headers):
        print("ESTE ES EL HEADER :\n",headers)
        try:
            if 'Authorization' in headers.keys():
                authorization = headers['Authorization']
                encoded_token = authorization.split(" ")[1]
                print(encoded_token)
                #and (encoded_token.count('.') == 2))
                if (len(encoded_token) > 0  ):
                    print("pasasmos el if de len(encoded_token)>0")
                    try:
                        payload = jwt.decode(encoded_token, cls.secret, algorithms=["HS256"])
                        roles = list(payload['roles'])
                        if 'Administrator' in roles:
                            return True
                        return False
                    except (jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
                        return False 
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())

