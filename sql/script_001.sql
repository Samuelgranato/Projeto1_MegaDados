-- MySQL Script generated by MySQL Workbench
-- Sun 13 Oct 2019 09:23:47 PM -03
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering



-- -----------------------------------------------------
-- Schema projeto_dados
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema projeto_dados
-- -----------------------------------------------------
-- DROP SCHEMA IF EXISTS `projeto_dados`;
CREATE SCHEMA IF NOT EXISTS `projeto_dados` DEFAULT CHARACTER SET utf8 ;
USE `projeto_dados` ;


-- -----------------------------------------------------
-- Table `projeto_dados`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `projeto_dados`.`user` (
  `iduser` INT NOT NULL AUTO_INCREMENT,
  `login` VARCHAR(45) NOT NULL UNIQUE,
  `nome` VARCHAR(45) NOT NULL ,
  `sobrenome` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NULL UNIQUE,
  `cidade_idcidade` INT NOT NULL,
  PRIMARY KEY (`iduser`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `projeto_dados`.`post`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `projeto_dados`.`post` (
  `idpost` INT NOT NULL AUTO_INCREMENT,
  `user_iduser_p` INT NULL,
  `titulo` VARCHAR(45) NULL,
  `texto` VARCHAR(45) NULL,
  `url` VARCHAR(45) NULL,
  `is_active` INT NULL DEFAULT '1',
  PRIMARY KEY (`idpost`),
  INDEX `iduser_idx` (`user_iduser_p` ASC),
  CONSTRAINT `iduser`
    FOREIGN KEY (`user_iduser_p`)
    REFERENCES `projeto_dados`.`user` (`iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `projeto_dados`.`passaro`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `projeto_dados`.`passaro` (
  `idpassaro` INT NOT NULL AUTO_INCREMENT,
  `especie` VARCHAR(45) NULL UNIQUE,
  PRIMARY KEY (`idpassaro`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `projeto_dados`.`user_has_passaro`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `projeto_dados`.`user_has_passaro` (
  `user_iduser_hp` INT NOT NULL,
  `passaro_idpassaro_hp` INT NOT NULL,
  PRIMARY KEY (`user_iduser_hp`, `passaro_idpassaro_hp`),
  INDEX `fk_user_has_passaro_passaro1_idx` (`passaro_idpassaro_hp` ASC),
  INDEX `fk_user_has_passaro_user1_idx` (`user_iduser_hp` ASC),
  CONSTRAINT `fk_user_has_passaro_user1`
    FOREIGN KEY (`user_iduser_hp`)
    REFERENCES `projeto_dados`.`user` (`iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_has_passaro_passaro1`
    FOREIGN KEY (`passaro_idpassaro_hp`)
    REFERENCES `projeto_dados`.`passaro` (`idpassaro`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;




-- -----------------------------------------------------
-- Table `projeto_dados`.`post_menciona_passaro`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `projeto_dados`.`post_menciona_passaro` (
  `post_idpost_mp` INT NOT NULL,
  `passaro_idpassaro_mp` INT NOT NULL,
  `is_active` VARCHAR(45) NULL DEFAULT '1',
  PRIMARY KEY (`post_idpost_mp`, `passaro_idpassaro_mp`),
  INDEX `fk_post_has_passaro_passaro1_idx` (`passaro_idpassaro_mp` ASC),
  INDEX `fk_post_has_passaro_post1_idx` (`post_idpost_mp` ASC),
  CONSTRAINT `fk_post_has_passaro_post1`
    FOREIGN KEY (`post_idpost_mp`)
    REFERENCES `projeto_dados`.`post` (`idpost`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_post_has_passaro_passaro1`
    FOREIGN KEY (`passaro_idpassaro_mp`)
    REFERENCES `projeto_dados`.`passaro` (`idpassaro`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `projeto_dados`.`post_menciona_user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `projeto_dados`.`post_menciona_user` (
  `post_idpost_mu` INT NOT NULL,
  `user_iduser_mu` INT NOT NULL,
  `is_active` VARCHAR(45) NULL DEFAULT '1',
  PRIMARY KEY (`post_idpost_mu`, `user_iduser_mu`),
  INDEX `fk_post_has_user_user1_idx` (`user_iduser_mu` ASC),
  INDEX `fk_post_has_user_post1_idx` (`post_idpost_mu` ASC),
  CONSTRAINT `fk_post_has_user_post1`
    FOREIGN KEY (`post_idpost_mu`)
    REFERENCES `projeto_dados`.`post` (`idpost`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_post_has_user_user1`
    FOREIGN KEY (`user_iduser_mu`)
    REFERENCES `projeto_dados`.`user` (`iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



-- -----------------------------------------------------
-- Table `projeto_dados`.`cidade`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `projeto_dados`.`cidade` (
  `idcidade` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NULL,
  PRIMARY KEY (`idcidade`))
ENGINE = InnoDB;



-- -----------------------------------------------------
-- Table `projeto_dados`.`log`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `projeto_dados`.`log` (
  `idlog` INT NOT NULL AUTO_INCREMENT,
  `user_iduser_l` INT NULL,
  `os` VARCHAR(45) NULL,
  `browser` VARCHAR(45) NULL,
  `ip` VARCHAR(45) NULL,
  `criado_ts` VARCHAR(45) NULL,
  PRIMARY KEY (`idlog`),
  INDEX `iduser_idx` (`user_iduser_l` ASC),
  CONSTRAINT `idlog`
    FOREIGN KEY (`user_iduser_l`)
    REFERENCES `projeto_dados`.`user` (`iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
