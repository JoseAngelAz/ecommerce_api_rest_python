DELIMITER //
-- INSERTAR USUARIO CON LA CONTRASENA ENCRIPTADA (funciona)
CREATE PROCEDURE agregar_usuario (IN pNombre VARCHAR(20), IN pCorreo VARCHAR(20), IN pContrasena VARCHAR(20) )
BEGIN
    INSERT INTO Usuarios(nombre, correo, contrasena)
    VALUES (pNombre, pCorreo, AES_ENCRYPT(pContrasena,
    SHA2('B!1w8*NAt1T^%kvhUI*S^_',512)));
END //


-- VERIFICAR IDENTIDAD DEL USUARIO (si funciona)
CREATE PROCEDURE verificar_usuario (IN pCorreo VARCHAR(20), IN pContrasena VARCHAR(20))
BEGIN
    SELECT *
    FROM Usuarios 
    where 1=1
    AND correo = pCorreo
    AND CAST(AES_DECRYPT(contrasena,SHA2('B!1w8*NAt1T^%kvhUI*S^_', 512))
    AS CHAR(30)) = pContrasena;
END //

-- Metodo para consular todos los usuarios (funciona bien)
CREATE PROCEDURE consultar_usuarios()
BEGIN
    SELECT * FROM Usuarios;
END //

-- CONSULTAR LAS CATEGORIAS
CREATE PROCEDURE consultar_categorias ()
BEGIN
    SELECT * FROM Categorias;
END //

-- CONSULTAR DETALLES DE PEDIDOS
CREATE PROCEDURE consultar_detalles_pedidos ()
BEGIN
    SELECT * FROM Detalles_Pedido;
END //

-- CONSULTAR TODOS LOS PEDIDOS
CREATE PROCEDURE consultar_pedidos ()
BEGIN
    SELECT * FROM Pedidos;
END //

-- CONSULTAR TODOS LOS PRODUCTOS
CREATE PROCEDURE consultar_productos ()
BEGIN
    SELECT * FROM Productos;
END //

DELIMITER ;
