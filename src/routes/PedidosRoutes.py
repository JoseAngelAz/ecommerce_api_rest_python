from flask import Blueprint, request, jsonify
import traceback
from src.utils.Logger import Logger
from src.utils.Security import Security

from src.services.PedidosService import PedidosService

main = Blueprint('pedidos_blueprint', __name__)

@main.route('/')
def conseguir_pedidos():
    try: 
        pedidos = PedidosService.conseguir_Pedidos()
        if (len(pedidos)>0):
            return jsonify({'pedidos':pedidos,'message':'EXITO','success':True})
        else:
            return jsonify({'message':"PEDIDOS NO ENCONTRADOS",'success':True})
    
    except Exception as e:
        Logger.add_to_log("error",str(e))
        Logger.add_to_log("error",traceback.format_exc())
