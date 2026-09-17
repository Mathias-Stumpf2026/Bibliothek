CREATE DATABASE  IF NOT EXISTS `lianes_library` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `lianes_library`;
-- MySQL dump 10.13  Distrib 8.0.40, for macos14 (arm64)
--
-- Host: localhost    Database: atlas
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `authors`
--

DROP TABLE IF EXISTS `authors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8 */;
CREATE TABLE `authors` (
`authorID` int AUTO_INCREMENT NOT NULL PRIMARY KEY ,
`first_name` varchar(45) DEFAULT NULL,
`last_name` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authors`
--

/* LOCK TABLES `authors` WRITE; */
/*!40000 ALTER TABLE `authors` DISABLE KEYS */;
INSERT INTO `authors` (`first_name`, `last_name`) VALUES 
('Stephen','King'),
('Joanne K.','Rowling'),
('J.R.R.','Tolkien'),
('George','Orwell'),
('Jane','Austen'),
('Dan','Brown'),
('Agatha','Christie'),
('Frank','Herbert'),
('Suzanne','Collins'),
('Michael','Ende');
/*!40000 ALTER TABLE `authors` ENABLE KEYS */;
/*UNLOCK TABLES;*/

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8 */;
CREATE TABLE `books` (
  `bookID` int AUTO_INCREMENT NOT NULL PRIMARY KEY,
  `authorID` int DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `subtitle` varchar(255) DEFAULT NULL,
  `description` text(1000) DEFAULT NULL,
  `genre` varchar(45) DEFAULT NULL,
  `cover` varchar(255) DEFAULT NULL,
  `ISBN` varchar(17) DEFAULT NULL,
  `pub_year` year(4) DEFAULT NULL,
  `duplicate` varchar(45) DEFAULT NULL,
  `language`char(5) DEFAULT NULL,
  `publisher` varchar(45) DEFAULT NULL,
  FOREIGN KEY (`authorID`) REFERENCES `authors` (`authorID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

/*LOCK TABLES `books` WRITE;*/
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` (`authorID`, `title`, `subtitle`, `description`, `genre`, `cover`, `ISBN`, `pub_year`, `duplicate`, `language`, `publisher`) VALUES 
(1,'Es',NULL,NULL,'Horror',NULL,'978-3-453-43577-3','2011',NULL,'DEU','Heyne'),
(2,'Harry Potter und der Stein der Weisen',NULL,NULL,'Fantasy',NULL,'978-3-551-55741-4','2018',NULL,'DEU','Carlsen'),
(3,'Der Hobbit',NULL,NULL,'Fantasy',NULL,'978-3-6089-3800-5','2009',NULL,'DEU','Klett-Cotta'),
(4,'1984',NULL,NULL,'Dystopie',NULL,'978-3-548-23410-6','1994',NULL,'DEU','Ullstein'),
(5,'Stolz und Vorurteil',NULL,NULL,'Roman',NULL,'978-3-423-14160-4','2012',NULL,'DEU','Reclam'),
(6,'Illuminati',NULL,NULL,'Thriller',NULL,'978-3-404-14866-0','2003',NULL,'DEU','Bastei Lübbe'),
(7,'Mord im Orient-Express',NULL,NULL,'Krimi',NULL,'978-3-455-65001-3','2014',NULL,'DEU','Atlantik'),
(8,'Dune',NULL,NULL,'Science-Fiction',NULL,'9783453310847','1965',NULL,'DEU','Heyne'),
(9,'Die Tribute von Panem','Tödliche Spiele',NULL,'Dystopie',NULL,'978-3-7891-3218-6','2009',NULL,'DEU','Oetinger'),
(10,'Die unendliche Geschichte',NULL,NULL,'Fantasy',NULL,'978-3-522-20260-2','2019',NULL,'DEU','Thienemann');
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
/*UNLOCK TABLES;*/

--
-- Table structure for table `borrowers`
--

DROP TABLE IF EXISTS `borrowers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8 */;
CREATE TABLE `borrowers` (
`borrowerID` int AUTO_INCREMENT NOT NULL PRIMARY KEY,
`first_name` varchar(45) NOT NULL,
`last_name` varchar(60) NOT NULL,
`email` varchar(45) DEFAULT NULL,
`telephone` varchar(22) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `borrowers`
--

/*LOCK TABLES `borrowers` WRITE;*/
/*!40000 ALTER TABLE `borrowers` DISABLE KEYS */;
INSERT INTO `borrowers` (`first_name`, `last_name`, `email`, `telephone`) VALUES 
('Anna','Becker','anna.becker@example.com','0151-10000001'),
('Lukas','Wagner','lukas.wagner@example.com','0151-10000002'),
('Sarah','Hoffmann','sarah.hoffmann@example.com','0151-10000003'),
('Jonas','Keller','jonas.keller@example.com','0151-10000004'),
('Lena','Richter','lena.richter@example.com','0151-10000005'),
('Tim','Schneider','tim.schneider@example.com','0151-10000006'),
('Marie','Fischer','marie.fischer@example.com','0151-10000007'),
('Daniel','Weber','daniel.weber@example.com','0151-10000008'),
('Laura','Neumann','laura.neumann@example.com','0151-10000009'),
('Felix','Braun','felix.braun@example.com','0151-10000010');
/*!40000 ALTER TABLE `borrowers` ENABLE KEYS */;
/*UNLOCK TABLES;*/

--
-- Table structure for table `loans`
--

DROP TABLE IF EXISTS `loans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8 */;
CREATE TABLE `loans` (
`loanID` int AUTO_INCREMENT NOT NULL PRIMARY KEY,
`bookID` int NOT NULL,
`borrowerID` int NOT NULL,  
`loan_date` date DEFAULT NULL,
`return_date` date DEFAULT NULL,
`borrowed` tinyint(1) DEFAULT TRUE,
FOREIGN KEY (`bookID`) REFERENCES `books` (`bookID`),
FOREIGN KEY (`borrowerID`) REFERENCES `borrowers` (`borrowerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loans`
--

/*LOCK TABLES `loans` WRITE;*/
/*!40000 ALTER TABLE `loans` DISABLE KEYS */;
INSERT INTO `loans` (`bookID`, `borrowerID`, `loan_date`, `return_date`, `borrowed`) VALUES
(3,1,'2026-08-01','2026-08-14',0),
(7,4,'2026-08-03','2026-08-20',0),
(1,2,'2026-08-10',NULL,1),
(9,6,'2026-08-12','2026-08-29',0),
(5,3,'2026-08-15',NULL,1),
(2,8,'2026-08-19','2026-09-02',0),
(10,5,'2026-08-22',NULL,1),
(4,9,'2026-08-25','2026-09-05',0),
(8,7,'2026-09-01',NULL,1),
(6,10,'2026-09-04',NULL,1);
/*!40000 ALTER TABLE `loans` ENABLE KEYS */;
/*UNLOCK TABLES;*/




