-- Productos
DELIMITER //
CREATE PROCEDURE sp_listProductos()
BEGIN
  SELECT LAN.producto_id, LAN.nombre
    FROM Productos LAN
    ORDER BY LAN.producto_id ASC;
END //

--Usuarios

DELIMITER //
CREATE PROCEDURE sp_addUser(IN pNombre VARCHAR(20), IN pPassword VARCHAR(20), IN pFullname VARCHAR(50))
BEGIN
    INSERT INTO user (username, password, fullname)
    VALUES (pUsername, AES_ENCRYPT(pPassword, SHA2('B!1w8*NAt1T^%kvhUI*S^_', 512)), pFullname);
END //
DELIMITER ;


