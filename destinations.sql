-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Host: mariadb
-- Generation Time: Mar 17, 2026 at 12:09 PM
-- Server version: 10.6.20-MariaDB-ubu2004
-- PHP Version: 8.3.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `2026_1_travel`
--

-- --------------------------------------------------------

--
-- Table structure for table `destinations`
--

CREATE TABLE `destinations` (
  `destination_pk` char(32) NOT NULL,
  `destination_user_fk` char(32) NOT NULL,
  `destination_title` varchar(100) NOT NULL,
  `destination_date_from` bigint(20) UNSIGNED NOT NULL,
  `destination_date_to` bigint(20) UNSIGNED NOT NULL,
  `destination_description` text DEFAULT NULL,
  `destination_location` varchar(100) NOT NULL COMMENT '\r\n',
  `destination_country` varchar(100) NOT NULL,
  `destination_created_at` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `destinations`
--

INSERT INTO `destinations` (`destination_pk`, `destination_user_fk`, `destination_title`, `destination_date_from`, `destination_date_to`, `destination_description`, `destination_location`, `destination_country`, `destination_created_at`) VALUES
('690d11023f0d4bd897f5c736c9a7b21f', 'b373d85d19354407bf1bd804ece22667', 'France from Hell', 1773273600, 1773792000, 'great trip', 'Madrid', 'Spain', 1773232959),
('b5ca489c7f3042bcafde77147a84ed21', 'test_user', 'Trip to Paris', 1773091676, 1791581332, 'Lovely trip', 'Bombay', 'France', 1773093227);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `destinations`
--
ALTER TABLE `destinations`
  ADD PRIMARY KEY (`destination_pk`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
