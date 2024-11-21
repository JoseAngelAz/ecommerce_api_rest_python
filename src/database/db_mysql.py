from decouple import config
import pymysql

#metodo que retorna una tupla con los datos para la db
def get_connection():
    try:
        return pymysql.connect(
                host=config('MYSQL_HOST'),
                user=config('MYSQL_USER'),
                password=config('MYSQL_PASSWORD'),
                db=config'MYSQL_DB'
                )
    except Exception as e:
        print(e)
