from flask import Flask, jsonify

#Routes
from .routes import AuthRoutes, IndexRoutes, UsuariosRoutes, ProductosRoutes, PedidosRoutes,UserRoutes,agregar_userRoute,CategoriasRoutes

app = Flask(__name__)

def init_app(config):
    #configuration
    app.config.from_object(config)

    #endponts
    app.register_blueprint(IndexRoutes.main, url_prefix='/')
    #Consultar tablas
    app.register_blueprint(AuthRoutes.main, url_prefix='/auth')
    app.register_blueprint(ProductosRoutes.main, url_prefix='/productos')
    app.register_blueprint(UsuariosRoutes.main, url_prefix='/usuarios')
    app.register_blueprint(PedidosRoutes.main, url_prefix='/pedidos')
    app.register_blueprint(UserRoutes.main, url_prefix='/user')
    #Insertar en tablas
    app.register_blueprint(agregar_userRoute.main, url_prefix='/add_user')
    #categorias
    app.register_blueprint(CategoriasRoutes.main, url_prefix='/categorias')
    #manejo de errores
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Solicitud inválida. Verifica los datos enviados."}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Recurso no encontrado."}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"error": "Error interno del servidor. Inténtalo más tarde."}), 500


    return app
