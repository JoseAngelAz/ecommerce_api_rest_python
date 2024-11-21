-- MySQL dump 10.13  Distrib 8.4.3, for Linux (x86_64)
--
-- Host: localhost    Database: ecommerce
-- ------------------------------------------------------
-- Server version	8.4.3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping data for table `Categorias`
--

LOCK TABLES `Categorias` WRITE;
/*!40000 ALTER TABLE `Categorias` DISABLE KEYS */;
INSERT INTO `Categorias` VALUES (1,'Electrónica','Dispositivos electrónicos y gadgets'),(2,'Ropa','Vestimenta y accesorios'),(3,'Hogar','Artículos para el hogar y decoración');
/*!40000 ALTER TABLE `Categorias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `Detalles_Pedido`
--

LOCK TABLES `Detalles_Pedido` WRITE;
/*!40000 ALTER TABLE `Detalles_Pedido` DISABLE KEYS */;
INSERT INTO `Detalles_Pedido` VALUES (1,1,1,1,699.99),(2,1,2,1,29.99),(3,2,2,1,29.99);
/*!40000 ALTER TABLE `Detalles_Pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `Pedidos`
--

LOCK TABLES `Pedidos` WRITE;
/*!40000 ALTER TABLE `Pedidos` DISABLE KEYS */;
INSERT INTO `Pedidos` VALUES (1,1,'2024-11-17 16:11:17','pendiente',729.98),(2,2,'2024-11-17 16:11:17','completado',29.99);
/*!40000 ALTER TABLE `Pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `Productos`
--

LOCK TABLES `Productos` WRITE;
/*!40000 ALTER TABLE `Productos` DISABLE KEYS */;
INSERT INTO `Productos` VALUES (1,'Smartphone','Teléfono inteligente de última generación',699.99,50,1),(2,'Camisa Casual','Camisa de algodón de manga larga',29.99,100,2),(3,'Sofá de 3 plazas','Sofá cómodo de tela',399.99,20,3);
/*!40000 ALTER TABLE `Productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `Usuarios`
--

LOCK TABLES `Usuarios` WRITE;
/*!40000 ALTER TABLE `Usuarios` DISABLE KEYS */;
INSERT INTO `Usuarios` VALUES (1,'Ada Azucena','ada.azucena@email.com',_binary 'azucena','2024-11-17 16:10:57'),(2,'Angel Azucena','angel.azucena@example.com',_binary 'azucena','2024-11-17 16:10:57'),(3,'Maria Luna','maria.luna@example.com',_binary 'luna','2024-11-17 16:10:57'),(4,'Angel','angel.email@email.com',_binary 'azucena','2024-11-17 17:04:49'),(5,'ismael','isma@email.com',_binary '\�֨ք��c���hN','2024-11-21 06:26:32'),(6,'test','test@email.com',_binary '�\�^0�G�f�Y`�~]�','2024-11-21 17:33:29');
/*!40000 ALTER TABLE `Usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-21 12:33:04
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
