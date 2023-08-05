CREATE TABLE Member (
 Member_ID INT PRIMARY KEY,
 Member_Name VARCHAR(255),
 Address VARCHAR(255),
 Registration_Date DATE,
 Membership_Type VARCHAR(50),
 FOREIGN KEY (Membership_Type) REFERENCES Membership(Membership_Type)
);

CREATE TABLE Membership (
 Membership_Type VARCHAR(50) PRIMARY KEY,
 Fee DECIMAL(10, 2)
);

CREATE TABLE Exercise (
 Exercise_ID INT PRIMARY KEY,
 Name VARCHAR(255),
 Exercise_Type VARCHAR(50),
 Descriptor VARCHAR(255)
);

CREATE TABLE Class (
 Class_ID INT PRIMARY KEY,
 Room_Number VARCHAR(255),
 Building VARCHAR(255),
 Instructor_ID INT,
 Start_Time TIMESTAMP,
 Duration INT,
 Max_Members INT,
 FOREIGN KEY (Building, Room_Number) REFERENCES Room(Building, Room_Number),
 FOREIGN KEY (Instructor_ID) REFERENCES Instructor(Instructor_ID)
);


CREATE TABLE Member_Class (
    Member_ID INT NOT NULL,
    Class_ID INT NOT NULL,
    Registration_Date DATE,
    CONSTRAINT PK_Member_Class PRIMARY KEY (Member_ID, Class_ID),
    FOREIGN KEY (Member_ID) REFERENCES Member(Member_ID),
    FOREIGN KEY (Class_ID) REFERENCES Class(Class_ID)   
)

CREATE TABLE Room (
 Building VARCHAR(255),
 Room_Number VARCHAR(50),
 CONSTRAINT PK_Room PRIMARY KEY (Building, Room_Number)
);

CREATE TABLE Instructor (
 Instructor_ID INT PRIMARY KEY,
 Name VARCHAR(255),
 Employment_Type VARCHAR(50)
);

CREATE TABLE External_Instructor (
    Instructor_ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Wage DECIMAL(10,2),
    Hours INT,
    FOREIGN KEY (Instructor_ID) REFERENCES Instructor(Instructor_ID)
)

CREATE TABLE Internal_Instructor (
    Instructor_ID INT PRIMARY KEY,
    Name VARCHAR(255),
    Salary INT,
    FOREIGN KEY (Instructor_ID) REFERENCES Instructor(Instructor_ID)
)



CREATE OR REPLACE FUNCTION check_class_capacity()
RETURNS TRIGGER AS $$
DECLARE
    current_capacity INT;
    max_capacity INT;
BEGIN
    SELECT COUNT(DISTINCT Member_ID) INTO current_capacity
    FROM Member_Class
    WHERE Class_ID = NEW.Class_ID;

    SELECT Max_Members INTO max_capacity
    FROM "Class"
    WHERE Class_ID = NEW.Class_ID;

    IF current_capacity >= max_capacity THEN
        RAISE EXCEPTION 'Class is at maximum capacity. Cannot insert.';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER before_insert_class_member
BEFORE INSERT ON Member_Class
FOR EACH ROW
EXECUTE FUNCTION check_class_capacity();

