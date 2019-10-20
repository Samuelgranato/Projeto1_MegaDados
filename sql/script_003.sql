use `projeto_dados`;

CREATE TABLE IF NOT EXISTS `projeto_dados`.`post_likes` (
  `idpost` INT NOT NULL,
  `iduser` INT NOT NULL,
  `curtida` INT NOT NULL DEFAULT 0,
  INDEX `idpost_idx` (`idpost` ASC),
  INDEX `iduser_idx` (`iduser` ASC),
  CONSTRAINT `idpost`
    FOREIGN KEY (`idpost`)
    REFERENCES `projeto_dados`.`post` (`idpost`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `iduser_fk`
    FOREIGN KEY (`iduser`)
    REFERENCES `projeto_dados`.`user` (`iduser`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;