SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--Base de datos jwt_ecommerce

DELIMITER $$
--
-- Procedimientos
--
-- AGREGA USUARIO Y ENCRIPTA LA contrasena
CREATE PROCEDURE `sp_addUsuario` (IN `pUsuarionombre` VARCHAR(20), IN `pContrasena` VARCHAR(20), IN `pEmail` VARCHAR(50))  BEGIN
    INSERT INTO user (nombre, contrasena, email)
    VALUES (pUsuarionombre, AES_ENCRYPT(pContrasena, SHA2('B!1w8*NAt1T^%kvhUI*S^_', 512)), pEmail);
END$$

-- LISTA LOS PRODUCTOS
CREATE PROCEDURE `sp_listProductos` ()  BEGIN
	SELECT LAN.id, LAN.nombre 
    FROM Productos LAN 
    ORDER BY LAN.id ASC;
END$$

-- VERIFICAR IDENTIDAD DEL USUARIO

CREATE PROCEDURE `sp_verifyIdentity` (IN `pUsuarionombre` VARCHAR(20), IN `pContrasena` VARCHAR(20))  BEGIN
	SELECT USER.usuario_id, USER.nombre, USER.email 
	FROM Usuario USER 
    WHERE 1 = 1 
    AND USER.nombre = pUsuarionombre 
	AND CAST(AES_DECRYPT(USER.contrasena, SHA2('B!1w8*NAt1T^%kvhUI*S^_', 512)) AS CHAR(30)) = pContrasena;
END$$
DELIMITER ;
-- --------------------------------------------------------------------

--ESCTRUCTURA PARA LA TABLA PRODUCTOS


CREATE TABLE `Productos` (
  `id` tinyint(2) UNSIGNED NOT NULL,
  `nombre` varchar(20) COLLATE utf8_unicode_ci NOT NULL
  `descripcion` text COLLATE utf8_unicode_ci NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `stock` int NOT NULL,
  `categoria_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Store the Productos data.';

-- volcado de datos para la tabla Productos

INSERT INTO `Productos` (`id`, `nombre`, `descripcion`, `precio`, `stock`, `categoria_id`) VALUES

