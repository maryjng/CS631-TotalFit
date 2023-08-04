CREATE TABLE Member (
 MemberID INT PRIMARY KEY,
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
 ExerciseID INT PRIMARY KEY,
 Name VARCHAR(255),
 Exercise_Type VARCHAR(50),
 Descriptor VARCHAR(255)
);

CREATE TABLE Class (
 ClassID INT PRIMARY KEY,
 RoomNumber VARCHAR(255),
 Building VARCHAR(255),
 InstructorID INT,
 Start_Time TIMESTAMP,
 Duration INT,
 Max_Members INT,
 FOREIGN KEY (Building, RoomNumber) REFERENCES Room(Building, RoomNumber),
 FOREIGN KEY (InstructorID) REFERENCES Instructor(InstructorID)
);


CREATE TABLE Member_Class (
    MemberID INT NOT NULL,
    ClassID INT NOT NULL,
    Registration_Date DATE,
    CONSTRAINT PK_Member_Class PRIMARY KEY (MemberID, ClassID),
    FOREIGN KEY (MemberID) REFERENCES Member(MemberID),
    FOREIGN KEY (ClassID) REFERENCES Class(ClassID)   
)

CREATE TABLE Room (
 Building VARCHAR(255),
 RoomNumber VARCHAR(50),
 CONSTRAINT PK_Room PRIMARY KEY (Building, RoomNumber)
);

CREATE TABLE Instructor (
 InstructorID INT PRIMARY KEY,
 Name VARCHAR(255),
 EmploymentType VARCHAR(50)
);

CREATE TABLE External_Instructor (
    InstructorID INT PRIMARY KEY,
    Name VARCHAR(255),
    Wage DECIMAL(10,2),
    Hours INT,
    FOREIGN KEY (InstructorID) REFERENCES Instructor(InstructorID)
)

CREATE TABLE Internal_Instructor (
    InstructorID INT PRIMARY KEY,
    Name VARCHAR(255),
    Salary INT,
    FOREIGN KEY (InstructorID) REFERENCES Instructor(InstructorID)
)
