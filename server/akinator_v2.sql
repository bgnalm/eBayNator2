-- phpMyAdmin SQL Dump
-- version 4.1.4
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Nov 22, 2015 at 03:38 AM
-- Server version: 5.6.15-log
-- PHP Version: 5.5.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `akinator_v2`
--

-- --------------------------------------------------------

--
-- Table structure for table `answers`
--

CREATE TABLE IF NOT EXISTS `answers` (
  `item_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `q1` float NOT NULL DEFAULT '0.5',
  `q2` float NOT NULL DEFAULT '0.5',
  `q3` float NOT NULL DEFAULT '0.5',
  `q4` float NOT NULL DEFAULT '0.5',
  `q5` float NOT NULL DEFAULT '0.5',
  PRIMARY KEY (`item_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `answers`
--

INSERT INTO `answers` (`item_id`, `q1`, `q2`, `q3`, `q4`, `q5`) VALUES
(1, 1, 0.1, 0.75, 1, 0.8),
(2, 1, 0.2, 0.76, 0, 0.6),
(3, 1, 0.5, 0.6, 0, 0.2),
(4, 0, 0.01, 0.5, 0, 0.1);

-- --------------------------------------------------------

--
-- Table structure for table `items`
--

CREATE TABLE IF NOT EXISTS `items` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `date_added` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `time_played` int(10) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6 ;

--
-- Dumping data for table `items`
--

INSERT INTO `items` (`id`, `name`, `date_added`, `time_played`) VALUES
(1, 'Iphone 5', '2015-11-20 20:39:00', 1),
(2, 'Nexus 4', '2015-11-20 20:39:56', 1),
(3, 'Dell Screen', '2015-11-20 20:40:11', 1),
(4, 'The 7 Habits of highly effective people by steven covey', '2015-11-20 20:40:53', 1);

-- --------------------------------------------------------

--
-- Table structure for table `questions`
--

CREATE TABLE IF NOT EXISTS `questions` (
  `question_id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(150) NOT NULL,
  `time_added` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`question_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7 ;

--
-- Dumping data for table `questions`
--

INSERT INTO `questions` (`question_id`, `text`, `time_added`) VALUES
(1, 'Is the item electronic?', '2015-11-20 20:26:18'),
(2, 'Is the item heavy?', '2015-11-20 20:26:33'),
(3, 'Is the item expensive?', '2015-11-20 20:26:43'),
(4, 'Is the item made by Apple?', '2015-11-20 20:26:57'),
(5, 'Do people use item often?', '2015-11-20 20:27:20');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
