-- SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
-- SET AUTOCOMMIT = 0;
-- START TRANSACTION;
-- SET time_zone = "+00:00";


-- /*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
-- /*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
-- /*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
-- /*!40101 SET NAMES utf8mb4 */;

-- --
-- -- Database: `catalogue`
-- --
-- CREATE DATABASE IF NOT EXISTS `catalogue` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
-- USE `catalogue`;

-- -- --------------------------------------------------------

-- --
-- -- Table structure for table `brokers`
-- --

-- DROP TABLE IF EXISTS `brokers`;
-- CREATE TABLE IF NOT EXISTS `brokers` (
--   `P_id` int(255) NOT NULL AUTO_INCREMENT,
--   `company` varchar(255) NOT NULL,
--   `code` varchar(55) NOT NULL,
--   `postal_address` varchar(255) NOT NULL,
--   `telephone` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`telephone`)),
--   `email_address` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`email_address`)),
--   `location` varchar(255) DEFAULT NULL,
--   `fax` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`fax`)),
--   PRIMARY KEY (`P_id`),
--   UNIQUE KEY `company_code` (`code`)
-- ) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- -- --------------------------------------------------------

-- --
-- -- Table structure for table `buyers`
-- --

-- DROP TABLE IF EXISTS `buyers`;
-- CREATE TABLE IF NOT EXISTS `buyers` (
--   `P_id` int(11) NOT NULL AUTO_INCREMENT,
--   `company` varchar(255) NOT NULL,
--   `code` varchar(55) NOT NULL,
--   `postal_address` varchar(255) NOT NULL,
--   `telephone` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`telephone`)),
--   `email_address` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`email_address`)),
--   `location` varchar(255) DEFAULT NULL,
--   `fax` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`fax`)),
--   PRIMARY KEY (`P_id`),
--   UNIQUE KEY `company_code` (`code`)
-- ) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- -- --------------------------------------------------------

-- --
-- -- Table structure for table `producers`
-- --

-- DROP TABLE IF EXISTS `producers`;
-- CREATE TABLE IF NOT EXISTS `producers` (
--   `P_id` int(255) NOT NULL AUTO_INCREMENT,
--   `company` varchar(255) NOT NULL,
--   `code` varchar(55) NOT NULL,
--   `postal_address` varchar(255) NOT NULL,
--   `telephone` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`telephone`)),
--   `email_address` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`email_address`)),
--   `country` varchar(55) NOT NULL,
--   `location` varchar(255) DEFAULT NULL,
--   `fax` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`fax`)),
--   PRIMARY KEY (`P_id`),
--   UNIQUE KEY `company_code` (`code`)
-- ) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- -- --------------------------------------------------------

-- --
-- -- Table structure for table `teagrades`
-- --

-- DROP TABLE IF EXISTS `teagrades`;
-- CREATE TABLE IF NOT EXISTS `teagrades` (
--   `P_id` int(255) NOT NULL AUTO_INCREMENT,
--   `type` varchar(55) NOT NULL,
--   `class` varchar(55) NOT NULL,
--   `grade` varchar(55) NOT NULL,
--   `packages` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`packages`)),
--   `package_type` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`package_type`)),
--   PRIMARY KEY (`P_id`)
-- ) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- -- --------------------------------------------------------

-- --
-- -- Table structure for table `warehouses`
-- --

-- DROP TABLE IF EXISTS `warehouses`;
-- CREATE TABLE IF NOT EXISTS `warehouses` (
--   `P_id` int(255) NOT NULL AUTO_INCREMENT,
--   `company` varchar(255) NOT NULL,
--   `company_parent` varchar(255) NOT NULL DEFAULT 'self',
--   `code` varchar(55) NOT NULL,
--   `postal_address` varchar(255) DEFAULT NULL,
--   `telephone` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`telephone`)),
--   `email_address` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`email_address`)),
--   `type` varchar(55) NOT NULL DEFAULT 'warehouse',
--   `location` varchar(255) DEFAULT NULL,
--   `fax` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`fax`)),
--   PRIMARY KEY (`P_id`),
--   UNIQUE KEY `company code` (`code`)
-- ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
-- COMMIT;

