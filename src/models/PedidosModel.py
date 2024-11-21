class Pedidos():
    """Modelo de los pedidos"""
    def __init__(self, pedido_id, usuario_id, fecha_pedido, estado, total) -> None:
        self.pedido_id = pedido_id
        self.usuario_id = usuario_id
        self.fecha_pedido = fecha_pedido
        self.estado = estado
        self.total = total

    def Pedido_Model_to_json(self):
        return {
            'pedido_id':self.pedido_id,
            'usuario_id':self.usuario_id,
            'fecha_pedido':self.fecha_pedido,
            'estado':self.estado,
            'total':self.total
        }