-- The API states that any value can be null, but for our purposes,
-- we will not include rows that have invalid null values.

-- Course --
-- Will be querying this table mainly by subject and catalog number, since that is the way to 
-- get the classes for the course.
CREATE TABLE IF NOT EXISTS Course (
    id INTEGER NOT NULL,
    subject VARCHAR(10) NOT NULL,
    catalog_number VARCHAR(10) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(1000),
    prerequisites VARCHAR(1000),
    antirequisites VARCHAR (1000),
    PRIMARY KEY (subject, catalog_number)
);

-- Instructor --
-- The endpoint only provides instructor name, so that is the primary index.
-- We have no way of handling instructors with the same name. 
CREATE TABLE IF NOT EXISTS Instructor (
    id SERIAL NOT NULL PRIMARY KEY,
    name VARCHAR(30) NOT NULL UNIQUE
);

-- Class --
-- Things to preprocess before insertion:
-- * class_type
-- * section_number
CREATE TABLE IF NOT EXISTS Class (
    class_number INTEGER NOT NULL PRIMARY KEY,
    subject VARCHAR(10) NOT NULL,
    catalog_number VARCHAR(10) NOT NULL,
    units FLOAT NOT NULL CHECK (units >= 0),
    class_type CHAR(3) NOT NULL, -- LEC, TUT, TST, LAB, etc
    section_number VARCHAR(10) NOT NULL, -- 001, 101, 201, etc
    campus VARCHAR(20) NOT NULL,
    associated_class INTEGER NOT NULL CHECK(associated_class >= 0),
    related_component_1 INTEGER, -- will first be populated with results from API, then modified to reference a class number
    related_component_2 INTEGER, -- same as related_component_1
    topic VARCHAR(1000),
    term INTEGER NOT NULL,
    academic_level VARCHAR(20),
    FOREIGN KEY (subject, catalog_number) REFERENCES Course(subject, catalog_number) ON DELETE CASCADE
);

-- Class Time --
-- Some classes have multiple locations. For example, MATH 135 has one class MWF and one class T in different rooms
CREATE TABLE IF NOT EXISTS ClassTime (
    id SERIAL NOT NULL PRIMARY KEY,
    class_number INTEGER NOT NULL REFERENCES Class(class_number) ON DELETE CASCADE ON UPDATE CASCADE,
    start_time TIME NOT NULL, -- format: 'hh:mm:ss', stored in 24-hour EST
    end_time TIME NOT NULL,
    weekdays VARCHAR(10), -- M,T,W,Th,F,Sa,Su
    start_date DATE,
    end_date DATE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE, -- true if is_tba, is_cancelled, and is_closed are all false
    building VARCHAR(10) NOT NULL,
    room VARCHAR(10) NOT NULL,
    instructor_id INTEGER REFERENCES Instructor(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- AppUser --
CREATE TABLE IF NOT EXISTS AppUser (
    username VARCHAR(30) NOT NULL PRIMARY KEY,
    academic_level VARCHAR(20)
);

-- CoursesTaken --
CREATE TABLE IF NOT EXISTS CoursesTaken (
    username VARCHAR(30) NOT NULL REFERENCES AppUser(username) ON DELETE CASCADE ON UPDATE CASCADE,
    subject VARCHAR(10) NOT NULL,
    catalog_number VARCHAR(10) NOT NULL,
    FOREIGN KEY (subject, catalog_number) REFERENCES Course(subject, catalog_number) ON DELETE CASCADE,
    PRIMARY KEY (username, subject, catalog_number)
);

-- UserSchedule --
CREATE TABLE IF NOT EXISTS UserSchedule (
    username VARCHAR(30) NOT NULL REFERENCES AppUser(username) ON DELETE CASCADE ON UPDATE CASCADE,
    class_number INTEGER NOT NULL REFERENCES Class(class_number) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (username, class_number)
);