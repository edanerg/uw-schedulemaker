-- Execute once to create sample data
-- TODO: how to execute file from Cloud Shell
-- Data: 
--      * 1 course: CS 348
--      * 2 classes: TTh 10-11:30, TTh 1-2:30
--      * 1 instructor: He,Xi

INSERT INTO Course
VALUES (004417, 'CS', '348', 'Introduction to Database Management', 'The main objective of this course is to introduce students to fundamentals of database technology by studying databases from three viewpoints: those of the database user, the database designer, and the database administrator. It teaches the use of a database management system (DBMS) by treating it as a black box, focusing only on its functionality and its interfaces. Topics include: introduction to database systems, relational database systems, database design methodology, SQL and interfaces, database application development, concept of transactions, ODBC, JDBC, database tuning, database Administration, and current topics (distributed databases, data warehouses, data mining).');

INSERT INTO Course
VALUES (004407, 'CS', '436', 'Networks and Distributed Computer Systems', 'An introduction to networks, protocols, and distributed systems. Layered models, resource management, naming, addressing and routing, reliable communication, security, and higher-level services.');

INSERT INTO Instructor
VALUES (1, 'He,Xi');

-- TTh 10-11:30
INSERT INTO Class (id, subject, catalog_number, units, class_number, class_type, section_number, campus, associated_class, 
    related_component_1, enrollment_capacity, enrollment_total, term, academic_level)
VALUES (111, 'CS', '348', 0.5, 5794, 'LEC', 001, 'UW U', 1, 101, 70, 68, 1201, 'undergraduate');

INSERT INTO ClassTime (id, class_id, start_time, end_time, weekdays, is_active, building, room)
VALUES (999, 111, '10:00:00', '11:20:00', 'TTh', TRUE, 'RCH', '207');

INSERT INTO InstructorClassTime
VALUES (1, 999);

-- TTh 1-2:30
INSERT INTO Class (id, subject, catalog_number, units, class_number, class_type, section_number, campus, associated_class, 
    related_component_1, enrollment_capacity, enrollment_total, term, academic_level)
VALUES (222, 'CS', '436', 0.5, 6354, 'LEC', 002, 'UW U', 2, 101, 70, 67, 1201, 'undergraduate');

INSERT INTO ClassTime (id, class_id, start_time, end_time, weekdays, is_active, building, room)
VALUES (1010, 222, '13:00:00', '14:20:00', 'TTh', TRUE, 'MC', '4040');

INSERT INTO InstructorClassTime
VALUES (1, 1010);