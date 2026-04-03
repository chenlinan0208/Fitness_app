-- ============================================
-- BLOCK 3-A: PERFORMANCE LOGS FOR ALEX (UserID = 1)
-- ============================================

-- Day 1 (Progression)
INSERT INTO PerformanceLog (Date, Duration, Sets, Reps, `Load`) VALUES
('2025-01-01', 55, 3, 5, 80);  -- Squat
SET @A1 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@A1, 1, 1);
INSERT INTO Generates VALUES (@A1, 1);

-- Day 3
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-03', 50, 3, 5, 60); -- Bench Press
SET @A2 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@A2, 2, 1);
INSERT INTO Generates VALUES (@A2, 1);

-- Day 5
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-05', 60, 1, 5, 120); -- Deadlift
SET @A3 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@A3, 3, 1);
INSERT INTO Generates VALUES (@A3, 1);

-- Day 8
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-08', 45, 3, 10, 24); -- Kettlebell Swing
SET @A4 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@A4, 4, 1);
INSERT INTO Generates VALUES (@A4, 1);

-- Day 10
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-10', 50, 3, 5, 65); -- Overhead Press
SET @A5 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@A5, 5, 1);
INSERT INTO Generates VALUES (@A5, 1);

-- Day 12 (Progression continues)
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-12', 55, 3, 5, 85); -- Squat
SET @A6 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@A6, 1, 1);
INSERT INTO Generates VALUES (@A6, 1);

-- Day 15
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-15', 50, 3, 5, 62); -- Bench
SET @A7 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@A7, 2, 1);
INSERT INTO Generates VALUES (@A7, 1);

-- Day 17 (Plateau begins)
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-17', 60, 1, 5, 122); -- Deadlift
SET @A8 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@A8, 3, 1);
INSERT INTO Generates VALUES (@A8, 1);

-- Day 20
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-20', 55, 3, 5, 86); -- Squat (flat)
SET @A9 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@A9, 1, 1);
INSERT INTO Generates VALUES (@A9, 1);

-- Day 23
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-23', 50, 3, 5, 63); -- Bench (flat)
SET @A10 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@A10, 2, 1);
INSERT INTO Generates VALUES (@A10, 1);

-- Day 26
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-26', 60, 1, 5, 123); -- Deadlift (flat)
SET @A11 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@A11, 3, 1);
INSERT INTO Generates VALUES (@A11, 1);

-- Day 30 (Plateau ends)
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-30', 55, 3, 5, 87);
SET @A12 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@A12, 1, 1);
INSERT INTO Generates VALUES (@A12, 1);

-- Day 33 (Regression)
INSERT INTO PerformanceLog VALUES
(NULL, '2025-02-02', 50, 3, 5, 80);
SET @A13 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@A13, 1, 1);
INSERT INTO Generates VALUES (@A13, 1);

-- Day 36
INSERT INTO PerformanceLog VALUES
(NULL, '2025-02-05', 45, 3, 5, 55);
SET @A14 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@A14, 2, 1);
INSERT INTO Generates VALUES (@A14, 1);

-- Day 40
INSERT INTO PerformanceLog VALUES
(NULL, '2025-02-09', 55, 1, 5, 110);
SET @A15 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@A15, 3, 1);
INSERT INTO Generates VALUES (@A15, 1);

-- Day 43 (Recovery)
INSERT INTO PerformanceLog VALUES
(NULL, '2025-02-12', 55, 3, 5, 90);
SET @A16 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@A16, 1, 1);
INSERT INTO Generates VALUES (@A16, 1);

-- Day 47
INSERT INTO PerformanceLog VALUES
(NULL, '2025-02-16', 50, 3, 5, 65);
SET @A17 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@A17, 2, 1);
INSERT INTO Generates VALUES (@A17, 1);

-- Day 52
INSERT INTO PerformanceLog VALUES
(NULL, '2025-02-21', 60, 1, 5, 130);
SET @A18 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@A18, 3, 1);
INSERT INTO Generates VALUES (@A18, 1);

-- Day 56
INSERT INTO PerformanceLog VALUES
(NULL, '2025-02-25', 45, 3, 10, 26);
SET @A19 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@A19, 4, 1);
INSERT INTO Generates VALUES (@A19, 1);

-- Day 60
INSERT INTO PerformanceLog VALUES
(NULL, '2025-03-01', 50, 3, 5, 70);
SET @A20 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@A20, 5, 1);
INSERT INTO Generates VALUES (@A20, 1);
