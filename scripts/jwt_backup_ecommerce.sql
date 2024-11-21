
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--ESTRUCTURA DE TABLAS

CREATE TABLE Categorias (
    categoria_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Store the Categorias data.';

CREATE TABLE Usuarios (
    usuario_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    contrasena BLOB NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Productos (
    producto_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL,
    categoria_id INT,
    FOREIGN KEY (categoria_id) REFERENCES Categorias(categoria_id)
);

CREATE TABLE Pedidos (
    pedido_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT,
    fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(50) DEFAULT 'pendiente',
    total DECIMAL(10, 2),
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id)
);

CREATE TABLE Detalles_Pedido (
    detalle_id INT PRIMARY KEY AUTO_INCREMENT,
    pedido_id INT,
    producto_id INT,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES Pedidos(pedido_id),
    FOREIGN KEY (producto_id) REFERENCES Productos(producto_id)
);

---- PROCEDIMIENTOS ALMACENADOS

DELIMITER $$

-- Procedimiento para agregar un usuario
CREATE PROCEDURE sp_addUsuario (IN pNombre VARCHAR(100), IN pCorreo VARCHAR(100), IN pContrasena VARCHAR(255))
BEGIN
    INSERT INTO Usuarios (nombre, correo, contrasena)
    VALUES (pNombre, pCorreo, AES_ENCRYPT(pContrasena, SHA2('B!1w8*NAt1T^%kvhUI*S^_', 512)));
END$$


-- Procedimiento para verificar la identidad de un usuario
-- pide CORREO Y CONTRASENA
CREATE PROCEDURE sp_verifyUsuario (IN pCorreo VARCHAR(100), IN pContrasena VARCHAR(255))
BEGIN
    SELECT usuario_id, nombre, correo, fecha_registro
    FROM Usuarios USUARIOS
    WHERE 1 = 1
    AND USUARIOS.correo = pCorreo 
      AND CAST(AES_DECRYPT(USUARIOS.contrasena, SHA2('B!1w8*NAt1T^%kvhUI*S^_', 512)) AS CHAR(255)) = pContrasena;
END$$

-- Procedimiento para listar categorías
CREATE PROCEDURE sp_listCategorias()
BEGIN
    SELECT categoria_id, nombre, descripcion 
    FROM Categorias 
    ORDER BY nombre ASC;
END$$

-- Procedimiento para listar Usuarios
CREATE PROCEDURE sp_listUsuarios()
BEGIN
    SELECT * FROM Usuarios;
END$$


DELIMITER ;
----- FIN DE PROCEDIMIENTOS

-- Volcado de datos

-- Insertar en Categorias
INSERT INTO Categorias (nombre, descripcion) VALUES
('Electrónica', 'Dispositivos electrónicos y gadgets'),
('Ropa', 'Vestimenta y accesorios'),
('Hogar', 'Artículos para el hogar y decoración');

-- Insertar en Usuarios
INSERT INTO Usuarios (nombre, correo, contrasena) VALUES
('Ada Azucena', 'ada.azucena@email.com', 'azucena'),
('Angel Azucena', 'angel.azucena@example.com', 'azucena'),
('Maria Luna', 'maria.luna@example.com', 'luna'),
('Angel', 'angel.luna@example.com', 'azucena');


-- Insertar en Productos
INSERT INTO Productos (nombre, descripcion, precio, stock, categoria_id) VALUES
('Smartphone', 'Teléfono inteligente de última generación', 699.99, 50, 1),
('Camisa Casual', 'Camisa de algodón de manga larga', 29.99, 100, 2),
('Sofá de 3 plazas', 'Sofá cómodo de tela', 399.99, 20, 3);

-- Insertar en Pedidos
INSERT INTO Pedidos (usuario_id, estado, total) VALUES
(1, 'pendiente', 729.98),
(2, 'completado', 29.99);

-- Insertar en Detalles_Pedido
INSERT INTO Detalles_Pedido (pedido_id, producto_id, cantidad, precio_unitario) VALUES
(1, 1, 1, 699.99),
(1, 2, 1, 29.99),
(2, 2, 1, 29.99);

---------------------------------------------------------------------------------------
-- PROCEDIMIENTO ALMACENADO DE PRUEBA PARA CONFIRMAR USUARIO
DELIMITER $$

CREATE PROCEDURE pa_identificar_usuario_v2 (IN pCorreo VARCHAR(100), IN pContrasena VARCHAR(255))
BEGIN
    SELECT usuario_id, nombre, correo, contrasena, fecha_registro
    FROM Usuarios USUARIOS
    WHERE 1 = 1
    AND USUARIOS.correo = pCorreo 
      AND CAST(AES_DECRYPT(USUARIOS.contrasena, SHA2('B!1w8*NAt1T^%kvhUI*S^_', 512)) AS CHAR(255)) = pContrasena;
END$$

DELIMITER;
