from flask import Blueprint, request, jsonify

import traceback

#Logger
from src.utils.Logger import Logger
#security
from src.utils.Security import Security
#services
from src.services.ProductosService import ProductosService

main = Blueprint('productos_blueprint', __name__)

@main.route('/')
def conseguir_productos():
    has_access = Security.verify_token(request.headers)
    if has_access:
        try:
            productos = ProductosService.conseguir_productos()
            if (len(productos)>0):
                return jsonify({'productos': productos,'message':'EXITO', 'success':True})

            else:
                return jsonify({'message':"NO ENCONTRADO", 'success': True})
        except Exception as e:
            Logger.add_to_log("error", str(e))
            Logger.add_to_log("error", traceback.format_exc())
            return jsonify({'message':"ERROR", 'success': False})
    else:
        response = jsonify({'message': 'NO AUTORIZADO'})
        return response, 401

