#services
from src.services.UsuariosService import UsuariosService

def test_conseguir_usuarios_not_none():
    usuarios = UsuariosService.conseguir_usuarios()
    assert usuarios != None

def test_conseguir_usuarios_has_elements():
    usuarios = UsuariosService.conseguir_usuarios()
    assert len(usuarios) > 0

def test_conseguir_usuarios_check_elements_length():
    usuarios = UsuariosService.conseguir_usuarios()
    for usuario in usuarios:
        assert len(usuario) > 0
