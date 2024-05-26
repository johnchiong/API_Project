-- MySQL Administrator dump 1.4
--
-- ------------------------------------------------------
-- Server version	5.0.27-community-nt


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


--
-- Create schema company
--

CREATE DATABASE IF NOT EXISTS company;
USE company;

--
-- Definition of table `department`
--

DROP TABLE IF EXISTS `department`;
CREATE TABLE `department` (
  `Dnumber` int(10) unsigned NOT NULL auto_increment,
  `Dname` varchar(45) NOT NULL,
  `Mgr_ssn` int(10) unsigned NOT NULL,
  `Mgr_start_date` date NOT NULL,
  PRIMARY KEY  (`Dnumber`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `department`
--

/*!40000 ALTER TABLE `department` DISABLE KEYS */;
INSERT INTO `department` (`Dnumber`,`Dname`,`Mgr_ssn`,`Mgr_start_date`) VALUES 
 (1,'Headquarters',888665555,'1981-06-19'),
 (4,'Administration',987654321,'1995-01-01'),
 (5,'Research',333445555,'1988-05-02');
/*!40000 ALTER TABLE `department` ENABLE KEYS */;


--
-- Definition of table `dependent`
--

DROP TABLE IF EXISTS `dependent`;
CREATE TABLE `dependent` (
  `Dep_id` int(10) unsigned NOT NULL auto_increment,
  `Essn` int(10) unsigned NOT NULL,
  `Dependent_name` varchar(45) NOT NULL,
  `Sex` char(1) NOT NULL,
  `Bdate` date NOT NULL,
  `Relationship` varchar(45) NOT NULL,
  PRIMARY KEY  (`Dep_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dependent`
--

/*!40000 ALTER TABLE `dependent` DISABLE KEYS */;
INSERT INTO `dependent` (`Dep_id`,`Essn`,`Dependent_name`,`Sex`,`Bdate`,`Relationship`) VALUES 
 (1,333445555,'Alice','F','1986-04-05','Daughter'),
 (2,333445555,'Theodore','M','1983-10-25','Son'),
 (3,333445555,'Joy','F','1958-05-03','Spouse'),
 (4,987654321,'Abner','M','1942-02-28','Spouse'),
 (5,123456789,'Michael','M','1988-01-04','Son'),
 (6,123456789,'Alice','F','1988-12-30','Daughter'),
 (7,123456789,'Elizabeth','F','1967-05-05','Spouse');
/*!40000 ALTER TABLE `dependent` ENABLE KEYS */;


--
-- Definition of table `dept_locations`
--

DROP TABLE IF EXISTS `dept_locations`;
CREATE TABLE `dept_locations` (
  `DL_id` int(10) unsigned NOT NULL auto_increment,
  `Dnumber` int(10) unsigned NOT NULL,
  `Dlocation` varchar(45) NOT NULL,
  PRIMARY KEY  (`DL_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dept_locations`
--

/*!40000 ALTER TABLE `dept_locations` DISABLE KEYS */;
INSERT INTO `dept_locations` (`DL_id`,`Dnumber`,`Dlocation`) VALUES 
 (1,1,'Houston'),
 (2,4,'Stafford'),
 (3,5,'Bellaire'),
 (4,5,'Sugarland'),
 (5,5,'Houston');
/*!40000 ALTER TABLE `dept_locations` ENABLE KEYS */;


--
-- Definition of table `employee`
--

DROP TABLE IF EXISTS `employee`;
CREATE TABLE `employee` (
  `ssn` int(10) unsigned NOT NULL,
  `Fname` varchar(45) NOT NULL,
  `Minit` char(1) default NULL,
  `Lname` varchar(45) NOT NULL,
  `Bdate` date NOT NULL,
  `Address` varchar(45) NOT NULL,
  `Sex` char(1) NOT NULL,
  `Salary` double NOT NULL,
  `Super_ssn` int(10) unsigned default NULL,
  `DL_id` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`ssn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `employee`
--

/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` (`ssn`,`Fname`,`Minit`,`Lname`,`Bdate`,`Address`,`Sex`,`Salary`,`Super_ssn`,`DL_id`) VALUES 
 (123456789,'John','B','Smith','1965-01-09','731 Fondren, Houston, TX','M',30000,333445555,5),
 (333445555,'Franklin','T','Wong','1955-12-08','638 Voss, Houston, TX','M',40000,888665555,5),
 (453453453,'Joyce','A','English','1972-07-31','5631 Rice, Houston, TX','F',25000,333445555,5),
 (666884444,'Ramesh','K','Narayan','1962-09-15','975 Fire Oak, Humble, TX','M',38000,333445555,5),
 (888665555,'James','E','Borg','1937-11-10','450 Stone, Houston, TX','M',55000,NULL,1),
 (987654321,'Jennifer','S','Wallace','1941-06-20','291 Berry, Bellaire, TX','F',43000,888665555,4),
 (987987987,'Ahmad','V','Jabbar','1969-03-29','980 Dallas, Houston, TX','M',25000,987654321,4),
 (999887777,'Alicia','J','Zelaya','1968-01-19','3321 Castle, Spring, TX','F',25000,987654321,4);
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;


--
-- Definition of table `project`
--

DROP TABLE IF EXISTS `project`;
CREATE TABLE `project` (
  `Pnumber` int(10) unsigned NOT NULL auto_increment,
  `Pname` varchar(45) NOT NULL,
  `DL_id` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`Pnumber`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `project`
--

/*!40000 ALTER TABLE `project` DISABLE KEYS */;
INSERT INTO `project` (`Pnumber`,`Pname`,`DL_id`) VALUES 
 (1,'ProductX',3),
 (2,'ProductY',4),
 (3,'ProductZ',5),
 (10,'Computerization',2),
 (20,'Reorganization',1),
 (30,'Newbenefits',2);
/*!40000 ALTER TABLE `project` ENABLE KEYS */;


--
-- Definition of table `works_on`
--

DROP TABLE IF EXISTS `works_on`;
CREATE TABLE `works_on` (
  `work_id` int(10) unsigned NOT NULL auto_increment,
  `Essn` int(10) unsigned NOT NULL,
  `Pno` int(10) unsigned NOT NULL,
  `Hours` double default NULL,
  PRIMARY KEY  (`work_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `works_on`
--

/*!40000 ALTER TABLE `works_on` DISABLE KEYS */;
INSERT INTO `works_on` (`work_id`,`Essn`,`Pno`,`Hours`) VALUES 
 (1,123456789,1,32.5),
 (2,123456789,2,7.5),
 (3,666884444,3,40),
 (4,453453453,1,20),
 (5,453453453,2,20),
 (6,333445555,2,10),
 (7,333445555,3,10),
 (8,333445555,10,10),
 (9,333445555,20,10),
 (10,999887777,30,30),
 (11,999887777,10,10),
 (12,987987987,10,35),
 (13,987987987,30,5),
 (14,987654321,30,20),
 (15,987654321,20,15),
 (16,888665555,20,NULL);
/*!40000 ALTER TABLE `works_on` ENABLE KEYS */;




/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
