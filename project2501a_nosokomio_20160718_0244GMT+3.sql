#
# SQL Export
# Created by Querious (1042)
# Created: 18 July 2016 at 02:45:22 GMT+3
# Encoding: Unicode (UTF-8)
#


DROP DATABASE IF EXISTS `project2501a_nosokomio`;
CREATE DATABASE `project2501a_nosokomio` DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
USE `project2501a_nosokomio`;




SET @PREVIOUS_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS;
SET FOREIGN_KEY_CHECKS = 0;


DROP TABLE IF EXISTS `test`;
DROP TABLE IF EXISTS `nosileia`;
DROP TABLE IF EXISTS `patient`;
DROP TABLE IF EXISTS `gene2disease`;
DROP TABLE IF EXISTS `gene`;
DROP TABLE IF EXISTS `doctor`;
DROP TABLE IF EXISTS `disease`;
DROP TABLE IF EXISTS `clinic`;


CREATE TABLE `clinic` (
  `clinic_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `beds` int(11) NOT NULL,
  `location` varchar(255) NOT NULL,
  PRIMARY KEY (`clinic_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;


CREATE TABLE `disease` (
  `diseaseId` varchar(10) NOT NULL,
  `diseaseName` varchar(50) NOT NULL,
  PRIMARY KEY (`diseaseId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `doctor` (
  `doctor_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `surname` varchar(255) NOT NULL,
  `speciality` varchar(255) NOT NULL,
  `clinic` int(11) NOT NULL,
  PRIMARY KEY (`doctor_id`),
  KEY `fk_doctor_clinic` (`clinic`),
  CONSTRAINT `fk_doctor_clinic` FOREIGN KEY (`clinic`) REFERENCES `clinic` (`clinic_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;


CREATE TABLE `gene` (
  `geneId` varchar(10) NOT NULL,
  `geneName` varchar(20) NOT NULL,
  PRIMARY KEY (`geneId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `gene2disease` (
  `geneId` varchar(10) DEFAULT NULL,
  `diseaseId` varchar(10) DEFAULT NULL,
  KEY `geneId` (`geneId`),
  KEY `diseaseId` (`diseaseId`),
  CONSTRAINT `gene2disease_ibfk_1` FOREIGN KEY (`geneId`) REFERENCES `gene` (`geneId`) ON UPDATE CASCADE,
  CONSTRAINT `gene2disease_ibfk_2` FOREIGN KEY (`diseaseId`) REFERENCES `disease` (`diseaseId`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `patient` (
  `afm` varchar(10) NOT NULL,
  `name` varchar(255) NOT NULL,
  `surname` varchar(255) NOT NULL,
  `birth_year` int(4) DEFAULT NULL,
  PRIMARY KEY (`afm`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `nosileia` (
  `nosileia_id` int(11) NOT NULL AUTO_INCREMENT,
  `patient` varchar(10) NOT NULL,
  `clinic` int(11) NOT NULL,
  `startdate` date NOT NULL,
  `days` int(11) NOT NULL,
  PRIMARY KEY (`nosileia_id`),
  KEY `fk_nosileia_clinic` (`clinic`),
  KEY `fk_nosileia_patient` (`patient`),
  CONSTRAINT `fk_nosileia_clinic` FOREIGN KEY (`clinic`) REFERENCES `clinic` (`clinic_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_nosileia_patient` FOREIGN KEY (`patient`) REFERENCES `patient` (`afm`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;


CREATE TABLE `test` (
  `counter` int(11) DEFAULT NULL,
  `string` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




SET FOREIGN_KEY_CHECKS = @PREVIOUS_FOREIGN_KEY_CHECKS;


SET @PREVIOUS_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS;
SET FOREIGN_KEY_CHECKS = 0;


LOCK TABLES `clinic` WRITE;
ALTER TABLE `clinic` DISABLE KEYS;
INSERT INTO `clinic` (`clinic_id`, `title`, `beds`, `location`) VALUES 
	(1,'Γενικής Χειρουργικής',20,'2ος όροφος'),
	(2,'Ψυχιατρική',30,'5ος όροφος'),
	(3,'Ακτινολογική',10,'1ος όροφος'),
	(4,'Αγγειοπλαστική',100,'3ος όροφος'),
	(5,'Νευρολογική',200,'6ος όροφος'),
	(6,'Ενδοκρινολογική',1000,'4ος όροφος');
ALTER TABLE `clinic` ENABLE KEYS;
UNLOCK TABLES;


LOCK TABLES `disease` WRITE;
ALTER TABLE `disease` DISABLE KEYS;
ALTER TABLE `disease` ENABLE KEYS;
UNLOCK TABLES;


LOCK TABLES `doctor` WRITE;
ALTER TABLE `doctor` DISABLE KEYS;
INSERT INTO `doctor` (`doctor_id`, `name`, `surname`, `speciality`, `clinic`) VALUES 
	(0,'Άννα','Καϊάφα','Ψυχίατρος',2),
	(1,'Άννα','Καϊάφα','Ψυχίατρος',2),
	(2,'Κότης','Κοτόπουλος','Χειρούργος-ΩΡΛ',1),
	(3,'Κοκό','Φουμπαρά','Ψυχίατρος-Ψυχολόγος',2),
	(4,'Φτιάχτος','Ματζαφλάρης','Χειρούργος',1),
	(5,'Άλφα','Ματζαφλάρης','Ακτινολόγος',3),
	(6,'Γάμμα','Ματζαφλάρης','Νοσοκόμος',5),
	(7,'Δέλτα','Ματζαφλάρης','Λογιστής',6),
	(8,'Έψιλον','Ματζαφλάρης','Λατζιέρης',1),
	(9,'Ζήτα','Ματζαφλάρης','Αποεντομοτής',2),
	(10,'Ήτα','Ματζαφλάρης','Ορθοπεδικός',3),
	(11,'Θήτα','Ματζαφλάρης','Χαρτορίχτρα',4),
	(12,'Ιώτα','Ματζαφλάρης','Ενδοκρινολόγος',5),
	(13,'Κάππα','Ματζαφλάρης','Παθολόγος',6),
	(14,'Λάμδα','Ματζαφλάρης','Πολλάβαρύςκαιόχι',1),
	(15,'Βήτα','Ματζαφλάρης','Ψυχογιός',4);
ALTER TABLE `doctor` ENABLE KEYS;
UNLOCK TABLES;


LOCK TABLES `gene` WRITE;
ALTER TABLE `gene` DISABLE KEYS;
ALTER TABLE `gene` ENABLE KEYS;
UNLOCK TABLES;


LOCK TABLES `gene2disease` WRITE;
ALTER TABLE `gene2disease` DISABLE KEYS;
ALTER TABLE `gene2disease` ENABLE KEYS;
UNLOCK TABLES;


LOCK TABLES `patient` WRITE;
ALTER TABLE `patient` DISABLE KEYS;
INSERT INTO `patient` (`afm`, `name`, `surname`, `birth_year`) VALUES 
	('9874563217','Τζιμ','Ο Μαύρος Θερμαστής',1988),
	('9874563218','Όπερα της','Πεντάρας',1989),
	('9874563219','Δημητριάδη','Αντάρτικα 1',1979),
	('9874563220','Δημητριάδη','Αντάρτικα 2',1980),
	('9874563221','Δημητριάδη','Αντάρτικα 3',1999),
	('9874563222','Δημητριάδη','Αντάρτικα 4',1929),
	('9874563223','Δημητριάδη','Αντάρτικα 4',1929),
	('9874563224','Δημητριάδη','Αντάρτικα 5',1949),
	('9874563225','Δημητριάδη','Αντάρτικα 6',1959),
	('9874563226','Δημητριάδη','Αντάρτικα 7',1969),
	('9874563227','Δημητριάδη','Αντάρτικα 8',1919),
	('9874563228','Δημητριάδη','Αντάρτικα 9',1929),
	('9874563229','Δημητριάδη','Αντάρτικα 10',1959),
	('9874563230','Δημητριάδη','Αντάρτικα 11',1989),
	('9874563231','Δημητριάδη','Αντάρτικα 12',1989),
	('9874563232','Δημητριάδη','Αντάρτικα 13',1989),
	('9874563233','Δημητριάδη','Αντάρτικα 14',1989),
	('9874563234','Δημητριάδη','Αντάρτικα 15',1989),
	('9874563235','Δημητριάδη','Αντάρτικα 16',1989),
	('9874563236','Δημητριάδη','Αντάρτικα 17',1989),
	('9874563237','Δημητριάδη','Αντάρτικα 18',1989),
	('9874563238','Δημητριάδη','Αντάρτικα 19',1989),
	('9874563239','Δημητριάδη','Αντάρτικα 20',1989),
	('9874563240','Δημητριάδη','Αντάρτικα 21',1989),
	('9874563241','Δημητριάδη','Αντάρτικα 22',1989),
	('9874563242','Δημητριάδη','Αντάρτικα 23',1989),
	('9874563243','Δημητριάδη','Αντάρτικα 23',1989);
ALTER TABLE `patient` ENABLE KEYS;
UNLOCK TABLES;


LOCK TABLES `nosileia` WRITE;
ALTER TABLE `nosileia` DISABLE KEYS;
INSERT INTO `nosileia` (`nosileia_id`, `patient`, `clinic`, `startdate`, `days`) VALUES 
	(1,'9874563217',1,'2014-07-01',5),
	(2,'9874563218',1,'2014-06-01',3),
	(3,'9874563219',1,'2014-07-07',5),
	(4,'9874563221',2,'2014-07-08',2),
	(5,'9874563222',3,'2014-07-09',1),
	(6,'9874563223',4,'2014-07-10',4),
	(7,'9874563224',5,'2014-07-11',5),
	(8,'9874563225',6,'2014-07-12',53),
	(9,'9874563226',1,'2014-07-13',14),
	(10,'9874563227',1,'2014-07-15',12),
	(11,'9874563228',4,'2014-07-15',13),
	(12,'9874563229',6,'2014-07-15',11),
	(13,'9874563230',6,'2014-07-15',16),
	(14,'9874563231',6,'2014-07-15',14),
	(15,'9874563232',5,'2014-07-15',15),
	(16,'9874563233',1,'2014-07-15',5),
	(17,'9874563234',2,'2014-07-15',35),
	(18,'9874563235',3,'2014-07-15',535),
	(19,'9874563236',2,'2014-07-15',535),
	(20,'9874563237',1,'2014-07-15',13),
	(21,'9874563238',4,'2014-07-15',15),
	(22,'9874563240',4,'2014-07-15',122),
	(23,'9874563241',5,'2014-07-07',35),
	(24,'9874563242',6,'2014-07-07',156),
	(25,'9874563243',6,'2014-07-07',115);
ALTER TABLE `nosileia` ENABLE KEYS;
UNLOCK TABLES;


LOCK TABLES `test` WRITE;
ALTER TABLE `test` DISABLE KEYS;
INSERT INTO `test` (`counter`, `string`) VALUES 
	(NULL,'Hello3'),
	(NULL,'Hello3'),
	(NULL,'Hello3'),
	(NULL,'Hello3'),
	(NULL,'Hello3'),
	(NULL,'Hello3'),
	(NULL,'Hello3'),
	(NULL,'Hello3'),
	(NULL,'Hello3'),
	(NULL,'Hello3'),
	(NULL,'Hello3'),
	(NULL,'Hello3'),
	(NULL,'Hello3'),
	(NULL,'Hello3'),
	(NULL,'Hello3'),
	(NULL,'Hello3'),
	(NULL,'Hello3'),
	(NULL,'Hello3'),
	(NULL,'Hello3'),
	(NULL,'Hello3'),
	(NULL,'Hello3'),
	(NULL,'Hello3'),
	(NULL,'Hello3');
ALTER TABLE `test` ENABLE KEYS;
UNLOCK TABLES;




SET FOREIGN_KEY_CHECKS = @PREVIOUS_FOREIGN_KEY_CHECKS;


