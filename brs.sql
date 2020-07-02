-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: May 07, 2020 at 12:36 AM
-- Server version: 10.1.36-MariaDB
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
 CREATE DATABASE brs;
 USE brs;
--

-- --------------------------------------------------------
--
-- Table structure for table 'rules'
--

 CREATE TABLE `rules` (
 	`rule_id` varchar(20) NOT NULL,
 	`fact` varchar(50) NOT NULL,
 	`operator` varchar(50) NOT NULL,
 	`value` varchar(50) NOT NULL,
 	`type` varchar(50) NOT NULL,
 	`message` varchar(50) NOT NULL
 )ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `rules`
--

 INSERT INTO `rules` (`rule_id`,`fact`,`operator`,`value`,`type`,`message`) VALUES
 ('R101','category','equal','Electronics','booking','increment 0.25 star');

--
-- Table structure for table `cancel_details`
--

CREATE TABLE `cancel_details` (
  `o_id` varchar(50) NOT NULL,
  `cancel_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `reason` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


--
-- Dumping data for table `cancel_details`
--

-- INSERT INTO `cancel_details` (`o_id`, `cancel_date`, `reason`) VALUES
-- ('A100', '2020-05-06 22:35:41', 1);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--


CREATE TABLE `orders` (
  `o_id` varchar(50) NOT NULL,
  `u_id` int(50) UNSIGNED NOT NULL,
  `p_id` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



--
-- Dumping data for table `orders`
--


INSERT INTO `orders` (`o_id`, `u_id`, `p_id`) VALUES
('A100', 100000, 'P101'),
('A101', 100001, 'P102');

-- --------------------------------------------------------

--
-- Table structure for table `order_details`
--


CREATE TABLE `order_details` (
  `o_id` varchar(50) NOT NULL,
  `order_status` ENUM('in_progress', 'delivered', 'cancelled') default 'in_progress',
  `book_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `exp_del_date` timestamp NULL DEFAULT NULL,
  `del_date` timestamp NULL DEFAULT NULL
   
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `order_details`
--
INSERT INTO `order_details` (`o_id`, `order_status`, `book_date`, `exp_del_date`, `del_date`) VALUES
('A100', 'in_progress', '2020-05-06 22:29:14', '2020-05-11 22:29:14', NULL),
('A101', 'in_progress', '2020-05-06 22:35:41', '2020-05-11 22:30:13', NULL);

------------------------------------------------------

--
-- Table structure for table `payment_info`
--
CREATE TABLE `payment_info`(
  `o_id` varchar(50) NOT NULL,
  `pay_id` varchar(50) NOT NULL,
  `pay_method` ENUM('COD','Debit_card','Credit_card','Paytm') default 'COD'
)ENGINE=InnoDB DEFAULT CHARSET=latin1;


--
-- Dumping data for table `payment_info`
--

INSERT INTO `payment_info` (`o_id`, `pay_id`, `pay_method`) VALUES
('A100', '1111', 'COD'),
('A101', '1112', 'Debit_card');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `p_id` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` varchar(200) NOT NULL,
  `price` varchar(50) NOT NULL,
  `category` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
--
-- Dumping data for table `products`
--

INSERT INTO `products` (`p_id`, `name`, `description`, `price`, `category`) VALUES
('P101', 'MiA1', 'Android smartphone', '16000', 'Electronics'),
('P102', 'X11', 'iPhone', '70000', 'Electronics'),
('P103', 'boatRockerz', 'boat earphones', '1900', 'Electronics'),
('P104', 'Blue jeans', 'Zara navy blue jeans', '1900', 'Clothing'),
('P105', 'Salwar kameez', 'Dazzle red salwar kameez', '3000', 'Clothing');

-- --------------------------------------------------------

--
-- Table structure for table `User`
--


CREATE TABLE `User` (
  `user_id` int(50) UNSIGNED NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(15) NOT NULL,
  `address` varchar(200) NOT NULL,
  `rating` varchar(5) NOT NULL DEFAULT '3',
  `cod` varchar(10) NOT NULL DEFAULT 'yes',
  `coupon` varchar(10) NOT NULL DEFAULT 'no'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


--
-- Dumping data for table `User`
--


INSERT INTO `User` (`user_id`, `name`, `email`, `password`, `address`, `rating` ,`cod` , `coupon`) VALUES
(100000, 'abc', 'abc@gmail.com', 'pwd123', 'Blore', '3' , 'yes' , 'no'),
(100001, 'abc1', 'abc1@gmail.com', 'pwd123', 'Blore', '3' , 'yes' , 'no'),
(100002, 'abc2', 'abc2@gmail.com', 'pwd123', 'Blore', '3' , 'yes' , 'no'),
(100003, 'abc3', 'abc3@gmail.com', 'pwd123', 'Blore', '3' , 'yes' , 'no'),
(100004, 'abc4', 'abc4@gmail.com', 'pwd123', 'Blore', '3' , 'yes' , 'no'),
(100005, 'abc5', 'abc5@gmail.com', 'pwd123', 'Blore', '3' , 'yes' , 'no'),
(100006, 'abc6', 'abc6@gmail.com', 'pwd123', 'Blore', '3' , 'yes' , 'no');








--
-- Indexes for dumped tables
--

--
-- Indexes for table `cancel_details`
--

ALTER TABLE `cancel_details`
  ADD PRIMARY KEY (`o_id`);

--
-- Indexes for table `orders`
--

ALTER TABLE `orders`
  ADD PRIMARY KEY (`o_id`),
  ADD KEY `u_id` (`u_id`),
  ADD KEY `p_id` (`p_id`);

--
-- Indexes for table `order_details`
--
ALTER TABLE `order_details`
  ADD PRIMARY KEY (`o_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`p_id`);

--
-- Indexes for table `User`
--

ALTER TABLE `User`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `payment_info`
--

ALTER TABLE `payment_info`
  ADD PRIMARY KEY (`pay_id`);



ALTER TABLE `User`
  MODIFY `user_id` int(50) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;



--
-- Constraints for dumped tables
--
--
-- Constraints for table `cancel_details`
--
ALTER TABLE `cancel_details`
  ADD CONSTRAINT `cancel_details_ibfk_1` FOREIGN KEY (`o_id`) REFERENCES `orders` (`o_id`);

--
-- Constraints for table `orders`
--

ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`u_id`) REFERENCES `User` (`user_id`),
  ADD CONSTRAINT `orders_ibfk_3` FOREIGN KEY (`p_id`) REFERENCES `products` (`p_id`);

--
-- Constraints for table `order_details`
--
ALTER TABLE `order_details`
  ADD CONSTRAINT `order_details_ibfk_1` FOREIGN KEY (`o_id`) REFERENCES `orders` (`o_id`);

--
-- Constraints for table `payment_info`
--
 ALTER TABLE `payment_info`
  ADD CONSTRAINT `payment_info_ibfk_1` FOREIGN KEY (`o_id`) REFERENCES `orders` (`o_id`);
COMMIT;



/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