-- /*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
-- /*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
-- /*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 13, 2022 at 05:55 PM
-- Server version: 10.4.10-MariaDB
-- PHP Version: 7.3.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `catalogue`
--

-- --------------------------------------------------------

--
-- Table structure for table `brokers`
--

DROP TABLE IF EXISTS `brokers`;
CREATE TABLE IF NOT EXISTS `brokers` (
  `P_id` int(255) NOT NULL AUTO_INCREMENT,
  `company` varchar(255) NOT NULL,
  `code` varchar(55) NOT NULL,
  `postal_address` varchar(255) DEFAULT NULL,
  `telephone` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`telephone`)),
  `email_address` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`email_address`)),
  `location` varchar(255) DEFAULT NULL,
  `fax` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`fax`)),
  PRIMARY KEY (`P_id`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `buyers`
--

DROP TABLE IF EXISTS `buyers`;
CREATE TABLE IF NOT EXISTS `buyers` (
  `P_id` int(11) NOT NULL AUTO_INCREMENT,
  `company` varchar(255) NOT NULL,
  `code` varchar(55) NOT NULL,
  `postal_address` varchar(255) NOT NULL,
  `telephone` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`telephone`)),
  `email_address` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`email_address`)),
  `location` varchar(255) DEFAULT NULL,
  `fax` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`fax`)),
  PRIMARY KEY (`P_id`)
) ENGINE=MyISAM AUTO_INCREMENT=96 DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `invoice_number`
--

DROP TABLE IF EXISTS `invoice_number`;
CREATE TABLE IF NOT EXISTS `invoice_number` (
  `number` int(55) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `invoice_number`
--

INSERT INTO `invoice_number` (`number`) VALUES
(1);


--
-- Dumping data for table `invoice_number`
--

-- INSERT INTO `account_sale_number` (`number`) VALUES
-- (1);

-- --------------------------------------------------------

--
-- Table structure for table `lot_number`
--

-- DROP TABLE IF EXISTS `lot_number`;
-- CREATE TABLE IF NOT EXISTS `lot_number` (
--   `number` int(55) NOT NULL
-- ) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `lot_number`
--

-- INSERT INTO `lot_number` (`number`) VALUES
-- (23000);

-- --------------------------------------------------------

--
-- Table structure for table `producers`
--

DROP TABLE IF EXISTS `producers`;
CREATE TABLE IF NOT EXISTS `producers` (
  `P_id` int(255) NOT NULL AUTO_INCREMENT,
  `company` varchar(255) NOT NULL,
  `code` varchar(55) NOT NULL,
  `mark` varchar(55) NOT NULL,
  `postal_address` varchar(255) DEFAULT NULL,
  `telephone` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `email_address` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `country` varchar(55) NOT NULL,
  `location` varchar(255) DEFAULT NULL,
  `fax` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`fax`)),
  `warehouse` varchar(255) DEFAULT NULL,
  `warehouse_code` varchar(55) DEFAULT NULL,
  PRIMARY KEY (`P_id`)
) ENGINE=MyISAM AUTO_INCREMENT=187 DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `teagrades`
--

DROP TABLE IF EXISTS `teagrades`;
CREATE TABLE IF NOT EXISTS `teagrades` (
  `P_id` int(255) NOT NULL AUTO_INCREMENT,
  `type` varchar(55) NOT NULL,
  `class` varchar(55) NOT NULL,
  `grade` varchar(55) NOT NULL,
  `packages` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`packages`)),
  `package_type` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`package_type`)),
  PRIMARY KEY (`P_id`)
) ENGINE=MyISAM AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `teagrades`
--

INSERT INTO `teagrades` (`P_id`, `type`, `class`, `grade`, `packages`, `package_type`) VALUES
(1, 'primary', 'CTC', 'BP1', '[40,60]', '[\"TPP\"]'),
(2, 'primary', 'CTC', 'PF1', '[40,60]', '[\"TPP\"]'),
(3, 'primary', 'CTC', 'PD', '[40,60]', '[\"TPP\"]'),
(4, 'primary', 'CTC', 'DUST1', '[40,60]', '[\"TPP\"]'),
(5, 'secondary', 'CTC', 'BP', '[20]', '[\"PB\"]'),
(6, 'secondary', 'CTC', 'PF', '[20]', '[\"PB\",\"TPP\"]'),
(7, 'secondary', 'CTC', 'PF2', '[20]', '[\"PB\"]'),
(8, 'secondary', 'CTC', 'FNGS1', '[20]', '[\"PB\"]'),
(9, 'secondary', 'CTC', 'FNGS', '[20]', '[\"PB\"]'),
(10, 'secondary', 'CTC', 'DUST', '[20]', '[\"PB\"]'),
(11, 'secondary', 'CTC', 'DUST2', '[20]', '[\"PB\"]'),
(12, 'secondary', 'CTC', 'BMF', '[20]', '[\"PB\"]'),
(13, 'secondary', 'CTC', 'BMF1', '[20]', '[\"PB\"]'),
(14, '', 'ORTHODOX', 'OPAL', NULL, NULL),
(15, '', 'ORTHODOX', 'OPA', NULL, NULL),
(16, '', 'ORTHODOX', 'GFOP', NULL, NULL),
(17, '', 'ORTHODOX', 'OP', NULL, NULL),
(18, '', 'ORTHODOX', 'OP1', NULL, NULL),
(19, '', 'ORTHODOX', 'FOP', NULL, NULL),
(20, '', 'ORTHODOX', 'PEKOE', NULL, NULL),
(21, '', 'ORTHODOX', 'GFBOP', NULL, NULL),
(22, '', 'ORTHODOX', 'TBOP', NULL, NULL),
(23, '', 'ORTHODOX', 'FOF', NULL, NULL),
(24, '', 'ORTHODOX', 'BOPF', NULL, NULL),
(25, '', 'ORTHODOX', 'BOPD', NULL, NULL),
(26, '', 'ORTHODOX', 'STGFBOP', NULL, NULL),
(27, '', 'ORTHODOX', 'FBOP', NULL, NULL),
(28, '', 'ORTHODOX', 'FBOPFSP', NULL, NULL),
(29, '', 'ORTHODOX', 'GFBOPSP', NULL, NULL),
(30, '', 'ORTHODOX', 'GREEN TEA', NULL, NULL),
(31, '', 'ORTHODOX', 'PURPLE TEA', NULL, NULL),
(32, '', 'ORTHODOX', 'RED TEA', NULL, NULL),
(33, '', 'ORTHODOX', 'OOLONG', NULL, NULL),
(34, 'primary', 'CTC', 'D1', '[40,60]', '[\"TPP\"]');

-- --------------------------------------------------------

--
-- Table structure for table `warehouses`
--

DROP TABLE IF EXISTS `warehouses`;
CREATE TABLE IF NOT EXISTS `warehouses` (
  `P_id` int(255) NOT NULL AUTO_INCREMENT,
  `company` varchar(255) NOT NULL,
  `company_parent` varchar(255) NOT NULL DEFAULT 'self',
  `code` varchar(55) NOT NULL,
  `postal_address` varchar(255) DEFAULT NULL,
  `telephone` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`telephone`)),
  `email_address` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`email_address`)),
  `type` varchar(55) NOT NULL DEFAULT 'warehouse',
  `location` varchar(255) DEFAULT NULL,
  `fax` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`fax`)),
  PRIMARY KEY (`P_id`)
) ENGINE=MyISAM AUTO_INCREMENT=91 DEFAULT CHARSET=utf8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
