class User():
    def __init__(self,usuario_id, nombre, correo, contrasena) -> None:
        self.usuario_id = usuario_id
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena

    def to_json(self):
        return {
                'usuario_id': self.usuario_id,
                'nombre':self.nombre,
                'correo':self.correo,
                'contrasena':self.contrasena
        }
