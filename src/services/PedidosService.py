import traceback
import datetime

#importar la conexion de la config de la base de datos
from src.database.db_mysql import get_connection
#de logger importar logger para crear los logs
from src.utils.Logger import Logger
#importar el modelo de Pedidos
from src.models.PedidosModel import Pedidos


class PedidosService():
    @classmethod
    def conseguir_Pedidos(cls):
        try:
            connection = get_connection()
            pedidos = []
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM Pedidos')
                resulset = cursor.fetchall()
                for row in resulset:
                    pedido = Pedidos(int(row[0]),int(row[1]),datetime.datetime(row[2]),row[3],float(row[4]))
                    pedidos.append(pedido.Pedido_Model_to_json())
            connection.close()
            return pedidos
        except Exception as e:
            Logger.add_to_log("error",str(e))
            Logger.add_to_log("erro", traceback.format_exc())