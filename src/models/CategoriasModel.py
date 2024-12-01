class Categorias():
    def __init__(self,categoria_id,nombre,descripcion,fecha_creacion) -> None:
        self.categoria_id = categoria_id
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_creacion = fecha_creacion

    def categorias_to_json(self):
        return {
            'categoria_id':self.categoria_id,
            'nombre':self.nombre,
            'descripcion':self.descripcion,
            'fecha_creacion':self.fecha_creacion
        }