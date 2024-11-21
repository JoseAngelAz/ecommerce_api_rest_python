class Usuarios():
    def __init__(self, usuario_id, nombre, correo, contrasena, fecha_registro) -> None:
        self.id = usuario_id
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena
        self.fecha_registro = fecha_registro

    def to_json(self):
        return {
                'id':self.id,
                'nombre':self.nombre,
                'correo':self.correo,
                'contrasena':self.contrasena,
                'fecha_registro':self.fecha_registro
                }
