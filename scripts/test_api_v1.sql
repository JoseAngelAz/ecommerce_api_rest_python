-- ESTRUCTURA DE TABLAS y PROCEDIMIENTOS ALMACENADOS

CREATE TABLE categorias (
    categoria_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion VARCHAR(255),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE usuarios (
    usuario_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    correo VARCHAR(50) UNIQUE NOT NULL,
    contrasena VARBINARY(255) NOT NULL, -- Usar VARBINARY para contraseñas encriptadas
    rol ENUM('Cliente', 'Admin','Editor') NOT NULL DEFAULT 'Cliente',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE productos (
    producto_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL CHECK (precio > 0), -- Validación: precio debe ser positivo
    stock INT NOT NULL CHECK (stock >= 0), -- Validación: stock no puede ser negativo
    categoria_id INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias(categoria_id) ON DELETE CASCADE
);

CREATE TABLE pedidos (
    pedido_id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('pendiente', 'completado', 'cancelado') DEFAULT 'pendiente',
    total DECIMAL(10, 2) NOT NULL CHECK (total >= 0), -- Validación: total no puede ser negativo
    FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE
);

CREATE TABLE detalles_pedido (
    detalle_id INT PRIMARY KEY AUTO_INCREMENT,
    pedido_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0), -- Validación: cantidad debe ser mayor a 0
    precio_unitario DECIMAL(10, 2) NOT NULL CHECK (precio_unitario > 0), -- Validación: precio_unitario debe ser positivo
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(pedido_id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(producto_id) ON DELETE CASCADE
);
-- TERMINAN LAS TABLAS

-- PROCEDIMIENTOS ALMACENADOS MEJORADOS CREATE
-- Añadimos validación para evitar duplicados y transacciones para cumplir con ACID:
-- SP_Agregar_Usuario
DELIMITER //

CREATE PROCEDURE agregar_usuario (
    IN pNombre VARCHAR(50),
    IN pCorreo VARCHAR(50),
    IN pContrasena VARCHAR(100),
    IN pRol ENUM('Admin','Cliente','Editor')
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK; -- Si ocurre un error, revierte la transacción
    END;

    START TRANSACTION;

    -- Si el rol es NULL o vacío, asigna 'Cliente'
    IF pRol IS NULL OR pRol = '' THEN
        SET pRol = 'Cliente';
    END IF;

    -- Validación de rol
    IF pRol NOT IN ('Admin', 'Cliente','Editor') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Rol no válido.';
    END IF;

    -- Validación de duplicados en el correo
    IF EXISTS (SELECT 1 FROM usuarios WHERE correo = pCorreo) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El correo ya está registrado.';
    END IF;

    -- Inserción del usuario
    -- AES_ENCRYPT(pContrasena, SHA2('B!1w8*NAt1T^%kvhUI*S^_', 512)),
    INSERT INTO usuarios (nombre, correo, contrasena, rol)
    VALUES (
        pNombre,
        pCorreo,
        AES_ENCRYPT(pContrasena, SHA2('B!1w8*NAt1T^%kvhUI*S^_', 512)),
        pRol
    );
    IF ROW_COUNT() = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No se insertó el usuario';
    END IF;

    COMMIT;
END //

DELIMITER ;



-- autenticar usuario
DELIMITER //

CREATE PROCEDURE consultar_usuario(
    IN pCorreo VARCHAR(50), 
    IN pContrasena VARCHAR(100)
)
BEGIN
    -- Consulta al usuario con verificación de correo y contraseña desencriptada
    SELECT *
    FROM usuarios
    WHERE 1 = 1
    AND correo = pCorreo
    AND CAST(AES_DECRYPT(contrasena, SHA2('B!1w8*NAt1T^%kvhUI*S^_', 512))
    AS CHAR(100)) = pContrasena;

    -- Nota: Si no se encuentra el usuario, simplemente no devuelve resultados.
END //

DELIMITER ;

-- MODIFICAR usuario por ID
DELIMITER //

CREATE PROCEDURE modificar_usuario(
    IN p_usuario_id INT,
    IN p_nombre VARCHAR(100),
    IN p_correo VARCHAR(100),
    IN p_contrasena VARCHAR(255),
    IN p_rol VARCHAR(50)
)
BEGIN
    DECLARE v_existe_usuario INT;

    -- Verificar si el usuario existe
    SELECT COUNT(*) INTO v_existe_usuario
    FROM usuarios
    WHERE usuario_id = p_usuario_id;

    IF v_existe_usuario = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El usuario no existe.';
    END IF;

    -- Actualizar los datos del usuario
    UPDATE usuarios
    SET
        nombre = p_nombre,
        correo = p_correo,
        contrasena = AES_ENCRYPT(p_contrasena, SHA2('B!1w8*NAt1T^%kvhUI*S^_', 512)), -- Encriptar usando AES_ENCRYPT
        rol = p_rol
    WHERE usuario_id = p_usuario_id;

    -- Verificar que se haya realizado la actualización
    IF ROW_COUNT() = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No se pudo modificar el usuario. Verifique los datos proporcionados.';
    END IF;
END //

DELIMITER ;


-- ELIMINAR USUARIO POR ID
DELIMITER //

CREATE PROCEDURE eliminar_usuario(IN p_usuario_id INT)
BEGIN
    DELETE FROM usuarios WHERE usuario_id = p_usuario_id;

    -- Verificar si se eliminó algún registro
    IF ROW_COUNT() = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No se encontró el usuario con el ID proporcionado.';
    END IF;
END //

DELIMITER ;


-- Validamos que no se repitan nombres de categorías.
DELIMITER //
CREATE PROCEDURE agregar_categoria(
    IN pNombre VARCHAR(100),
    IN pDescripcion VARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    -- Validación de existencia previa
    IF EXISTS (SELECT 1 FROM categorias WHERE nombre = pNombre) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La categoría ya existe.';
    END IF;

    -- Inserción
    INSERT INTO categorias (nombre, descripcion)
    VALUES (pNombre, pDescripcion);

    COMMIT;
END //
DELIMITER ;

-- Validamos la categoría y otros valores antes de insertar.
DELIMITER //
CREATE PROCEDURE agregar_producto (
    IN pNombre VARCHAR(100),
    IN pDescripcion TEXT,
    IN pPrecio DECIMAL(10, 2),
    IN pStock INT,
    IN pCategoria_id INT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    -- Validación de categoría existente
    IF NOT EXISTS (SELECT 1 FROM categorias WHERE categoria_id = pCategoria_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La categoría no existe.';
    END IF;

    -- Inserción
    INSERT INTO productos (nombre, descripcion, precio, stock, categoria_id)
    VALUES (pNombre, pDescripcion, pPrecio, pStock, pCategoria_id);

    COMMIT;
END //
DELIMITER ;

-- Calculamos el total automáticamente a partir de los detalles del pedido.
DELIMITER //
CREATE PROCEDURE agregar_pedido(
    IN pUsuario_id INT,
    IN pEstado VARCHAR(50)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    -- Validación de estado
    IF pEstado NOT IN ('pendiente', 'completado', 'cancelado') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Estado no válido.';
    END IF;

    -- Validación de usuario existente
    IF NOT EXISTS (SELECT 1 FROM usuarios WHERE usuario_id = pUsuario_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El usuario no existe.';
    END IF;

    -- Inserción del pedido con total inicial 0
    INSERT INTO pedidos (usuario_id, estado, total)
    VALUES (pUsuario_id, pEstado, 0);

    -- Obtener el ID del pedido recién creado
    SET @nuevo_pedido_id = LAST_INSERT_ID();

    -- Calcular el total del pedido sumando los detalles (suponiendo que ya se agregaron)
    UPDATE pedidos
    SET total = (
        SELECT COALESCE(SUM(cantidad * precio_unitario), 0)
        FROM detalles_pedido
        WHERE pedido_id = @nuevo_pedido_id
    )
    WHERE pedido_id = @nuevo_pedido_id;

    COMMIT;
END //
DELIMITER ;


-- Validamos la existencia de productos y pedidos.
DELIMITER //
CREATE PROCEDURE agregar_detalles_pedido(
    IN pPedido_id INT,
    IN pProducto_id INT,
    IN pCantidad INT,
    IN pPrecio_unitario DECIMAL(10, 2)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION 
    BEGIN
        ROLLBACK;
    END;

    START TRANSACTION;

    -- Validación: verificar si el pedido existe
    IF NOT EXISTS (SELECT 1 FROM pedidos WHERE pedido_id = pPedido_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El pedido no existe.';
    END IF;

    -- Validación: verificar si el producto existe
    IF NOT EXISTS (SELECT 1 FROM productos WHERE producto_id = pProducto_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El producto no existe.';
    END IF;

    -- Validación: verificar si hay suficiente stock del producto
    IF (SELECT stock FROM productos WHERE producto_id = pProducto_id) < pCantidad THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Stock insuficiente para el producto.';
    END IF;

    -- Insertar el detalle del pedido
    INSERT INTO detalles_pedido (pedido_id, producto_id, cantidad, precio_unitario)
    VALUES (pPedido_id, pProducto_id, pCantidad, pPrecio_unitario);

    -- Actualizar el stock del producto
    UPDATE productos
    SET stock = stock - pCantidad
    WHERE producto_id = pProducto_id;

    -- Calcular el nuevo total del pedido y actualizarlo
    UPDATE pedidos
    SET total = (
        SELECT COALESCE(SUM(cantidad * precio_unitario), 0)
        FROM detalles_pedido
        WHERE pedido_id = pPedido_id
    )
    WHERE pedido_id = pPedido_id;

    COMMIT;
END //
DELIMITER ;

-- READ TABLAS CON PROCEDIMIENTOS ALMACENADOS
DELIMITER //
-- Metodo para consular todos los usuarios (funciona bien)
CREATE PROCEDURE consultar_usuarios()
BEGIN
    SELECT * FROM usuarios;
END //
DELIMITER ;

DELIMITER //
-- CONSULTAR LAS CATEGORIAS
CREATE PROCEDURE consultar_categorias ()
BEGIN
    SELECT * FROM categorias;
END //
DELIMITER ;
-- CONSULTAR DETALLES DE PEDIDO
DELIMITER //
CREATE PROCEDURE consultar_detalles_pedido()
BEGIN
    SELECT * FROM detalles_pedido;
END //
DELIMITER ;
-- CONSULTAR PRODUCTOS
DELIMITER //
CREATE PROCEDURE consultar_productos ()
BEGIN
    SELECT * FROM productos;
END //
DELIMITER ;

-- CONSULTAR PEDIDOS
DELIMITER //
CREATE PROCEDURE consultar_pedidos ()
BEGIN
    SELECT * FROM pedidos;
END //
DELIMITER ;


-- EJECUCION DE LOS PROCEDIMIENTOS ALMACENADOS

/*
1. Insertar Categorías
Las categorías deben crearse primero porque los productos necesitan
asociarse a una categoría existente.
*/
-- Insertar categorías
CALL agregar_categoria('Electrónica', 'Dispositivos electrónicos y gadgets');
CALL agregar_categoria('Ropa', 'Vestimenta y accesorios');
CALL agregar_categoria('Hogar', 'Artículos para el hogar y decoración');

/*
2. Insertar Usuarios
Los usuarios deben registrarse antes de realizar pedidos. Aquí se incluyen
tanto clientes como un administrador para validar diferentes roles.
*/
-- Insertar usuarios
CALL agregar_usuario('Ada Azucena', 'ada.azucena@email.com', 'azucena',3); -- Editor
CALL agregar_usuario('Angel Azucena', 'angel.azucena@example.com', 'azucena',2); -- Cliente
CALL agregar_usuario('Maria Luna', 'maria.luna@example.com', 'luna',1); -- Cliente
CALL agregar_usuario('Admin', 'admin@email.com', 'admin', 'Admin'); -- Administrador

/*
3. Insertar Productos
Los productos dependen de las categorías ya creadas, por lo que se insertan
después de estas. Se especifica la categoría a la que pertenecen, y 
el stock inicial asegura disponibilidad para realizar pedidos.
*/
-- Insertar productos
CALL agregar_producto('Smartphone', 'Teléfono inteligente de última generación', 699.99, 50, 1); -- Electrónica
CALL agregar_producto('Camisa Casual', 'Camisa de algodón de manga larga', 29.99, 100, 2); -- Ropa
CALL agregar_producto('Sofá de 3 plazas', 'Sofá cómodo de tela', 399.99, 20, 3); -- Hogar
CALL agregar_producto('Laptop', 'Computadora portátil de alto rendimiento', 999.99, 30, 1); -- Electrónica

/*
4. Insertar Pedidos
Los pedidos requieren usuarios ya registrados. En este paso, se crean pedidos
para los usuarios, dejando el total inicial en 0, ya que este se calcula 
automáticamente al agregar los detalles del pedido.
*/
-- Insertar pedidos
CALL agregar_pedido(1, 'pendiente'); -- Pedido de Ada Azucena
CALL agregar_pedido(2, 'completado'); -- Pedido de Angel Azucena
CALL agregar_pedido(3, 'pendiente'); -- Pedido de Maria Luna

/*
5. Insertar Detalles de Pedidos
Los detalles de los pedidos vinculan productos con pedidos existentes.
Durante este proceso, el procedimiento almacenado actualizará automáticamente 
el total de cada pedido y ajustará el stock de los productos.
*/
-- Insertar detalles de pedidos

-- Pedido 1: Smartphone y Camisa Casual
CALL agregar_detalles_pedido(1, 1, 1, 699.99); -- 1 Smartphone para Ada Azucena
CALL agregar_detalles_pedido(1, 2, 2, 29.99);  -- 2 Camisas para Ada Azucena

-- Pedido 2: Sofá de 3 plazas
CALL agregar_detalles_pedido(2, 3, 1, 399.99); -- 1 Sofá para Angel Azucena

-- Pedido 3: Laptop
CALL agregar_detalles_pedido(3, 4, 1, 999.99); -- 1 Laptop para Maria Luna

/*
Para insertar datos iniciales en la base de datos y probar su funcionamiento, es importante seguir un orden lógico que respete las relaciones de las tablas y asegure la consistencia de los datos. Aquí está el plan paso a paso, con explicaciones y las llamadas correspondientes a los procedimientos almacenados:
/*
Resumen del Orden de Ejecución

    Categorías: Son necesarias para los productos.
    Usuarios: Los pedidos dependen de los usuarios.
    Productos: Los detalles del pedido requieren productos con stock disponible.
    Pedidos: Los detalles del pedido necesitan pedidos previamente creados.
    Detalles del Pedido: Actualizan automáticamente los totales y el stock.
*/
/*
Datos Resultantes en la Base de Datos
Después de ejecutar las llamadas anteriores:

    Las categorías, usuarios y productos estarán correctamente registrados.
    Los pedidos tendrán totales actualizados basados en los productos y cantidades solicitados.
    El stock de los productos reflejará las cantidades restantes después de ser descontadas.
*/
/*
Validación de relaciones:

    Intentar insertar un detalle de pedido con un producto inexistente o sin stock suficiente.
    Intentar crear un pedido para un usuario inexistente.

Cálculo del total:

    Verificar que los totales en los pedidos coincidan con la suma de los subtotales de sus detalles.

Transacciones y Reversiones:

Simular errores (por ejemplo, valores inválidos) para comprobar que no se registran cambios parciales en la base de datos.
*/
