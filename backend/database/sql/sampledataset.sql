-- Execute once to create sample data
-- Data: 
--      * 1 course: CS 348
--      * 1 instructor: He,Xi
--      * 2 LEC: TTh 10-11:30, TTh 1-2:30
--      * 2 TUT: M 10-11:30, M 1-2:30. Each tutorial corresponds to the respective LEC

INSERT INTO Course
VALUES (004417, 'CS', '348', 'Introduction to Database Management', 'The main objective of this course is to introduce students to fundamentals of database technology by studying databases from three viewpoints: those of the database user, the database designer, and the database administrator.');

INSERT INTO Instructor (name)
VALUES ('He,Xi');

-- TTh 10-11:30
-- LEC
INSERT INTO Class (class_number, subject, catalog_number, units, class_type, section_number, campus, associated_class, 
    term, academic_level)
VALUES (5794, 'CS', '348', 0.5, 'LEC', '001', 'UW U', 1, 1201, 'undergraduate');

INSERT INTO ClassTime (class_number, start_time, end_time, weekdays, building, room, instructor_id)
VALUES (5794, '10:00:00', '11:20:00', 'TTh', 'RCH', '207', 1);

-- TUT
INSERT INTO Class (class_number, subject, catalog_number, units, class_type, section_number, campus, associated_class, 
    term, academic_level)
VALUES (5795, 'CS', '348', 0.5, 'TUT', '101', 'UW U', 1, 1201, 'undergraduate');

INSERT INTO ClassTime (class_number, start_time, end_time, weekdays, building, room)
VALUES (5795, '10:00:00', '11:20:00', 'M', 'RCH', '207');

-- TTh 1-2:30
-- LEC
INSERT INTO Class (class_number, subject, catalog_number, units, class_type, section_number, campus, associated_class, 
    term, academic_level)
VALUES (6354, 'CS', '348', 0.5, 'LEC', '002', 'UW U', 2, 1201, 'undergraduate');

INSERT INTO ClassTime (class_number, start_time, end_time, weekdays, building, room, instructor_id)
VALUES (6354, '13:00:00', '14:20:00', 'TTh', 'MC', '4040', 1);

-- TUT
INSERT INTO Class (class_number, subject, catalog_number, units, class_type, section_number, campus, associated_class, 
    term, academic_level)
VALUES (6355, 'CS', '348', 0.5, 'TUT', '102', 'UW U', 2, 1201, 'undergraduate');

INSERT INTO ClassTime (class_number, start_time, end_time, weekdays, building, room)
VALUES (6355, '13:00:00', '14:20:00', 'M', 'MC', '4040');