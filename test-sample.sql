-- For demonstration purposes, the parameters are hardcoded into the queries

-- Select classes that match the given start time, end time, and weekdays.
-- Our sample database has two classes on Tuesday Thursday, one from 10-11:20, the other from 13-14:20.
SELECT * FROM Classtime LEFT JOIN
    (SELECT Class.id AS class_id, * FROM Class LEFT JOIN Course ON Course.subject = Class.subject AND Course.catalog_number = Class.catalog_number)
AS CourseAndClass ON CourseAndClass.class_id = ClassTime.class_id
WHERE weekdays LIKE 'TTh'
AND start_time >= '11:00:00' AND end_time <= '15:00:00';


-- Insert an app user
INSERT INTO AppUser (username) VALUES ('csstudent');