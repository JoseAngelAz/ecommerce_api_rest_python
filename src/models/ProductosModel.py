class Productos():
    """docstring for Productos."""
    def __init__(self, id, nombre, descripcion, precio, stock, categoria_id) -> None:
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.categoria_id = categoria_id

    def to_json(self):
        return {
                'id': self.id,
                'nombre':self.nombre,
                'descripcion':self.descripcion,
                'precio':self.precio,
                'stock':self.stock,
                'categoria_id':self.categoria_id
                }
        
        
