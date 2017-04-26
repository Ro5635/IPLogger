-- Predefined Procedure for MySQL

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_updateIP`(
    IN p_id int(10),
    IN p_IPAddress VARCHAR(255)
)
BEGIN
        
        UPDATE Servers SET ipaddress = p_IPAddress WHERE id= p_id ; 


END$$
DELIMITER ;


CALL sp_updateIP(1,'192.168.2.155')