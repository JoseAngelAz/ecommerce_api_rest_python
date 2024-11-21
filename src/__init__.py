from flask import Flask 

#Routes
from .routes import AuthRoutes, IndexRoutes, UsuariosRoutes, ProductosRoutes, PedidosRoutes,UserRoutes

app = Flask(__name__)

def init_app(config):
    #configuration
    app.config.from_object(config)

    #Blueprints
    app.register_blueprint(IndexRoutes.main, url_prefix='/')
    app.register_blueprint(AuthRoutes.main, url_prefix='/auth')
    app.register_blueprint(ProductosRoutes.main, url_prefix='/productos')
    app.register_blueprint(UsuariosRoutes.main, url_prefix='/usuarios')
    app.register_blueprint(PedidosRoutes.main, url_prefix='/pedidos')
    app.register_blueprint(UserRoutes.main, url_prefix='/user')
    return app
