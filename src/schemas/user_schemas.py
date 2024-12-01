# schemas/user_schemas.py
from marshmallow import Schema, fields, validates, ValidationError

class ConsultarUsuarioSchema(Schema): #FUNCIONA
    """Esquema para validar el cuerpo de la solicitud de consultar un usuario por ID."""
    usuario_id = fields.Int(required=True, error_messages={
        "required": "El campo 'usuario_id' es obligatorio.",
        "invalid": "El 'usuario_id' debe ser un número entero."
    })


class AgregarUsuarioSchema(Schema): #FUNCIONA
    """Esquema para validar el cuerpo de la solicitud de agregar un nuevo usuario."""
    nombre = fields.Str(required=True, error_messages={"required": "El campo 'nombre' es obligatorio."})
    correo = fields.Email(required=True, error_messages={
        "required": "El campo 'correo' es obligatorio.",
        "invalid": "El 'correo' debe ser un email válido."
    })
    contrasena = fields.Str(required=True, error_messages={"required": "El campo 'contrasena' es obligatorio."})
    rol = fields.Raw(required=True, error_messages={"required": "El campo 'rol' es obligatorio."})
    @validates("rol")
    def validate_rol(self, value):
        if not isinstance(value, (str, int)):
            raise ValidationError("El campo 'rol' debe ser de tipo string o integer.")

class ModificarUsuarioSchema(Schema):
    """Esquema para validar el cuerpo de la solicitud de modificar un usuario."""
    usuario_id = fields.Int(required=True, error_messages={
        "required": "El campo 'usuario_id' es obligatorio.",
        "invalid": "El 'usuario_id' debe ser un número entero."
    })
    nombre = fields.Str(required=True, error_messages={"required": "El campo 'nombre' es obligatorio."})
    correo = fields.Email(required=True, error_messages={
        "required": "El campo 'correo' es obligatorio.",
        "invalid": "El 'correo' debe ser un email válido."
    })
    contrasena = fields.Str(required=True, error_messages={"required": "El campo 'contrasena' es obligatorio."})
    rol = fields.Str(required=True, error_messages={"required": "El campo 'rol' es obligatorio."})


class EliminarUsuarioSchema(Schema):
    """Esquema para validar el cuerpo de la solicitud de eliminar un usuario."""
    usuario_id = fields.Int(required=True, error_messages={
        "required": "El campo 'usuario_id' es obligatorio.",
        "invalid": "El 'usuario_id' debe ser un número entero."
    })
