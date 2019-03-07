-- MySQL dump 10.13  Distrib 5.7.25, for Linux (x86_64)
--
-- Host: localhost    Database: db
-- ------------------------------------------------------
-- Server version	5.7.25-0ubuntu0.16.04.2

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
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `accounts` (
  `email` text,
  `password_hash` text,
  `role` text,
  `id` int(11) DEFAULT NULL,
  `name` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
INSERT INTO `accounts` VALUES ('test1@gmail.com','pbkdf2:sha256:50000$QTCUDYp5$f673d6f6381570d711056a834cfb696cdd3390c1ef0c5fc43a353940b7111a11','tutor',6,'test1Name'),('test2@gmail.com','pbkdf2:sha256:50000$mMiVvMl0$8c375ce8d41685eec43f02dbfee182b3cec582ce3572a012d0c7682524e1209c','tutor',7,'test2Name'),('test3@gmail.com','pbkdf2:sha256:50000$QWHsQXG1$96fecd30e8344c599fd08d33e81deec8bcb46ea728f2af5c97bd37cdc6131a75','tutor',8,'tutor'),('test4@gmail.com','pbkdf2:sha256:50000$G5cEpOhK$60d256b0ab752257aaf12d875e3a30408424a20a6d3027b0d4e034f797c86a10','tutor',9,'tutor2'),('student1@gmail.com','pbkdf2:sha256:50000$gqerH1mn$63f7e5ce1f9ef32d15980bdbd55d79d83ea13845500fd7b279ebc111a9fa04a4','student',10,'Do Hong Son'),('test5@gmail.com','pbkdf2:sha256:50000$5nlWkyLm$3bf37067f25c6eb52f6902abb3bc9c8b6f83b682751bb9a1bb68aaa417990c77','tutor',12,'tutor5'),('student2@gmail.com','pbkdf2:sha256:50000$ygBo2pmt$8a45683bba1bd9108290114f2fe8b1169972dc222c37b316c0c295f7e93a5ce5','student',13,'Student 2'),('student3@gmail.com','pbkdf2:sha256:50000$AQjNSlQZ$3c4b75d3bf4365cbc3f5aadd41cf4f851ab45f42d1286f29e3758aa36687d3ea','student',14,'Student 3'),('test6@gmail.com','pbkdf2:sha256:50000$i3TrBjtD$74d93bb12144266f765dceb422c840aba63e9cea64313b3ff4d6b75d83f31bcc','tutor',15,'tutor6');
/*!40000 ALTER TABLE `accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `classes`
--

DROP TABLE IF EXISTS `classes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `classes` (
  `student_limit` int(11) DEFAULT NULL,
  `status` text,
  `tutor_id` int(11) DEFAULT NULL,
  `id` int(11) DEFAULT NULL,
  `name` text
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classes`
--

LOCK TABLES `classes` WRITE;
/*!40000 ALTER TABLE `classes` DISABLE KEYS */;
INSERT INTO `classes` VALUES (15,'active',7,1,'Class1'),(15,'active',8,3,'Class3'),(15,'active',8,4,'Class4'),(15,'deleted',6,5,'Class1.1'),(10,'deleted',12,6,'Class55'),(1,'deleted',7,7,'Class66');
/*!40000 ALTER TABLE `classes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enrolls`
--

DROP TABLE IF EXISTS `enrolls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `enrolls` (
  `class_id` int(11) DEFAULT NULL,
  `student_id` int(11) DEFAULT NULL,
  `isRemoved` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enrolls`
--

LOCK TABLES `enrolls` WRITE;
/*!40000 ALTER TABLE `enrolls` DISABLE KEYS */;
INSERT INTO `enrolls` VALUES (1,10,1),(3,10,0),(4,10,0),(1,13,0),(3,13,1),(4,13,0);
/*!40000 ALTER TABLE `enrolls` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-03-07 22:40:18
