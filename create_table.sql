DROP TABLE IF EXISTS Includes;
DROP TABLE IF EXISTS Generates;
DROP TABLE IF EXISTS Records;
DROP TABLE IF EXISTS Perform;
DROP TABLE IF EXISTS PerformanceLog;
DROP TABLE IF EXISTS NutritionLog;
DROP TABLE IF EXISTS Training_Session;
DROP TABLE IF EXISTS User;

CREATE TABLE User (
    UserID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255),
    Date_of_Birth DATE,
    Height INT,
    Weight DECIMAL(5,2)
);

CREATE TABLE Training_Session (
    WorkoutID INT,
    ExerciseID INT,
    Exercise_Name VARCHAR(255),
    Category VARCHAR(255),
    Equipment VARCHAR(255),
    Target_Goal VARCHAR(255),
    PRIMARY KEY (WorkoutID, ExerciseID)
);

CREATE TABLE PerformanceLog (
    LogID INT PRIMARY KEY AUTO_INCREMENT,
    Date DATE,
    Duration INT,
    Sets INT,
    Reps INT,
    `Load` INT
);


CREATE TABLE NutritionLog (
    NutritionLogID INT PRIMARY KEY AUTO_INCREMENT,
    Date DATE,
    Calorie_intake INT,
    Macros VARCHAR(255)
);

CREATE TABLE Perform (
    UserID INT,
    WorkoutID INT,
    ExerciseID INT,
    PRIMARY KEY (UserID, WorkoutID, ExerciseID),
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (WorkoutID, ExerciseID) REFERENCES Training_Session(WorkoutID, ExerciseID)
);

CREATE TABLE Includes (
    LogID INT PRIMARY KEY,
    WorkoutID INT,
    ExerciseID INT,
    FOREIGN KEY (LogID) REFERENCES PerformanceLog(LogID),
    FOREIGN KEY (WorkoutID, ExerciseID) REFERENCES Training_Session(WorkoutID, ExerciseID)
);

CREATE TABLE Generates (
    LogID INT PRIMARY KEY,
    UserID INT,
    FOREIGN KEY (LogID) REFERENCES PerformanceLog(LogID),
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);

CREATE TABLE Records (
    NutritionLogID INT PRIMARY KEY,
    UserID INT,
    FOREIGN KEY (NutritionLogID) REFERENCES NutritionLog(NutritionLogID),
    FOREIGN KEY (UserID) REFERENCES User(UserID)
);
