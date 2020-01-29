-- The API states that any value can be null, but for our purposes,
-- we will not include rows that have invalid null values.

-- Course --
-- Will be querying this table mainly by subject and catalog number, since that is the way to 
-- get the classes for the course.
CREATE TABLE IF NOT EXISTS Course (
    id INTEGER NOT NULL UNIQUE,
    subject VARCHAR(10) NOT NULL,
    catalog_number VARCHAR(10) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(1000),
    PRIMARY KEY(subject, catalog_number)
);

-- Instructor --
-- The endpoint only provides instructor name, so that is the primary index.
-- We have no way of handling instructors with the same name. 
CREATE TABLE IF NOT EXISTS Instructor (
    id INTEGER NOT NULL UNIQUE AUTO_INCREMENT,
    name VARCHAR(30) NOT NULL PRIMARY KEY
);

-- Class --
-- Things to preprocess before insertion:
-- * class_type
-- * section_number
-- * held_with
CREATE TABLE IF NOT EXISTS Class (
    id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    course_id INTEGER NOT NULL REFERENCES Course(id) ON DELETE CASCADE,
    units FLOAT NOT NULL CHECK (units >= 0),
    note VARCHAR(100),  -- sometimes the note will specify to choose a TUT
    class_number INTEGER NOT NULL UNIQUE,
    class_type CHAR(3) NOT NULL, -- LEC, TUT, TST, LAB, etc
    section_number VARCHAR(10) NOT NULL, -- 001, 101, 201, etc
    campus VARCHAR(10) NOT NULL,
    associated_class INTEGER NOT NULL CHECK(associated_class >= 0),
    related_component_1 INTEGER,
    related_component_2 INTEGER,
    enrollment_capacity INTEGER NOT NULL DEFAULT 0 CHECK(enrollment_capacity >= 0),
    enrollment_total INTEGER NOT NULL DEFAULT 0 CHECK(enrollment_total >= 0),
    waiting_capacity INTEGER NOT NULL DEFAULT 0 CHECK(waiting_capacity >= 0),
    waiting_total INTEGER NOT NULL DEFAULT 0 CHECK(waiting_total >= 0),
    topic VARCHAR(10),
    held_with VARCHAR(10), -- comma separated course names (see CLAS 221)
    term INTEGER NOT NULL,
    academic_level VARCHAR(20)
);

-- Class Time --
-- Some classes have multiple locations. For example, MATH 135 has one class MWF and one class T in different rooms
CREATE TABLE IF NOT EXISTS ClassTime (
    id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
    class_id INTEGER NOT NULL REFERENCES Class(id) ON DELETE CASCADE ON UPDATE CASCADE,
    start_time TIME NOT NULL, -- format: 'hh:mm:ss', stored in 24-hour EST
    end_time TIME NOT NULL CHECK(end_time > start_time),
    weekdays VARCHAR(10) NOT NULL, -- M,T,W,Th,F,Sa,Su
    start_date DATE,
    end_date DATE CHECK(end_date >= start_date),
    is_active BOOLEAN NOT NULL DEFAULT TRUE, -- true if is_tba, is_cancelled, and is_closed are all false
    building VARCHAR(10) NOT NULL,
    room VARCHAR(10) NOT NULL
);

-- Connects an instructor to a class time (since a class time can apparently be taught by multiple instructors)
CREATE TABLE IF NOT EXISTS InstructorClassTime(
    instructor_id INTEGER NOT NULL REFERENCES Instructor(id) ON DELETE CASCADE,
    class_time_id INTEGER NOT NULL REFERENCES ClassTime(id) ON DELETE CASCADE,
    PRIMARY KEY(instructor_id, class_time_id)
);

-- Reserve --
-- Multiple reserves can be associated with one class
CREATE TABLE IF NOT EXISTS Reserve (
    id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT, -- not sure if needed
    class_id INTEGER NOT NULL REFERENCES Class(id) ON DELETE CASCADE,
    reserve_group_name VARCHAR(15) NOT NULL,
    enrollment_capacity INTEGER NOT NULL CHECK(enrollment_capacity >= 0),
    enrollment_total INTEGER NOT NULL CHECK(enrollment_total >= 0)
);

-- Theres some issue with the syntax for this one:
-- Will likely be searching by class_id
-- CREATE IF NOT EXISTS INDEX reserve_class_id
-- ON Reserve(class_id);
