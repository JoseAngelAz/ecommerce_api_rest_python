from flask import Blueprint, jsonify, request
import traceback

#logger
from src.utils.Logger import Logger

main = Blueprint('index_blueprint', __name__)

@main.route('/')
def index():
    try:
        Logger.add_to_log("info", "Index/")
        n = 1
        print(n/0)
    except Exception as e:
        Logger.add_to_log("error", str(e))
        Logger.add_to_log("error", traceback.format_exc())
        response = jsonify({'mensaje': "Error interno del Servidor", 'success': False})
        return response, 500
