USE `projeto_dados` ;

DROP TRIGGER IF EXISTS trig_curtidas;
DELIMITER //
CREATE TRIGGER trig_curtidas BEFORE UPDATE ON post_likes

FOR EACH ROW
BEGIN
	IF (Old.curtida <=> New.curtida) THEN
		SET New.curtida = 0;
	ELSE
		SET New.curtida = New.curtida;
	END IF;
END //

DELIMITER ;
