-- MySQL dump 10.13  Distrib 8.0.26, for Win64 (x86_64)
--
-- Host: 10.73.200.200    Database: wsupbot
-- ------------------------------------------------------
-- Server version	8.0.28-0ubuntu0.20.04.3

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
-- Dumping data for table `ANSRS`
--

LOCK TABLES `ANSRS` WRITE;
/*!40000 ALTER TABLE `ANSRS` DISABLE KEYS */;
INSERT INTO `ANSRS` VALUES (1,'Arabe','اللغة العربية',1,2),(2,'Français','اللغة الفرنسية',1,2),(3,'Je veux parler avec un agent ','اريد التحدث إلى وكيل',2,NULL),(4,'Je suis intéresser par le recrutement','أنا مهتم بالتوظيف',2,3),(5,'Je veux avoir des informations','اريد الحصول على معلومات',2,6),(6,'Télévendeurs ayant une expérience en Energie TÉLÉTRAVAIL','المسوقون الهاتفيون ذوو الخبرة في اتصالات الطاقة',4,NULL),(7,'Chargés de Clientèle débutant ','ممثلي خدمة العملاء المبتدئين',4,NULL),(8,'Experience en Centre d\'appel (junior & senior)','خبرة مركز الاتصال (مبتدئ وخبير)',4,NULL),(9,'Autres','غير ذلك',4,NULL),(10,'Cuisiniers','طهاة',5,NULL),(11,'Superviseurs de restauration','مشرفون على  التموين',5,NULL),(12,'Pâtissier boulanger','خباز- صانع الحلويات',5,NULL),(13,'Profil IT','مختص في المعلوميات',5,NULL),(14,'Autres','غير ذلك',5,NULL);
/*!40000 ALTER TABLE `ANSRS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `QTS`
--

LOCK TABLES `QTS` WRITE;
/*!40000 ALTER TABLE `QTS` DISABLE KEYS */;
INSERT INTO `QTS` VALUES (1,'Voulez-vous continuer en quelle langue !','بأي لغة  تريد المتابعة؟'),(2,'Choisir l\'option qui vous convient .','اختر  ما يناسبك'),(3,'Pour quelle offre vous voulez postuler ?','ما الوظيفة التي تريد التقدم  تود الترشح اليها  لها؟'),(4,'Recrutement National','توظيف داخل المغرب '),(5,'Recrutement International','التوظيف الدولي     توظييف خارج المغرب'),(6,'QA','سؤال و جواب ؟'),(7,'final',NULL),(8,'end',NULL);
/*!40000 ALTER TABLE `QTS` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-02-17 17:57:42
