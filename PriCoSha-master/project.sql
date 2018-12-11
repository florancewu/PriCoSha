-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Dec 11, 2018 at 06:33 AM
-- Server version: 5.7.23
-- PHP Version: 7.2.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `project`
--

-- --------------------------------------------------------

--
-- Table structure for table `belong`
--

DROP TABLE IF EXISTS `belong`;
CREATE TABLE IF NOT EXISTS `belong` (
  `email` varchar(20) NOT NULL,
  `owner_email` varchar(20) NOT NULL,
  `fg_name` varchar(20) NOT NULL,
  PRIMARY KEY (`email`,`owner_email`,`fg_name`),
  KEY `owner_email` (`owner_email`,`fg_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
CREATE TABLE IF NOT EXISTS `comment` (
  `item_id` int(11) NOT NULL,
  `email` varchar(50) NOT NULL,
  `post_time` timestamp NOT NULL,
  `comment_text` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`item_id`,`email`,`post_time`),
  KEY `email` (`email`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `comment`
--

INSERT INTO `comment` (`item_id`, `email`, `post_time`, `comment_text`) VALUES
(7, 'fw@nyu.edu', '2018-12-10 23:40:06', 'Wow');

-- --------------------------------------------------------

--
-- Table structure for table `contentitem`
--

DROP TABLE IF EXISTS `contentitem`;
CREATE TABLE IF NOT EXISTS `contentitem` (
  `item_id` int(11) NOT NULL AUTO_INCREMENT,
  `email_post` varchar(20) DEFAULT NULL,
  `post_time` timestamp NULL DEFAULT NULL,
  `file_path` varchar(100) DEFAULT NULL,
  `item_name` varchar(20) DEFAULT NULL,
  `is_pub` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`item_id`),
  KEY `email_post` (`email_post`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `contentitem`
--

INSERT INTO `contentitem` (`item_id`, `email_post`, `post_time`, `file_path`, `item_name`, `is_pub`) VALUES
(7, 'fw@nyu.edu', '2018-12-10 23:02:39', NULL, 'Hello Flo', 1);

-- --------------------------------------------------------

--
-- Table structure for table `friendgroup`
--

DROP TABLE IF EXISTS `friendgroup`;
CREATE TABLE IF NOT EXISTS `friendgroup` (
  `owner_email` varchar(20) NOT NULL,
  `fg_name` varchar(20) NOT NULL,
  `description` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`owner_email`,`fg_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `friendgroup`
--

INSERT INTO `friendgroup` (`owner_email`, `fg_name`, `description`) VALUES
('fw@nyu.edu', 'NYU Group Friends', 'NYU Group Friends'),
('fw@nyu.edu', 'NYU', 'School'),
('fw@nyu.edu', 'My Friends', 'My group of friends');

-- --------------------------------------------------------

--
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
CREATE TABLE IF NOT EXISTS `member` (
  `email` varchar(20) NOT NULL,
  `fg_name` varchar(20) NOT NULL,
  `owner_email` varchar(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `member`
--

INSERT INTO `member` (`email`, `fg_name`, `owner_email`) VALUES
('al@nyu.edu', 'NYU Group Friends', 'fw@nyu.edu'),
('al@nyu.edu', 'NYU', 'fw@nyu.edu');

-- --------------------------------------------------------

--
-- Table structure for table `person`
--

DROP TABLE IF EXISTS `person`;
CREATE TABLE IF NOT EXISTS `person` (
  `email` varchar(20) NOT NULL,
  `password` char(64) DEFAULT NULL,
  `fname` varchar(20) DEFAULT NULL,
  `lname` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`email`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `person`
--

INSERT INTO `person` (`email`, `password`, `fname`, `lname`) VALUES
('fw@nyu.edu', '12345', 'florance', 'wu'),
('al@nyu.edu', '12345', 'Alex', 'Lin');

-- --------------------------------------------------------

--
-- Table structure for table `rate`
--

DROP TABLE IF EXISTS `rate`;
CREATE TABLE IF NOT EXISTS `rate` (
  `email` varchar(20) NOT NULL,
  `item_id` int(11) NOT NULL,
  `rate_time` timestamp NULL DEFAULT NULL,
  `emoji` varchar(20) CHARACTER SET utf8mb4 DEFAULT NULL,
  PRIMARY KEY (`email`,`item_id`),
  KEY `item_id` (`item_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `share`
--

DROP TABLE IF EXISTS `share`;
CREATE TABLE IF NOT EXISTS `share` (
  `owner_email` varchar(20) NOT NULL,
  `fg_name` varchar(20) NOT NULL,
  `item_id` int(11) NOT NULL,
  PRIMARY KEY (`owner_email`,`fg_name`,`item_id`),
  KEY `item_id` (`item_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `share`
--

INSERT INTO `share` (`owner_email`, `fg_name`, `item_id`) VALUES
('fw@nyu.edu', 'My Friends', 7),
('fw@nyu.edu', 'NYU', 7);

-- --------------------------------------------------------

--
-- Table structure for table `tag`
--

DROP TABLE IF EXISTS `tag`;
CREATE TABLE IF NOT EXISTS `tag` (
  `email_tagged` varchar(20) NOT NULL,
  `email_tagger` varchar(20) NOT NULL,
  `item_id` int(11) NOT NULL,
  `status` varchar(20) DEFAULT NULL,
  `tagtime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`email_tagged`,`email_tagger`,`item_id`),
  KEY `email_tagger` (`email_tagger`),
  KEY `item_id` (`item_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `tag`
--

INSERT INTO `tag` (`email_tagged`, `email_tagger`, `item_id`, `status`, `tagtime`) VALUES
('fw@nyu.edu', 'fw@nyu.edu', 7, '1', '2018-12-10 23:06:17'),
('al@nyu.edu', 'fw@nyu.edu', 7, '0', '2018-12-10 23:06:44');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
