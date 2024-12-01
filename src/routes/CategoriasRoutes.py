from flask import Blueprint, request, jsonify
import traceback
from src.utils.Logger import Logger
from src.utils.Security import Security

from src.services.CategoriasService import CategoriasService

main = Blueprint('categorias_blueprint',__name__)

@main.route('/')
def consultar_categorias():
    try:
        categorias = CategoriasService.consultar_categorias()
        if (len(categorias)>0):
            return jsonify({'categorias': categorias, 'message':'EXITO','success':True})
        else:
            return jsonify({'message':"CATEGORIAS NO ENCONTRADAS",'success':True})
        
    except Exception as e:
        Logger.add_to_log("error",str(e))
        Logger.add_to_log("error",traceback.format_exc())