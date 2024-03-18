-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema CoolBox
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema CoolBox
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `CoolBox` DEFAULT CHARACTER SET utf8 ;
USE `CoolBox` ;

-- -----------------------------------------------------
-- Table `CoolBox`.`sensor_dim`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `CoolBox`.`sensor_dim` (
  `sensor_id` VARCHAR(45) NOT NULL,
  `device_id` VARCHAR(45) NOT NULL,
  `device_name` VARCHAR(45) NOT NULL,
  `unit_name` VARCHAR(45) NOT NULL,
  `unit_value` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`sensor_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `CoolBox`.`timestamp_dim`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `CoolBox`.`timestamp_dim` (
  `timestamp_key` INT NOT NULL AUTO_INCREMENT,
  `year` INT NOT NULL,
  `month` INT NOT NULL,
  `week` INT NOT NULL,
  `day` INT NOT NULL,
  `hour` INT NOT NULL,
  `minute` INT NOT NULL,
  `sec` INT NOT NULL,
  `microsec` INT NOT NULL,
  PRIMARY KEY (`timestamp_key`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `CoolBox`.`measurement_fact`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `CoolBox`.`measurement_fact` (
  `timestamp_key` INT NOT NULL,
  `sensor_id` VARCHAR(45) NOT NULL,
  `value` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`timestamp_key`, `sensor_id`),
  INDEX `fk_measurement_fact_sensor_dim1_idx` (`sensor_id` ASC),
  CONSTRAINT `fk_measurement_fact_timestamp_dim`
    FOREIGN KEY (`timestamp_key`)
    REFERENCES `CoolBox`.`timestamp_dim` (`timestamp_key`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_measurement_fact_sensor_dim1`
    FOREIGN KEY (`sensor_id`)
    REFERENCES `CoolBox`.`sensor_dim` (`sensor_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
