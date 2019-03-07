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
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(128) DEFAULT NULL,
  `role` enum('tutor','student','admin') DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_accounts_email` (`email`),
  KEY `ix_accounts_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
INSERT INTO `accounts` VALUES (10,'tutor1','test1@gmail.com','pbkdf2:sha256:50000$bkZANTOg$570448aecc90f03eda6dcb2f44ec52a0cc17f1c9df9206bd241d79166d0ae1ea','tutor'),(11,'tutor2','test2@gmail.com','pbkdf2:sha256:50000$9gy4UdL2$58745c7323566de8b453ee77947126d274f2f7ddedcaf8a00804339f891753cb','tutor'),(12,'tutor3','test3@gmail.com','pbkdf2:sha256:50000$nUfVBbsI$b3b082e526922fca2146241267fe4decc142463efa8d0006725bf4ffccf08c29','tutor'),(13,'tutor4','test4@gmail.com','pbkdf2:sha256:50000$xCVebIhU$65694469b899683de77bbd060572daff88a1422fb523dbae1d0dc759592d9711','tutor'),(14,'tutor5','test5@gmail.com','pbkdf2:sha256:50000$z2SRzHGY$ed22648f9803d2b25aafd4c064f2681eb8bda299ed2d7773a785b589fb13aee7','tutor'),(15,'tutor6','test6@gmail.com','pbkdf2:sha256:50000$KmSn0NgG$f63b415e22a1706f115118afc746a0f1eed94548331889afbfe9a0b656067231','tutor'),(16,'Student 1','student1@gmail.com','pbkdf2:sha256:50000$77NZ2qBm$bad5fbf65424440c65ccc7e0baa3512d656dd3a19ff01ba8b8f298ed12a39a84','student'),(17,'Student 2','student2@gmail.com','pbkdf2:sha256:50000$kROTWWPb$a2987edc639ecc1eb420d8c15c98d9a3580384a8f6a53c0106d34518947d52c6','student'),(18,'Student 3','student3@gmail.com','pbkdf2:sha256:50000$Sib8KYM1$9fb55b7b6d95c0ab2642ad9ddc9993fdfd8c905e479a57dffc8a0b2824b93c34','student');
/*!40000 ALTER TABLE `accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `classes`
--

DROP TABLE IF EXISTS `classes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `classes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `student_limit` int(11) NOT NULL,
  `status` enum('active','deleted') DEFAULT NULL,
  `tutor_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `tutor_id` (`tutor_id`),
  CONSTRAINT `classes_ibfk_1` FOREIGN KEY (`tutor_id`) REFERENCES `accounts` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classes`
--

LOCK TABLES `classes` WRITE;
/*!40000 ALTER TABLE `classes` DISABLE KEYS */;
INSERT INTO `classes` VALUES (1,'Class1Tutor1',12,'active',10),(2,'Class2Tutor1',15,'deleted',10),(3,'Class3Tutor1',15,'active',10),(4,'Class21Tutor2',15,'active',11),(5,'Class22Tutor2',15,'active',11),(6,'Class23Tutor2',14,'active',11),(7,'Class31Tutor3',14,'active',12);
/*!40000 ALTER TABLE `classes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enrolls`
--

DROP TABLE IF EXISTS `enrolls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `enrolls` (
  `student_id` int(11) NOT NULL,
  `class_id` int(11) NOT NULL,
  `isRemoved` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`student_id`,`class_id`),
  KEY `class_id` (`class_id`),
  CONSTRAINT `enrolls_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `accounts` (`id`),
  CONSTRAINT `enrolls_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enrolls`
--

LOCK TABLES `enrolls` WRITE;
/*!40000 ALTER TABLE `enrolls` DISABLE KEYS */;
INSERT INTO `enrolls` VALUES (16,1,1),(16,3,0),(16,4,1),(16,5,0),(17,1,0),(17,5,0),(17,7,0),(18,1,0),(18,3,0),(18,4,0);
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

-- Dump completed on 2019-03-08  0:48:10
