-- For demonstration purposes, the parameters are hardcoded into the queries

-- Select classes that match the given subject, catalog number, start time, end time, and weekdays.
SELECT * FROM Classtime LEFT JOIN 
    (SELECT Class.class_number AS class_num, Course.subject AS c_subject, Course.catalog_number AS c_catalog, 
    Class.units AS units, Class.class_type AS class_type, Class.section_number AS section_number, 
    Course.description AS description, Course.name AS name 
    FROM Class LEFT JOIN Course ON Course.subject = Class.subject AND Course.catalog_number = Class.catalog_number) 
AS CourseAndClass 
ON CourseAndClass.class_num = ClassTime.class_number 
WHERE weekdays LIKE '%MW%' AND c_subject LIKE '%CS%' AND c_catalog LIKE '%106%' 
AND start_time >= '11:00:00' AND end_time <= '15:00:00'
LIMIT 10;

-- Insert an app user
INSERT INTO AppUser (username) VALUES ('csstudent');