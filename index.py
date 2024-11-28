from config import config
from src import init_app

configuration = config['development']
app = init_app(configuration)

if __name__ == "__main__":
    ssl_context = (configuration.SSL_CERT,
                    configuration.SSL_KEY)
    port = (configuration.PORT)
    host = (configuration.HOST)
    app.run(ssl_context=ssl_context, host=host, port=port)
