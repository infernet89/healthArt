-- --------------------------------------------------------
-- Host:                         192.168.1.223
-- Versione server:              5.5.62-0+deb8u1 - (Raspbian)
-- S.O. server:                  debian-linux-gnu
-- HeidiSQL Versione:            11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dump della struttura di tabella CosoDB.health_Heart
CREATE TABLE IF NOT EXISTS `health_Heart` (
  `time` datetime NOT NULL,
  `bpm` int(11) NOT NULL,
  PRIMARY KEY (`time`),
  UNIQUE KEY `time` (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- L’esportazione dei dati non era selezionata.

-- Dump della struttura di tabella CosoDB.health_rawData
CREATE TABLE IF NOT EXISTS `health_rawData` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` int(11) DEFAULT NULL,
  `unit` varchar(8) DEFAULT NULL,
  `startTime` varchar(32) NOT NULL,
  `start` datetime NOT NULL,
  `endTime` varchar(32) NOT NULL,
  `end` datetime NOT NULL,
  `value` varchar(128) DEFAULT NULL,
  `key` varchar(64) NOT NULL,
  `processed` bit(1) DEFAULT b'0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=942862 DEFAULT CHARSET=latin1;

-- L’esportazione dei dati non era selezionata.

-- Dump della struttura di tabella CosoDB.health_Sleep
CREATE TABLE IF NOT EXISTS `health_Sleep` (
  `start` datetime NOT NULL,
  `end` datetime NOT NULL,
  `type` varchar(16) NOT NULL,
  `durationMinutes` int(11) DEFAULT NULL,
  PRIMARY KEY (`start`,`end`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- L’esportazione dei dati non era selezionata.

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
