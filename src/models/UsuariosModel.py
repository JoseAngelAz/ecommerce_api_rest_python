class Usuarios():
    def __init__(self, usuario_id, nombre, correo, contrasena, rol, fecha_registro) -> None:
        self.id = usuario_id
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena
        self.rol = rol
        self.fecha_registro = fecha_registro

    def to_json(self):
        return {
                'usuario_id':self.id,
                'nombre':self.nombre,
                'correo':self.correo,
                'contrasena':self.contrasena,
                'rol':self.rol,
                'fecha_registro':self.fecha_registro
                }
