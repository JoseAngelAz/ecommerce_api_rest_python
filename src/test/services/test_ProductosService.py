#services
from src.services.ProductosService import ProductosService

def test_conseguir_productos_not_none():
    productos = ProductosService.conseguir_productos()
    assert productos != None

def test_conseguir_productos_has_elements():
    productos = ProductosService.conseguir_productos()
    assert len(productos) > 0

def test_conseguir_productos_check_elements_length():
    productos = ProductosService.conseguir_productos()
    for producto in productos:
        assert len(producto) > 0
