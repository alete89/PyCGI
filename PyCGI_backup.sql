-- MySQL dump 10.13  Distrib 5.5.57, for debian-linux-gnu (armv7l)
--
-- Host: localhost    Database: PyCGI
-- ------------------------------------------------------
-- Server version	5.5.57-0+deb8u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `PyCGI`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `PyCGI` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `PyCGI`;

--
-- Table structure for table `TablaDeSecuencias`
--

DROP TABLE IF EXISTS `TablaDeSecuencias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TablaDeSecuencias` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Menu` varchar(45) DEFAULT NULL,
  `SubMenu` varchar(45) DEFAULT NULL,
  `SubSubMenu` varchar(45) DEFAULT NULL,
  `Coordenada` int(11) DEFAULT NULL,
  `OrdenDeSecuencia` int(11) DEFAULT NULL,
  `ModuloPython` varchar(45) DEFAULT NULL,
  `ComandoDeSistema` varchar(500) DEFAULT NULL,
  `LoopDeProceso` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TablaDeSecuencias`
--

LOCK TABLES `TablaDeSecuencias` WRITE;
/*!40000 ALTER TABLE `TablaDeSecuencias` DISABLE KEYS */;
INSERT INTO `TablaDeSecuencias` VALUES (44,'Config','Tabla de Secuencias','None',91,1,'FormAltaQtSQL-v2.py TablaDeSecuencias','',0),(45,'System','Date','None',11,1,'','date',3),(47,'Test','Loop 6 veces','None',31,1,'./tests/test1.py','',5),(48,'Test','Escribir archivo','None',32,1,'./tests/test3.py random.txt','',0),(50,'Config','Variables Globales','None',92,1,'FormAltaQtSQL-v2.py VariablesGlobales',NULL,0),(52,'Config','BackUp MySQL','None',93,1,'','mysqldump -u root --password=23101log --databases PyCGI > PyCGI_backup.sql',0),(54,'System','Ping','None',12,1,'','ping 127.0.0.1',0);
/*!40000 ALTER TABLE `TablaDeSecuencias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `VariablesGlobales`
--

DROP TABLE IF EXISTS `VariablesGlobales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `VariablesGlobales` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Variable` varchar(45) DEFAULT NULL,
  `Valor` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `VariablesGlobales`
--

LOCK TABLES `VariablesGlobales` WRITE;
/*!40000 ALTER TABLE `VariablesGlobales` DISABLE KEYS */;
INSERT INTO `VariablesGlobales` VALUES (1,'DirectorioDeTrabajo','/home/manuel/MTR_PC'),(2,'NombreDelPrograma','PyCGI - 2.1'),(3,'ImagenDePresentacion','/home/manuel/MTR_PC/img/pres.png');
/*!40000 ALTER TABLE `VariablesGlobales` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-11-13 22:02:39
