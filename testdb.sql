-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 06, 2024 at 08:39 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `my_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `Course`
--

CREATE TABLE `Course` (
  `ID` int(8) NOT NULL,
  `Name` varchar(50) NOT NULL,
  `Credit` int(1) NOT NULL,
  `Required` tinyint(1) NOT NULL,
  `Quota` int(3) NOT NULL,
  `Dept` varchar(4) NOT NULL,
  `Year` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Course_Info';

--
-- Dumping data for table `Course`
--

INSERT INTO `Course` (`ID`, `Name`, `Credit`, `Required`, `Quota`, `Dept`, `Year`) VALUES
(1, 'Programme', 2, 1, 80, 'IECS', 1),
(2, 'Computer_Theroerm', 2, 1, 80, 'IECS', 1),
(3, '0_quota', 3, 0, 0, 'IECS', 1),
(4, 'English_advanced', 3, 1, 25, 'LANG', 2),
(5, 'Assembly', 3, 1, 80, 'IECS', 2),
(6, 'DBMS', 3, 1, 80, 'IECS', 2),
(7, 'FYP', 30, 1, 200, 'IECS', 3),
(8, 'Linear Algebra', 3, 1, 100, 'IECS', 1),
(9, 'Calcus(I)', 3, 1, 110, 'IECS', 1),
(10, 'Wireless Network', 3, 0, 50, 'IECS', 4),
(11, 'Software Testing', 3, 0, 70, 'IECS', 2),
(12, 'OOP', 3, 0, 60, 'IECS', 2);

-- --------------------------------------------------------

--
-- Table structure for table `Student`
--

CREATE TABLE `Student` (
  `ID` int(8) NOT NULL,
  `First_Name` varchar(50) NOT NULL,
  `Last_Name` varchar(50) NOT NULL,
  `Year` int(1) NOT NULL,
  `Dept` varchar(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Student Info';

--
-- Dumping data for table `Student`
--

INSERT INTO `Student` (`ID`, `First_Name`, `Last_Name`, `Year`, `Dept`) VALUES
(12345678, 'Peter', 'Chan', 1, 'IECS');

-- --------------------------------------------------------

--
-- Table structure for table `Subscription`
--

CREATE TABLE `Subscription` (
  `s_id` int(8) NOT NULL,
  `c_id` int(8) NOT NULL,
  `type` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Subscription`
--

INSERT INTO `Subscription` (`s_id`, `c_id`, `type`) VALUES
(12345678, 1, 1),
(12345678, 2, 1),
(12345678, 5, 1),
(12345678, 8, 1),
(12345678, 9, 1),
(12345678, 10, 1),
(12345678, 11, 1);

-- --------------------------------------------------------

--
-- Table structure for table `TimeTable`
--

CREATE TABLE `TimeTable` (
  `ID` int(8) NOT NULL,
  `Day` int(1) NOT NULL,
  `Section` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `TimeTable`
--

INSERT INTO `TimeTable` (`ID`, `Day`, `Section`) VALUES
(1, 2, 3),
(1, 2, 4),
(2, 2, 6),
(2, 2, 7),
(3, 1, 1),
(4, 1, 4),
(5, 3, 3),
(5, 3, 4),
(5, 3, 5),
(6, 2, 3),
(6, 2, 4),
(6, 2, 5),
(7, 5, 11),
(8, 2, 8),
(8, 2, 9),
(8, 2, 10),
(9, 5, 4),
(9, 5, 5),
(9, 5, 6),
(10, 3, 6),
(10, 3, 7),
(10, 3, 8),
(11, 1, 5),
(11, 1, 6),
(11, 1, 7),
(12, 3, 3),
(12, 3, 4),
(12, 3, 5),
(12, 3, 6);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Course`
--
ALTER TABLE `Course`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `Student`
--
ALTER TABLE `Student`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `Subscription`
--
ALTER TABLE `Subscription`
  ADD PRIMARY KEY (`s_id`,`c_id`);

--
-- Indexes for table `TimeTable`
--
ALTER TABLE `TimeTable`
  ADD PRIMARY KEY (`ID`,`Day`,`Section`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Course`
--
ALTER TABLE `Course`
  MODIFY `ID` int(8) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
