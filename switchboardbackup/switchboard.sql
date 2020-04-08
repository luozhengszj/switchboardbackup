/*
Navicat MySQL Data Transfer

Source Server         : 127.0.0.1
Source Server Version : 50729
Source Host           : 127.0.0.1:3306
Source Database       : switchboard

Target Server Type    : MYSQL
Target Server Version : 50729
File Encoding         : 65001

Date: 2020-04-08 09:10:02
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `switchboard`
-- ----------------------------
DROP TABLE IF EXISTS `switchboard`;
CREATE TABLE `switchboard` (
  `id` int(3) NOT NULL AUTO_INCREMENT,
  `sw_name` varchar(50) CHARACTER SET utf8 NOT NULL,
  `brand` varchar(20) CHARACTER SET utf8 NOT NULL,
  `ip` varchar(15) CHARACTER SET utf8 NOT NULL,
  `login` varchar(20) CHARACTER SET utf8 NOT NULL,
  `pwd` varchar(20) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=369 DEFAULT CHARSET=latin1;
