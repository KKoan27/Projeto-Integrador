CREATE DATABASE  IF NOT EXISTS `techmark` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `techmark`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: techmark
-- ------------------------------------------------------
-- Server version	8.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `aluno`
--

DROP TABLE IF EXISTS `aluno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `aluno` (
  `id_aluno` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(45) DEFAULT NULL,
  `idade` decimal(2,0) DEFAULT NULL,
  `matricula` varchar(45) DEFAULT NULL,
  `cpf` varchar(14) DEFAULT NULL,
  `rg` varchar(12) DEFAULT NULL,
  `estuda` int DEFAULT NULL,
  PRIMARY KEY (`id_aluno`),
  UNIQUE KEY `id_aluno` (`id_aluno`),
  UNIQUE KEY `cpf` (`cpf`),
  UNIQUE KEY `rg` (`rg`),
  KEY `estuda` (`estuda`),
  CONSTRAINT `aluno_ibfk_1` FOREIGN KEY (`estuda`) REFERENCES `curso` (`id_curso`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aluno`
--

LOCK TABLES `aluno` WRITE;
/*!40000 ALTER TABLE `aluno` DISABLE KEYS */;
INSERT INTO `aluno` VALUES (5,'Max Souzus',43,'13546957','163546576','136546576',4);
/*!40000 ALTER TABLE `aluno` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app`
--

DROP TABLE IF EXISTS `app`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app` (
  `id_app` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(45) DEFAULT NULL,
  `estado` varchar(45) DEFAULT NULL,
  `versão` varchar(45) DEFAULT NULL,
  `vencimento_licença` date DEFAULT NULL,
  PRIMARY KEY (`id_app`),
  UNIQUE KEY `id_app` (`id_app`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app`
--

LOCK TABLES `app` WRITE;
/*!40000 ALTER TABLE `app` DISABLE KEYS */;
/*!40000 ALTER TABLE `app` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `computadores`
--

DROP TABLE IF EXISTS `computadores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `computadores` (
  `id_computadores` int NOT NULL AUTO_INCREMENT,
  `nome_pc` varchar(45) DEFAULT NULL,
  `conf` varchar(500) DEFAULT NULL,
  `estado` varchar(45) DEFAULT NULL,
  `localização_sala_lab` int DEFAULT NULL,
  `localização_setor` int DEFAULT NULL,
  PRIMARY KEY (`id_computadores`),
  UNIQUE KEY `id_computadores` (`id_computadores`),
  KEY `localização_sala_lab` (`localização_sala_lab`),
  KEY `localização_setor` (`localização_setor`),
  CONSTRAINT `computadores_ibfk_1` FOREIGN KEY (`localização_sala_lab`) REFERENCES `sala_lab` (`id_sala_lab`),
  CONSTRAINT `computadores_ibfk_2` FOREIGN KEY (`localização_setor`) REFERENCES `setor` (`id_setor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `computadores`
--

LOCK TABLES `computadores` WRITE;
/*!40000 ALTER TABLE `computadores` DISABLE KEYS */;
/*!40000 ALTER TABLE `computadores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contas`
--

DROP TABLE IF EXISTS `contas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contas` (
  `id_contas` int NOT NULL AUTO_INCREMENT,
  `usuario` varchar(45) DEFAULT NULL,
  `senha` varchar(45) DEFAULT NULL,
  `nivel` varchar(45) DEFAULT NULL,
  `funcionario_id` int DEFAULT NULL,
  PRIMARY KEY (`id_contas`),
  KEY `funcionario_id` (`funcionario_id`),
  CONSTRAINT `contas_ibfk_1` FOREIGN KEY (`funcionario_id`) REFERENCES `funcionarios` (`id_funcionarios`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contas`
--

LOCK TABLES `contas` WRITE;
/*!40000 ALTER TABLE `contas` DISABLE KEYS */;
INSERT INTO `contas` VALUES (2,'Bob','123','1',1);
/*!40000 ALTER TABLE `contas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `curso`
--

DROP TABLE IF EXISTS `curso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `curso` (
  `id_curso` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(45) DEFAULT NULL,
  `tempo` varchar(45) DEFAULT NULL,
  `n°_materias` decimal(2,0) DEFAULT NULL,
  PRIMARY KEY (`id_curso`),
  UNIQUE KEY `id_curso` (`id_curso`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `curso`
--

LOCK TABLES `curso` WRITE;
/*!40000 ALTER TABLE `curso` DISABLE KEYS */;
INSERT INTO `curso` VALUES (1,'ADS','5 semestres',40),(4,'Pergolado','6 semestres',66);
/*!40000 ALTER TABLE `curso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `funcionarios`
--

DROP TABLE IF EXISTS `funcionarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `funcionarios` (
  `id_funcionarios` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(45) DEFAULT NULL,
  `cpf` varchar(14) DEFAULT NULL,
  `rg` varchar(12) DEFAULT NULL,
  `função` varchar(45) DEFAULT NULL,
  `salarioRS` decimal(7,0) DEFAULT NULL,
  `setor` int DEFAULT NULL,
  `leciona` int DEFAULT NULL,
  PRIMARY KEY (`id_funcionarios`),
  UNIQUE KEY `id_funcionarios` (`id_funcionarios`),
  UNIQUE KEY `cpf` (`cpf`),
  UNIQUE KEY `rg` (`rg`),
  KEY `setor` (`setor`),
  KEY `leciona` (`leciona`),
  CONSTRAINT `funcionarios_ibfk_1` FOREIGN KEY (`setor`) REFERENCES `setor` (`id_setor`),
  CONSTRAINT `funcionarios_ibfk_2` FOREIGN KEY (`leciona`) REFERENCES `curso` (`id_curso`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `funcionarios`
--

LOCK TABLES `funcionarios` WRITE;
/*!40000 ALTER TABLE `funcionarios` DISABLE KEYS */;
INSERT INTO `funcionarios` VALUES (1,'Manoel Gome','6516546','65465546','Técnico',2000,1,NULL);
/*!40000 ALTER TABLE `funcionarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pacote_internet`
--

DROP TABLE IF EXISTS `pacote_internet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pacote_internet` (
  `id_pacote_internet` int NOT NULL AUTO_INCREMENT,
  `velocidade` varchar(45) DEFAULT NULL,
  `estado` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_pacote_internet`),
  UNIQUE KEY `id_pacote_internet` (`id_pacote_internet`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pacote_internet`
--

LOCK TABLES `pacote_internet` WRITE;
/*!40000 ALTER TABLE `pacote_internet` DISABLE KEYS */;
/*!40000 ALTER TABLE `pacote_internet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projetor`
--

DROP TABLE IF EXISTS `projetor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projetor` (
  `id_projetor` int NOT NULL AUTO_INCREMENT,
  `estado` varchar(45) DEFAULT NULL,
  `modelo` varchar(45) DEFAULT NULL,
  `localização` int DEFAULT NULL,
  PRIMARY KEY (`id_projetor`),
  UNIQUE KEY `id_projetor` (`id_projetor`),
  KEY `localização` (`localização`),
  CONSTRAINT `projetor_ibfk_1` FOREIGN KEY (`localização`) REFERENCES `sala_lab` (`id_sala_lab`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projetor`
--

LOCK TABLES `projetor` WRITE;
/*!40000 ALTER TABLE `projetor` DISABLE KEYS */;
/*!40000 ALTER TABLE `projetor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sala_lab`
--

DROP TABLE IF EXISTS `sala_lab`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sala_lab` (
  `id_sala_lab` int NOT NULL AUTO_INCREMENT,
  `andar` varchar(45) DEFAULT NULL,
  `numero` decimal(3,0) DEFAULT NULL,
  `tipo` varchar(45) DEFAULT NULL,
  `capacidade` varchar(45) DEFAULT NULL,
  `reserva` varchar(45) DEFAULT NULL,
  `quant_pc` decimal(4,0) DEFAULT NULL,
  PRIMARY KEY (`id_sala_lab`),
  UNIQUE KEY `id_sala_lab` (`id_sala_lab`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sala_lab`
--

LOCK TABLES `sala_lab` WRITE;
/*!40000 ALTER TABLE `sala_lab` DISABLE KEYS */;
/*!40000 ALTER TABLE `sala_lab` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servidor`
--

DROP TABLE IF EXISTS `servidor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servidor` (
  `id_servidor` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(45) DEFAULT NULL,
  `estado` varchar(45) DEFAULT NULL,
  `capacidade` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_servidor`),
  UNIQUE KEY `id_servidor` (`id_servidor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servidor`
--

LOCK TABLES `servidor` WRITE;
/*!40000 ALTER TABLE `servidor` DISABLE KEYS */;
/*!40000 ALTER TABLE `servidor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `setor`
--

DROP TABLE IF EXISTS `setor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `setor` (
  `id_setor` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(45) DEFAULT NULL,
  `andar` varchar(45) DEFAULT NULL,
  `quant_funcionarios` decimal(4,0) DEFAULT NULL,
  `quant_pc` decimal(4,0) DEFAULT NULL,
  PRIMARY KEY (`id_setor`),
  UNIQUE KEY `id_setor` (`id_setor`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `setor`
--

LOCK TABLES `setor` WRITE;
/*!40000 ALTER TABLE `setor` DISABLE KEYS */;
INSERT INTO `setor` VALUES (1,'TI','2',4,4);
/*!40000 ALTER TABLE `setor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `switch`
--

DROP TABLE IF EXISTS `switch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `switch` (
  `id_switch` int NOT NULL AUTO_INCREMENT,
  `localização` varchar(45) DEFAULT NULL,
  `estado` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_switch`),
  UNIQUE KEY `id_switch` (`id_switch`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `switch`
--

LOCK TABLES `switch` WRITE;
/*!40000 ALTER TABLE `switch` DISABLE KEYS */;
/*!40000 ALTER TABLE `switch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `website`
--

DROP TABLE IF EXISTS `website`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `website` (
  `id_website` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(45) DEFAULT NULL,
  `estado` varchar(45) DEFAULT NULL,
  `versão` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_website`),
  UNIQUE KEY `id_website` (`id_website`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `website`
--

LOCK TABLES `website` WRITE;
/*!40000 ALTER TABLE `website` DISABLE KEYS */;
/*!40000 ALTER TABLE `website` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'techmark'
--

--
-- Dumping routines for database 'techmark'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-28  7:19:47
