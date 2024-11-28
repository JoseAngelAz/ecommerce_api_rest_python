from decouple import config

class Config():
    SECRET_KEY = config('SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = True
    SSL_CERT = config('SSL_CERT', default='certs/cert.pem')
    SSL_KEY = config('SSL_KEY', default='certs/key.pem')
    PORT = config('PORT')
    HOST = config('HOST')
config = {
        'development': DevelopmentConfig,
        
}
