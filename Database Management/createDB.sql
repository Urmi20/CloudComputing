-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

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
-- Table `InstaKilo`.`user_profile`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `InstaKilo`.`user_profile` ;

CREATE TABLE IF NOT EXISTS `InstaKilo`.`user_profile` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(6) NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `InstaKilo`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `InstaKilo`.`user` ;

CREATE TABLE IF NOT EXISTS `InstaKilo`.`user` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `profile` INT UNSIGNED NOT NULL,
  `name` VARCHAR(45) NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(100) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `pw_salt_hash` VARCHAR(165) NOT NULL,
  PRIMARY KEY (`id`, `profile`),
  UNIQUE INDEX `user_name_UNIQUE` (`name` ASC) VISIBLE,
  UNIQUE INDEX `user_id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `profile_idx` (`profile` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE,
  CONSTRAINT `profile`
    FOREIGN KEY (`profile`)
    REFERENCES `InstaKilo`.`user_profile` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `InstaKilo`.`photo`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `InstaKilo`.`photo` ;

CREATE TABLE IF NOT EXISTS `InstaKilo`.`photo` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `owner` INT UNSIGNED NOT NULL,
  `title` VARCHAR(50) NULL,
  `hashtags` VARCHAR(50) NULL,
  `date_time_added` DATETIME NOT NULL,
  `orig_file_name` VARCHAR(170) NOT NULL,
  `thumb_file_name` VARCHAR(170) NOT NULL,
  PRIMARY KEY (`id`, `owner`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `owner_idx` (`owner` ASC) VISIBLE,
  INDEX `orig_file` (`orig_file_name` ASC) VISIBLE,
  INDEX `thum_file` (`thumb_file_name` ASC) VISIBLE,
  CONSTRAINT `owner`
    FOREIGN KEY (`owner`)
    REFERENCES `InstaKilo`.`user` (`id`)
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
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `description_UNIQUE` (`description` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `InstaKilo`.`transformation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `InstaKilo`.`transformation` ;

CREATE TABLE IF NOT EXISTS `InstaKilo`.`transformation` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `original` INT UNSIGNED NOT NULL,
  `trans_type` INT UNSIGNED NOT NULL,
  `file_name` VARCHAR(170) NOT NULL,
  PRIMARY KEY (`id`, `original`, `trans_type`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  UNIQUE INDEX `file_name_UNIQUE` (`file_name` ASC) VISIBLE,
  INDEX `type_idx` (`trans_type` ASC) VISIBLE,
  INDEX `original_photo_idx` (`original` ASC) VISIBLE,
  INDEX `file_name` (`file_name` ASC) VISIBLE,
  CONSTRAINT `original_photo`
    FOREIGN KEY (`original`)
    REFERENCES `InstaKilo`.`photo` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `type`
    FOREIGN KEY (`trans_type`)
    REFERENCES `InstaKilo`.`transformation_type` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `InstaKilo`.`scaling_settings`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `InstaKilo`.`scaling_settings` ;

CREATE TABLE IF NOT EXISTS `InstaKilo`.`scaling_settings` (
  `idmanager` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `scale_up_load` DOUBLE NOT NULL,
  `scale_down_load` DOUBLE NOT NULL,
  `expand_ratio` DOUBLE NOT NULL,
  `shrink_ratio` DOUBLE NOT NULL,
  `scaling_mode` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idmanager`),
  UNIQUE INDEX `idmanager_UNIQUE` (`idmanager` ASC) VISIBLE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- -----------------------------------------------------
-- Data for table `InstaKilo`.`user_profile`
-- -----------------------------------------------------
START TRANSACTION;
USE `InstaKilo`;
INSERT INTO `InstaKilo`.`user_profile` (`id`, `type`) VALUES (DEFAULT, 'user');
INSERT INTO `InstaKilo`.`user_profile` (`id`, `type`) VALUES (DEFAULT, 'admin');

COMMIT;


-- -----------------------------------------------------
-- Data for table `InstaKilo`.`user`
-- -----------------------------------------------------
START TRANSACTION;
USE `InstaKilo`;
INSERT INTO `InstaKilo`.`user` (`id`, `profile`, `name`, `first_name`, `last_name`, `email`, `pw_salt_hash`) VALUES (DEFAULT, 2, 'root', 'Mr All', 'Power', 'root@instakilo.ca', '$b4d3f077394d4f748d9fc66d5d4e1d9c$2716add7a66cdc1e723f45122576ef4d7b1935fd89349cd194c1156e3169ac6e664a5376c9df734b4392a5e6d45aec530a1c120b166c8c3f67058c49b830c969');

COMMIT;


-- -----------------------------------------------------
-- Data for table `InstaKilo`.`transformation_type`
-- -----------------------------------------------------
START TRANSACTION;
USE `InstaKilo`;
INSERT INTO `InstaKilo`.`transformation_type` (`id`, `description`) VALUES (DEFAULT, 'B&W');
INSERT INTO `InstaKilo`.`transformation_type` (`id`, `description`) VALUES (DEFAULT, 'Warm');
INSERT INTO `InstaKilo`.`transformation_type` (`id`, `description`) VALUES (DEFAULT, 'High Contrast');

COMMIT;


-- -----------------------------------------------------
-- Data for table `InstaKilo`.`scaling_settings`
-- -----------------------------------------------------
START TRANSACTION;
USE `InstaKilo`;
INSERT INTO `InstaKilo`.`scaling_settings` (`idmanager`, `scale_up_load`, `scale_down_load`, `expand_ratio`, `shrink_ratio`, `scaling_mode`) VALUES (DEFAULT, 80, 40, 2, 2, 'auto');

COMMIT;

