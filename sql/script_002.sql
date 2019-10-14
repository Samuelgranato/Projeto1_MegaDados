USE `projeto_dados` ;

DROP TRIGGER IF EXISTS trig_apagacoment;
DELIMITER //
CREATE TRIGGER trig_apagacoment
AFTER UPDATE ON post
FOR EACH ROW
BEGIN
	IF NEW.is_active = 1 
    THEN
		UPDATE post_menciona_user
		SET    is_active = 1
		WHERE post_menciona_user.user_iduser_mu = post.idpost;
	ELSE
		UPDATE post_menciona_user
		SET    is_active = 1
		WHERE post_menciona_user.user_iduser_mu = post.idpost;
	END IF;
END
