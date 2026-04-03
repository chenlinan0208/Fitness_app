
INSERT INTO User (Name, Date_of_Birth, Height, Weight) VALUES
('Alex Johnson', '1995-04-12', 178, 78.5),
('Maria Lopez', '1992-09-30', 165, 62.3),
('James Kim', '2000-01-15', 172, 70.1);


INSERT INTO Training_Session VALUES
(1, 1, 'Squat', 'Strength', 'Barbell', 'Increase lower body strength'),
(1, 2, 'Romanian Deadlift', 'Strength', 'Barbell', 'Posterior chain development'),
(1, 3, 'Leg Press', 'Strength', 'Machine', 'Quad hypertrophy');

INSERT INTO Training_Session VALUES
(2, 1, 'Bench Press', 'Strength', 'Barbell', 'Chest and triceps strength'),
(2, 2, 'Barbell Row', 'Strength', 'Barbell', 'Back strength'),
(2, 3, 'Lat Pulldown', 'Strength', 'Machine', 'Lat development');

INSERT INTO Training_Session VALUES
(3, 1, 'Deadlift', 'Strength', 'Barbell', 'Full posterior chain strength'),
(3, 2, 'Hip Thrust', 'Strength', 'Barbell', 'Glute development'),
(3, 3, 'Back Extension', 'Strength', 'Bodyweight', 'Lower back endurance');


INSERT INTO Training_Session VALUES
(4, 1, 'Kettlebell Swing', 'Conditioning', 'Kettlebell', 'Explosive hip power'),
(4, 2, 'Push-Up', 'Bodyweight', 'None', 'Upper body endurance'),
(4, 3, 'Goblet Squat', 'Strength', 'Dumbbell', 'Full body strength');

INSERT INTO Training_Session VALUES
(5, 1, 'Overhead Press', 'Strength', 'Barbell', 'Shoulder strength'),
(5, 2, 'Pull-Up', 'Bodyweight', 'None', 'Back and biceps strength'),
(5, 3, 'Dumbbell Fly', 'Hypertrophy', 'Dumbbells', 'Chest hypertrophy');


INSERT INTO Perform VALUES
(1,1,1),(1,1,2),(1,1,3),
(1,2,1),(1,2,2),(1,2,3),
(1,3,1),(1,3,2),(1,3,3),
(1,4,1),(1,4,2),(1,4,3),
(1,5,1),(1,5,2),(1,5,3);


INSERT INTO Perform VALUES
(2,1,1),(2,1,2),(2,1,3),
(2,2,1),(2,2,2),(2,2,3),
(2,3,1),(2,3,2),(2,3,3),
(2,4,1),(2,4,2),(2,4,3),
(2,5,1),(2,5,2),(2,5,3);


INSERT INTO Perform VALUES
(3,1,1),(3,1,2),(3,1,3),
(3,2,1),(3,2,2),(3,2,3),
(3,3,1),(3,3,2),(3,3,3),
(3,4,1),(3,4,2),(3,4,3),
(3,5,1),(3,5,2),(3,5,3);
