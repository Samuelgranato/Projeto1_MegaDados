USE `projeto_dados` ;

DROP TRIGGER IF EXISTS trig_mencaoUser;
DELIMITER //
CREATE TRIGGER trig_mencaoUser BEFORE UPDATE ON post

FOR EACH ROW
BEGIN
	IF NOT (New.is_active <=> Old.is_active) THEN
		    UPDATE post_menciona_user
    		SET post_menciona_user.is_active = New.is_active
    		WHERE post_menciona_user.post_idpost_mu = New.idpost;
	END IF;
END //

DELIMITER ;



DROP TRIGGER IF EXISTS trig_mencaoPassaro;
DELIMITER //
CREATE TRIGGER trig_mencaoPassaro BEFORE UPDATE ON post

FOR EACH ROW
BEGIN
	IF NOT (New.is_active <=> Old.is_active) THEN
		    UPDATE post_menciona_passaro
    		SET post_menciona_passaro.is_active = New.is_active
    		WHERE post_menciona_passaro.post_idpost_mp = New.idpost;
	END IF;
END //

DELIMITER ;