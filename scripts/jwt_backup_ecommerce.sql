
-- ESTRUCTURA DE TABLAS

CREATE TABLE categorias (
    categoria_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Store the categorias data.';

CREATE TABLE usuarios (
    usuario_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    correo VARCHAR(50) UNIQUE NOT NULL,
    contrasena BLOB NOT NULL,
    rol VARCHAR(50) NOT NULL DEFAULT 'Cliente',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE productos (
    producto_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL,
    categoria_id INT NOT NULL,
    FOREIGN KEY (categoria_id) REFERENCES categorias(categoria_id)
);

CREATE TABLE pedidos (
    pedido_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT,
    fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(50) DEFAULT 'pendiente',
    total DECIMAL(10, 2),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id)
);

CREATE TABLE detalles_pedido (
    detalle_id INT PRIMARY KEY AUTO_INCREMENT,
    pedido_id INT,
    producto_id INT,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(pedido_id),
    FOREIGN KEY (producto_id) REFERENCES productos(producto_id)
);

--   -------------------------------------------------------------------------------------
-- PROCEDIMIENTOS ALMACENADOS PARA AGREGAR Y CONSULTAR
DELIMITER //
-- INSERTAR USUARIO CON LA CONTRASENA ENCRIPTADA (funciona)
CREATE PROCEDURE agregar_usuario (IN pNombre VARCHAR(50), IN pCorreo VARCHAR(50), IN pContrasena VARCHAR(100), IN pRol VARCHAR(50) DEFAULT NULL)
BEGIN
-- Si pRol es NULL, asigna un valor predeterminado
    IF pRol IS NULL THEN
        SET pRol = 'Cliente'; -- Valor predeterminado, como 'Cliente'
    END IF;
-- comienza la insercion
    INSERT INTO usuarios(nombre, correo, contrasena,rol)
    VALUES (pNombre, pCorreo, AES_ENCRYPT(pContrasena,
    SHA2('B!1w8*NAt1T^%kvhUI*S^_',512)),pRol);
END //


-- VERIFICAR IDENTIDAD DEL USUARIO (si funciona)
CREATE PROCEDURE verificar_usuario (IN pCorreo VARCHAR(50), IN pContrasena VARCHAR(20))
BEGIN
    SELECT *
    FROM usuarios 
    where 1=1
    AND correo = pCorreo
    AND CAST(AES_DECRYPT(contrasena,SHA2('B!1w8*NAt1T^%kvhUI*S^_', 512))
    AS CHAR(30)) = pContrasena;
END //

-- Metodo para consular todos los usuarios (funciona bien)
CREATE PROCEDURE consultar_usuarios()
BEGIN
    SELECT * FROM usuarios;
END //
DELIMITER ;

-- PROCEDIMIENTOS PARA CATEGORIAS
DELIMITER //
CREATE PROCEDURE agregar_categoria(pNombre VARCHAR(20),pDescripcion VARCHAR(255))
BEGIN 
  INSERT INTO categorias(nombre,descripcion) VALUES (pNombre,pDescripcion);
END //


-- CONSULTAR LAS CATEGORIAS
CREATE PROCEDURE consultar_categorias ()
BEGIN
    SELECT * FROM categorias;
END //
DELIMITER ;

-- CONSULTAR DETALLES DE PEDIDOS
DELIMITER //
CREATE PROCEDURE agregar_detalles_pedido(
        pPedido_id INT,
        pProducto_id INT,
        pCantidad INT,
        pPrecio_unitario DECIMAL(10,2))
BEGIN
      INSERT INTO detalles_pedido(
      pedido_id,
      producto_id,
      cantidad,
      precio_unitario)
      VALUES(
      pPedido_id,
      pProducto_id,
      pCantidad,
      pPrecio_unitario 
    );
END //


CREATE PROCEDURE consultar_detalles_pedido()
BEGIN
    SELECT * FROM detalles_pedido;
END //
DELIMITER ;

-- PROCEDIMIENTOS PARA LOS PEDIDOS
DELIMITER //
CREATE PROCEDURE agregar_pedido(pUsuario_id INT,pEstado VARCHAR(50),pTotal DECIMAL(10,2))
BEGIN
      INSERT INTO pedidos(usuario_id,estado,total) 
      VALUES (pUsuario_id,pEstado,pTotal);
END //

CREATE PROCEDURE consultar_pedidos ()
BEGIN
    SELECT * FROM pedidos;
END //
DELIMITER ;

-- PROCEDIMIENTOS PARA PRODUCTOS
DELIMITER //
CREATE PROCEDURE agregar_producto (
pNombre VARCHAR(100),
pDescripcion TEXT,
pPrecio DECIMAL(10,2),
pStock INT,
pCategoria_id INT
)
BEGIN
    INSERT INTO productos (nombre,descripcion,precio,stock,categoria_id) 
    VALUES (
      pNombre,
      pDescripcion,
      pPrecio,
      pStock,
      pCategoria_id
    );
END //

CREATE PROCEDURE consultar_productos ()
BEGIN
    SELECT * FROM productos;
END //

DELIMITER ;

-- ------------------------------------------------------------------------------
-- insertar usuarios por el procedimiento almacenado
CALL agregar_usuario('Ada Azucena', 'ada.azucena@email.com', 'azucena');
CALL agregar_usuario('Angel Azucena', 'angel.azucena@example.com', 'azucena');
CALL agregar_usuario('Maria Luna', 'maria.luna@example.com', 'luna');
CALL agregar_usuario('Angel', 'angel@email.com', 'azucena','Admin');
-- Insertar categorias por el procedimiento almacenado nombre, descripcion
CALL agregar_categoria( 'Electrónica', 'Dispositivos electrónicos y gadgets');
CALL agregar_categoria( 'Ropa', 'Vestimenta y accesorios');
CALL agregar_categoria( 'Hogar', 'Artículos para el hogar y decoración');
-- Insertar Productos por el procedimiento almacenado
-- nombre, descripcion, precio, stock, categoria
CALL agregar_producto( 'Smartphone', 'Teléfono inteligente de última generación', 699.99, 50, 1);
CALL agregar_producto( 'Camisa Casual', 'Camisa de algodón de manga larga', 29.99, 100, 2);
CALL agregar_producto( 'Sofá de 3 plazas', 'Sofá cómodo de tela', 399.99, 20, 3);
-- insertar pedido usuario_id, estado, total
CALL agregar_pedido( 1, 'pendiente', 699.99);
CALL agregar_pedido( 2, 'completado', 29.99);
CALL agregar_pedido( 3, 'quien sabe', 399.99);

-- pide: pedido_id, producto, cantidad, precio_unitario
CALL agregar_detalles_pedido( 1, 1, 1, 699.99);
CALL agregar_detalles_pedido( 1, 2, 1, 29.99);
CALL agregar_detalles_pedido( 2, 2, 1, 29.99);
-- ----------------------------------------------------------------------------

