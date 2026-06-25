CREATE DATABASE  IF NOT EXISTS `animal_rescue_db` /*!40100 DEFAULT CHARACTER SET utf8mb3 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `animal_rescue_db`;
-- MySQL dump 10.13  Distrib 8.0.45, for macos15 (arm64)
--
-- Host: localhost    Database: animal_rescue_db
-- ------------------------------------------------------
-- Server version	8.0.45

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
-- Table structure for table `adoptionInfo`
--

DROP TABLE IF EXISTS `adoptionInfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `adoptionInfo` (
  `idadoptionInfo` int NOT NULL AUTO_INCREMENT,
  `adoptionStatus_idadoptionStatus` int NOT NULL,
  `adoptionInfoAdopterName` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idadoptionInfo`),
  KEY `fk_adoptionInfo_adoptionStatus1_idx` (`adoptionStatus_idadoptionStatus`),
  CONSTRAINT `fk_adoptionInfo_adoptionStatus1` FOREIGN KEY (`adoptionStatus_idadoptionStatus`) REFERENCES `adoptionStatus` (`idadoptionStatus`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adoptionInfo`
--

LOCK TABLES `adoptionInfo` WRITE;
/*!40000 ALTER TABLE `adoptionInfo` DISABLE KEYS */;
INSERT INTO `adoptionInfo` VALUES (1,1,NULL),(2,2,NULL),(6,1,NULL),(7,1,NULL),(8,2,NULL),(9,3,NULL),(10,3,'Bruce'),(11,2,NULL),(12,1,NULL),(14,3,'Nichola'),(15,1,NULL),(16,1,NULL),(17,1,NULL),(18,3,NULL),(19,2,NULL),(20,3,NULL),(21,1,NULL),(25,3,'Tammo');
/*!40000 ALTER TABLE `adoptionInfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `adoptionStatus`
--

DROP TABLE IF EXISTS `adoptionStatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `adoptionStatus` (
  `idadoptionStatus` int NOT NULL AUTO_INCREMENT,
  `adoptionStatus` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idadoptionStatus`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adoptionStatus`
--

LOCK TABLES `adoptionStatus` WRITE;
/*!40000 ALTER TABLE `adoptionStatus` DISABLE KEYS */;
INSERT INTO `adoptionStatus` VALUES (1,'Available'),(2,'Pending'),(3,'Adopted');
/*!40000 ALTER TABLE `adoptionStatus` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `animal`
--

DROP TABLE IF EXISTS `animal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `animal` (
  `idanimal` int NOT NULL AUTO_INCREMENT,
  `animalName` varchar(25) NOT NULL,
  `animalRescueDate` date DEFAULT NULL,
  `species_idspecies` int NOT NULL,
  `breed_idbreed` int NOT NULL,
  `adoptionStatus_idadoptionInfo` int NOT NULL,
  `fosterCarer_idfosterCarer` int NOT NULL,
  PRIMARY KEY (`idanimal`),
  KEY `fk_animal_species_idx` (`species_idspecies`),
  KEY `fk_animal_breed1_idx` (`breed_idbreed`),
  KEY `fk_animal_adoptionStatus1_idx` (`adoptionStatus_idadoptionInfo`),
  KEY `fk_animal_fosterCarer1_idx` (`fosterCarer_idfosterCarer`),
  CONSTRAINT `fk_animal_breed1` FOREIGN KEY (`breed_idbreed`) REFERENCES `breed` (`idbreed`),
  CONSTRAINT `fk_animal_fosterCarer1` FOREIGN KEY (`fosterCarer_idfosterCarer`) REFERENCES `fosterCarer` (`idfosterCarer`),
  CONSTRAINT `fk_animal_species` FOREIGN KEY (`species_idspecies`) REFERENCES `species` (`idspecies`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `animal`
--

LOCK TABLES `animal` WRITE;
/*!40000 ALTER TABLE `animal` DISABLE KEYS */;
INSERT INTO `animal` VALUES (4,'Rocky','2026-04-17',2,2,8,3),(5,'Pip','2026-05-01',1,1,9,1),(6,'Shadow','2026-05-06',4,5,10,3),(7,'Milo','2026-05-09',1,5,11,3),(8,'Coco','2026-05-11',4,6,12,1),(12,'John','2026-05-27',4,5,14,3),(14,'Rocky','2026-05-24',1,1,16,1),(17,'Samul','2026-06-24',2,4,19,3),(19,'Luna 2','2026-04-17',1,1,21,1),(20,'Stormus','2026-06-16',4,5,25,3);
/*!40000 ALTER TABLE `animal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `breed`
--

DROP TABLE IF EXISTS `breed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `breed` (
  `idbreed` int NOT NULL AUTO_INCREMENT,
  `animalBreed` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idbreed`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `breed`
--

LOCK TABLES `breed` WRITE;
/*!40000 ALTER TABLE `breed` DISABLE KEYS */;
INSERT INTO `breed` VALUES (1,'Maine Coon'),(2,'Labrador'),(3,'Mini Lop'),(4,'German Shepherd'),(5,'Bengal'),(6,'Cockatiel'),(7,'Unknown');
/*!40000 ALTER TABLE `breed` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fosterCarer`
--

DROP TABLE IF EXISTS `fosterCarer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fosterCarer` (
  `idfosterCarer` int NOT NULL AUTO_INCREMENT,
  `fosterCarerFirstName` varchar(45) DEFAULT NULL,
  `fosterCarerLastName` varchar(45) DEFAULT NULL,
  `fosterCarerPhone` int DEFAULT NULL,
  PRIMARY KEY (`idfosterCarer`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fosterCarer`
--

LOCK TABLES `fosterCarer` WRITE;
/*!40000 ALTER TABLE `fosterCarer` DISABLE KEYS */;
INSERT INTO `fosterCarer` VALUES (1,'Emma','Clark',21998877),(2,'Cole','Lobban',226845480),(3,'Ben','Harris',22776655),(4,'Tina ','Wells',21443322),(5,'Tammo','B',22776655),(6,'Cole','Lobban',22776655),(7,'Joyce','Lobban',226845480);
/*!40000 ALTER TABLE `fosterCarer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `species`
--

DROP TABLE IF EXISTS `species`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `species` (
  `idspecies` int NOT NULL AUTO_INCREMENT,
  `animalSpecies` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idspecies`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `species`
--

LOCK TABLES `species` WRITE;
/*!40000 ALTER TABLE `species` DISABLE KEYS */;
INSERT INTO `species` VALUES (1,'Cat'),(2,'Dog'),(3,'Rabbit'),(4,'Bird');
/*!40000 ALTER TABLE `species` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `treatment`
--

DROP TABLE IF EXISTS `treatment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `treatment` (
  `idtreatment` int NOT NULL AUTO_INCREMENT,
  `treatment` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idtreatment`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `treatment`
--

LOCK TABLES `treatment` WRITE;
/*!40000 ALTER TABLE `treatment` DISABLE KEYS */;
INSERT INTO `treatment` VALUES (1,'Vaccination'),(2,'Surgery'),(3,'Check-up'),(4,'Dental Treatment'),(5,'Wing Assessment'),(6,'Flea & Tick'),(7,'Worming'),(8,'General Check-up');
/*!40000 ALTER TABLE `treatment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `treatments`
--

DROP TABLE IF EXISTS `treatments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `treatments` (
  `idtreatments` int NOT NULL AUTO_INCREMENT,
  `treatment_idtreatment` int NOT NULL,
  `vet_idvet` int NOT NULL,
  `animal_idanimal` int NOT NULL,
  PRIMARY KEY (`idtreatments`),
  KEY `fk_treatments_treatment1_idx` (`treatment_idtreatment`),
  KEY `fk_treatments_vet1_idx` (`vet_idvet`),
  KEY `fk_treatments_animal1_idx` (`animal_idanimal`),
  CONSTRAINT `fk_treatments_animal1` FOREIGN KEY (`animal_idanimal`) REFERENCES `animal` (`idanimal`) ON DELETE CASCADE,
  CONSTRAINT `fk_treatments_treatment1` FOREIGN KEY (`treatment_idtreatment`) REFERENCES `treatment` (`idtreatment`),
  CONSTRAINT `fk_treatments_vet1` FOREIGN KEY (`vet_idvet`) REFERENCES `vet` (`idvet`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `treatments`
--

LOCK TABLES `treatments` WRITE;
/*!40000 ALTER TABLE `treatments` DISABLE KEYS */;
INSERT INTO `treatments` VALUES (3,2,3,14),(4,3,1,5),(5,4,2,6),(7,1,3,20),(9,1,3,7),(10,3,2,8),(26,3,2,19);
/*!40000 ALTER TABLE `treatments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vet`
--

DROP TABLE IF EXISTS `vet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vet` (
  `idvet` int NOT NULL AUTO_INCREMENT,
  `vetName` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idvet`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vet`
--

LOCK TABLES `vet` WRITE;
/*!40000 ALTER TABLE `vet` DISABLE KEYS */;
INSERT INTO `vet` VALUES (1,'Dr Patel'),(2,'Dr Nguyen'),(3,'Dr Singh');
/*!40000 ALTER TABLE `vet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `volunteer`
--

DROP TABLE IF EXISTS `volunteer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `volunteer` (
  `idvolunteer` int NOT NULL AUTO_INCREMENT,
  `volunteerFirstName` varchar(45) DEFAULT NULL,
  `volunteerLastName` varchar(45) DEFAULT NULL,
  `volunteerShiftDay` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idvolunteer`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `volunteer`
--

LOCK TABLES `volunteer` WRITE;
/*!40000 ALTER TABLE `volunteer` DISABLE KEYS */;
INSERT INTO `volunteer` VALUES (1,'Jake','Morris','Monday'),(2,'Mia','Chen','Sunday'),(3,'Lara','Kim','Thursday'),(4,'Jake ','Morris','Wednesday'),(5,'Mai','Chen','Saturday'),(6,'Mai','Chen','Friday'),(7,'Cole','Coleson','Tuesday');
/*!40000 ALTER TABLE `volunteer` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-25 12:33:19
