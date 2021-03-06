-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: alarm_platform
-- ------------------------------------------------------
-- Server version	5.1.73

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
-- Table structure for table `alarm`
--

DROP TABLE IF EXISTS `alarm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alarm` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` char(64) NOT NULL,
  `zwaveid` int(11) NOT NULL,
  `deviceid` char(30) DEFAULT NULL,
  `deal_progress` int(11) DEFAULT '0',
  `deal_user` int(11) DEFAULT NULL,
  `deal_last_time` char(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alarm`
--

LOCK TABLES `alarm` WRITE;
/*!40000 ALTER TABLE `alarm` DISABLE KEYS */;
/*!40000 ALTER TABLE `alarm` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alarm_deal`
--

DROP TABLE IF EXISTS `alarm_deal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alarm_deal` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `alarm_id` int(11) DEFAULT NULL,
  `deal_manage` char(20) DEFAULT NULL,
  `telephone` char(20) DEFAULT NULL,
  `deal_time` char(20) DEFAULT NULL,
  `deal_remark` text,
  `audio` char(40) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alarm_deal`
--

LOCK TABLES `alarm_deal` WRITE;
/*!40000 ALTER TABLE `alarm_deal` DISABLE KEYS */;
/*!40000 ALTER TABLE `alarm_deal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `custumer`
--

DROP TABLE IF EXISTS `custumer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `custumer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(20) NOT NULL,
  `telephone` char(20) DEFAULT NULL,
  `email` char(32) DEFAULT NULL,
  `remark` text,
  `other` text,
  `deviceid` char(30) DEFAULT NULL,
  `phone` char(20) DEFAULT NULL,
  `state` char(20) DEFAULT '0',
  `city` char(20) DEFAULT '0',
  `street` char(20) DEFAULT NULL,
  `postelcode` char(20) DEFAULT NULL,
  `monleave` char(20) DEFAULT NULL,
  `monreturn` char(20) DEFAULT NULL,
  `tueleave` char(20) DEFAULT NULL,
  `tuereturn` char(20) DEFAULT NULL,
  `wedleave` char(20) DEFAULT NULL,
  `wedreturn` char(20) DEFAULT NULL,
  `thuleave` char(20) DEFAULT NULL,
  `thureturn` char(20) DEFAULT NULL,
  `frileave` char(20) DEFAULT NULL,
  `frireturn` char(20) DEFAULT NULL,
  `satleave` char(20) DEFAULT NULL,
  `satreturn` char(20) DEFAULT NULL,
  `sunleave` char(20) DEFAULT NULL,
  `sunreturn` char(20) DEFAULT NULL,
  `holleave` char(20) DEFAULT NULL,
  `holreturn` char(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `deviceid` (`deviceid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 PACK_KEYS=0;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `custumer`
--

LOCK TABLES `custumer` WRITE;
/*!40000 ALTER TABLE `custumer` DISABLE KEYS */;
/*!40000 ALTER TABLE `custumer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `record`
--

DROP TABLE IF EXISTS `record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` char(20) DEFAULT NULL,
  `object` char(20) DEFAULT NULL,
  `object_id` int(11) DEFAULT NULL,
  `action` char(20) DEFAULT NULL,
  `context` text,
  `time` char(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `record`
--

LOCK TABLES `record` WRITE;
/*!40000 ALTER TABLE `record` DISABLE KEYS */;
/*!40000 ALTER TABLE `record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sync_event`
--

DROP TABLE IF EXISTS `sync_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sync_event` (
  `id` int(11) NOT NULL,
  `type` char(20) DEFAULT NULL,
  `deviceid` char(30) DEFAULT NULL,
  `zwaveid` int(11) DEFAULT NULL,
  `eventtime` char(30) DEFAULT NULL,
  `context` text,
  `alarmid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sync_event`
--

LOCK TABLES `sync_event` WRITE;
/*!40000 ALTER TABLE `sync_event` DISABLE KEYS */;
/*!40000 ALTER TABLE `sync_event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(20) NOT NULL,
  `telephone` char(20) DEFAULT NULL,
  `passwd` char(64) DEFAULT NULL,
  `token` char(64) DEFAULT NULL,
  `logintime` char(64) DEFAULT NULL,
  `logouttime` char(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `token` (`token`),
  UNIQUE KEY `token_2` (`token`),
  UNIQUE KEY `token_3` (`token`),
  UNIQUE KEY `token_4` (`token`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 PACK_KEYS=0;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','','*4ACFE3202A5FF5CF467898FC58AAB1D615029441',NULL,NULL,NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-08-24 11:19:30
