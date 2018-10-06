-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema InstaKilo
-- -----------------------------------------------------
-- Database for the InstaKilo Web Application
DROP SCHEMA IF EXISTS `InstaKilo` ;

-- -----------------------------------------------------
-- Schema InstaKilo
--
-- Database for the InstaKilo Web Application
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `InstaKilo` DEFAULT CHARACTER SET utf8 ;
USE `InstaKilo` ;

-- -----------------------------------------------------
-- Table `InstaKilo`.`user_profiles`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `InstaKilo`.`user_profiles` ;

CREATE TABLE IF NOT EXISTS `InstaKilo`.`user_profiles` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(6) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `InstaKilo`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `InstaKilo`.`users` ;

CREATE TABLE IF NOT EXISTS `InstaKilo`.`users` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `profile` INT UNSIGNED NOT NULL,
  `name` VARCHAR(45) NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(100) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `pw_salt_hash` VARCHAR(160) NOT NULL,
  PRIMARY KEY (`id`, `profile`),
  UNIQUE INDEX `user_name_UNIQUE` (`name` ASC),
  UNIQUE INDEX `user_id_UNIQUE` (`id` ASC),
  INDEX `profile_idx` (`profile` ASC),
  CONSTRAINT `profile`
    FOREIGN KEY (`profile`)
    REFERENCES `InstaKilo`.`user_profiles` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `InstaKilo`.`photos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `InstaKilo`.`photos` ;

CREATE TABLE IF NOT EXISTS `InstaKilo`.`photos` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `owner` INT UNSIGNED NOT NULL,
  `title` VARCHAR(50) NULL,
  `hashtags` VARCHAR(50) NULL,
  `file_name` VARCHAR(128) NOT NULL,
  PRIMARY KEY (`id`, `owner`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `file_name_UNIQUE` (`file_name` ASC),
  INDEX `owner_idx` (`owner` ASC),
  CONSTRAINT `owner`
    FOREIGN KEY (`owner`)
    REFERENCES `InstaKilo`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `InstaKilo`.`transformation_type`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `InstaKilo`.`transformation_type` ;

CREATE TABLE IF NOT EXISTS `InstaKilo`.`transformation_type` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `description_UNIQUE` (`description` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `InstaKilo`.`transformations`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `InstaKilo`.`transformations` ;

CREATE TABLE IF NOT EXISTS `InstaKilo`.`transformations` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `original` INT UNSIGNED NOT NULL,
  `trans_type` INT UNSIGNED NOT NULL,
  `file_name` VARCHAR(128) NOT NULL,
  PRIMARY KEY (`id`, `original`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `file_name_UNIQUE` (`file_name` ASC),
  INDEX `type_idx` (`trans_type` ASC),
  INDEX `original_photo_idx` (`original` ASC),
  CONSTRAINT `original_photo`
    FOREIGN KEY (`original`)
    REFERENCES `InstaKilo`.`photos` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `type`
    FOREIGN KEY (`trans_type`)
    REFERENCES `InstaKilo`.`transformation_type` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `InstaKilo`.`user_profiles`
-- -----------------------------------------------------
START TRANSACTION;
USE `InstaKilo`;
INSERT INTO `InstaKilo`.`user_profiles` (`id`, `type`) VALUES (DEFAULT, 'user');
INSERT INTO `InstaKilo`.`user_profiles` (`id`, `type`) VALUES (DEFAULT, 'admin');

COMMIT;


-- -----------------------------------------------------
-- Data for table `InstaKilo`.`transformation_type`
-- -----------------------------------------------------
START TRANSACTION;
USE `InstaKilo`;
INSERT INTO `InstaKilo`.`transformation_type` (`id`, `description`) VALUES (DEFAULT, 'B&W');
INSERT INTO `InstaKilo`.`transformation_type` (`id`, `description`) VALUES (DEFAULT, 'Sepia');
INSERT INTO `InstaKilo`.`transformation_type` (`id`, `description`) VALUES (DEFAULT, 'Barrel Distortion');

COMMIT;

