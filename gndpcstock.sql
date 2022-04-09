-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 08, 2020 at 07:11 AM
-- Server version: 10.4.8-MariaDB
-- PHP Version: 7.3.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `gndpcstock`
--

-- --------------------------------------------------------

--
-- Table structure for table `conty`
--

CREATE TABLE `conty` (
  `S_no` int(15) NOT NULL,
  `Date` text COLLATE latin1_general_cs NOT NULL,
  `Item_name` varchar(200) COLLATE latin1_general_cs NOT NULL,
  `Quantity` int(15) NOT NULL,
  `Address` varchar(1000) COLLATE latin1_general_cs NOT NULL,
  `Bill_no` int(15) NOT NULL,
  `Without_gst` float NOT NULL,
  `GST` int(15) NOT NULL,
  `Total_amount` float NOT NULL,
  `Deleted_date` text COLLATE latin1_general_cs NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_cs;

--
-- Dumping data for table `conty`
--

INSERT INTO `conty` (`S_no`, `Date`, `Item_name`, `Quantity`, `Address`, `Bill_no`, `Without_gst`, `GST`, `Total_amount`, `Deleted_date`) VALUES
(1, '05-08-19', 'js', 20, 'kasndann', 200, 84.7458, 18, 100, ''),
(2, '03-10-19', 'abc,pen,chair,fan', 0, 'gill', 1222, 203.39, 18, 240, ''),
(3, '12-10-19', 'abujs', 23, 'gill', 1242, 194.915, 18, 230, '12-10-19'),
(4, '12-10-19', 'jaks', 23, 'gill', 1242, 194.915, 18, 230, '12-10-19'),
(5, '17-10-19', '', 50, 'abc', 101, 42.3729, 18, 50, ''),
(6, '17-10-19', 'b', 50, 'abc', 101, 42.3729, 18, 50, ''),
(7, '17-10-19', 'c', 50, 'abc', 101, 42.3729, 18, 50, '');

-- --------------------------------------------------------

--
-- Table structure for table `issue`
--

CREATE TABLE `issue` (
  `S_No` int(10) NOT NULL,
  `Date` text COLLATE latin1_general_cs NOT NULL,
  `Time` time NOT NULL,
  `Dept_Name` varchar(100) COLLATE latin1_general_cs NOT NULL,
  `Item_Name` varchar(100) COLLATE latin1_general_cs NOT NULL,
  `Item_pieces` int(20) NOT NULL,
  `Name` varchar(100) COLLATE latin1_general_cs NOT NULL,
  `Phone_No` bigint(20) NOT NULL,
  `Deleted_date` text COLLATE latin1_general_cs NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_cs;

--
-- Dumping data for table `issue`
--

INSERT INTO `issue` (`S_No`, `Date`, `Time`, `Dept_Name`, `Item_Name`, `Item_pieces`, `Name`, `Phone_No`, `Deleted_date`) VALUES
(1, '19-08-2018', '11:08:07', 'comp', 'pump', 5, 'aman', 8427406998, ''),
(2, '19-08-2018', '07:40:04', 'Fence Desighning', 'fan', 10, 'kndkjw', 834638756837, ' '),
(3, '20-08-2018', '07:57:58', 'Welding & Steel Fabrication', 'fans', 10, 'js', 9347289474, ''),
(4, '21-08-2018', '10:04:21', 'Computer Applications', 'book', 5, 'jaspreet', 1234567895, ''),
(5, '22-08-2018', '10:48:39', 'Computer Applications', 'chair', 50, 'jbub', 51561651651, ''),
(7, '08-07-2020', '10:37:46', 'Refrigeration/Air conditioning', 'abc', 2, 'Rajwinder', 8425374288, '');

-- --------------------------------------------------------

--
-- Table structure for table `stock`
--

CREATE TABLE `stock` (
  `S_No` int(10) NOT NULL,
  `Date` text COLLATE latin1_general_cs NOT NULL,
  `Item_name` varchar(50) COLLATE latin1_general_cs NOT NULL,
  `Total_Items` int(10) NOT NULL,
  `Issue` int(10) NOT NULL,
  `Balance` int(10) NOT NULL,
  `Address` varchar(1000) COLLATE latin1_general_cs NOT NULL,
  `Bill_no` int(20) NOT NULL,
  `Amount` float NOT NULL,
  `GST` int(11) NOT NULL,
  `GST_Amt` float NOT NULL,
  `Without_GST` float NOT NULL,
  `Department` text COLLATE latin1_general_cs NOT NULL,
  `Deleted_date` text COLLATE latin1_general_cs NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_cs;

--
-- Dumping data for table `stock`
--

INSERT INTO `stock` (`S_No`, `Date`, `Item_name`, `Total_Items`, `Issue`, `Balance`, `Address`, `Bill_no`, `Amount`, `GST`, `GST_Amt`, `Without_GST`, `Department`, `Deleted_date`) VALUES
(1, '05-08-2019', 'books', 50, 0, 50, 'kenkfkj', 100, 100, 18, 15.2542, 84.7458, 'stationary', ' '),
(2, '05-08-2019', 'abc', 40, 2, 18, 'ksald', 100, 100, 5, 4.7619, 95.2381, 'asset', ''),
(3, '05-08-2019', 'fans', 50, 10, 40, 'kasnda', 201, 1000, 18, 152.542, 847.458, 'asset', ''),
(4, '05-08-2019', 'pen', 20, 0, 20, 'sadkajkk', 120, 100, 5, 4.7619, 95.2381, 'stationary', ''),
(5, '05-08-2019', 'abc', 40, 2, 18, 'jbdkbkjs', 102, 100, 18, 15.2542, 84.7458, 'stationary', '15-09-19'),
(6, '08-08-2019', 'PUMP', 25, 0, 25, 'GILL CHOWNK', 1006, 520, 18, 79.322, 440.678, 'asset', '09-10-19'),
(7, '10-08-2019', 'book', 15, 5, 10, 'dugri', 1008, 950, 18, 144.915, 805.085, 'asset', '10-08-19'),
(8, '13-08-2019', 'pump', 25, 2, 23, 'gill', 1005, 560, 5, 26.6667, 533.333, 'asset', '13-08-19'),
(9, '19-08-2019', 'pen', 67, 0, 67, 'dfgd', 164, 170, 5, 8.09524, 161.905, 'stationary', ''),
(10, '25-08-2019', 'zzz', 56, 0, 56, 'sdsdf', 547, 578, 18, 88.1695, 489.831, 'stationary', '10-10-19'),
(11, '25-08-2019', 'books', 100, 0, 100, 'kenkfkj', 100, 100, 18, 15.2542, 84.7458, 'stationary', ''),
(12, '25-08-2019', 'abc', 20, 2, 18, 'sadkajkk', 120, 100, 5, 4.7619, 95.2381, 'asset', ''),
(13, '26-08-2019', 'fans', 500, 0, 500, 'kasnda', 201, 1000, 18, 152.542, 847.458, 'asset', ' '),
(14, '26-08-2019', 'ac', 5, 0, 5, 'dugri gungianvehar', 123, 7000, 18, 1067.8, 5932.2, 'asset', '10-05-2020');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `conty`
--
ALTER TABLE `conty`
  ADD PRIMARY KEY (`S_no`);

--
-- Indexes for table `issue`
--
ALTER TABLE `issue`
  ADD PRIMARY KEY (`S_No`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `conty`
--
ALTER TABLE `conty`
  MODIFY `S_no` int(15) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- AUTO_INCREMENT for table `issue`
--
ALTER TABLE `issue`
  MODIFY `S_No` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
