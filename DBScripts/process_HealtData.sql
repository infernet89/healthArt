BEGIN
	DECLARE v_done INT DEFAULT FALSE;
	DECLARE v_id INT DEFAULT NULL;
	DECLARE v_start DATETIME DEFAULT NULL;
	DECLARE v_end DATETIME DEFAULT NULL;
	DECLARE v_value INT DEFAULT NULL;
	DECLARE v_kind VARCHAR(32) DEFAULT NULL;

	DECLARE prev_kind VARCHAR(32) DEFAULT NULL;
	DECLARE prev_end DATETIME DEFAULT NULL;
	DECLARE sleep_start DATETIME DEFAULT NULL;
	DECLARE sleep_end DATETIME DEFAULT NULL;
	
	DECLARE curHealthData CURSOR FOR
		SELECT id,start,CAST(value AS SIGNED) as value FROM health_rawData where processed=0 AND `key` like '%HEART%';
	DECLARE curSleepData CURSOR FOR
		SELECT id,start,end,REPLACE(`key`,'PROFESSIONAL_SLEEP_','') as kind FROM health_rawData where processed=0 and `key` like '%sleep%' ORDER BY start,end;
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done = TRUE;

	OPEN curHealthData;
	healthData_loop: LOOP
			FETCH curHealthData INTO v_id, v_start, v_value;
			IF v_done THEN
					LEAVE healthData_loop;
			END IF;
			UPDATE health_rawData SET processed=1 WHERE id=v_id;
			INSERT IGNORE INTO health_Heart(time,bpm) VALUES (v_start,v_value);
	END LOOP;
CLOSE curHealthData;

	SET v_done = FALSE;
	OPEN curSleepData;
	curSleepData_loop: LOOP
		FETCH curSleepData INTO v_id, v_start, v_end, v_kind;
		IF sleep_start IS NULL THEN
			SET sleep_start=v_start;
		END IF;

		IF v_done THEN
			LEAVE curSleepData_loop;
		END IF;
		UPDATE health_rawData SET processed=1 WHERE id=v_id;
		/*IF prev_kind IS NOT NULL AND v_kind<>prev_kind THEN*/
		IF TIMESTAMPDIFF(MINUTE,prev_end,v_end)>1 THEN
			INSERT IGNORE INTO health_Sleep(start,end,type,durationMinutes) VALUES (sleep_start,sleep_end,prev_kind,TIMESTAMPDIFF(MINUTE,sleep_start,sleep_end));
			SET sleep_start=v_start;
		ELSE
			SET sleep_end=v_end;
		END IF;
		SET prev_kind=v_kind;
		SET prev_end=v_end;
	END LOOP;

CLOSE curSleepData;

UPDATE health_Sleep
SET durationMinutes=-durationMinutes,
start=(@temp:=start), 
start = end, 
end = @temp
WHERE start > end
;
END