-- ============================================
-- BLOCK 3-C: PERFORMANCE LOGS FOR JAMES (UserID = 3)
-- Beginner linear progression with small noise
-- ============================================

-- Day 1
INSERT INTO PerformanceLog (Date, Duration, Sets, Reps, `Load`)
VALUES ('2025-01-01', 40, 3, 5, 55); -- Squat
SET @J1 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@J1, 1, 1);
INSERT INTO Generates VALUES (@J1, 3);

-- Day 3
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-03', 35, 3, 5, 40); -- Bench Press
SET @J2 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@J2, 2, 1);
INSERT INTO Generates VALUES (@J2, 3);

-- Day 6
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-06', 45, 1, 5, 95); -- Deadlift
SET @J3 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@J3, 3, 1);
INSERT INTO Generates VALUES (@J3, 3);

-- Day 8
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-08', 30, 3, 12, 12); -- Kettlebell Swing
SET @J4 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@J4, 4, 1);
INSERT INTO Generates VALUES (@J4, 3);

-- Day 10
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-10', 35, 3, 5, 28); -- Overhead Press
SET @J5 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@J5, 5, 1);
INSERT INTO Generates VALUES (@J5, 3);

-- Day 13
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-13', 40, 3, 5, 58); -- Squat
SET @J6 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@J6, 1, 1);
INSERT INTO Generates VALUES (@J6, 3);

-- Day 16
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-16', 35, 3, 5, 42); -- Bench
SET @J7 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@J7, 2, 1);
INSERT INTO Generates VALUES (@J7, 3);

-- Day 19
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-19', 45, 1, 5, 98); -- Deadlift
SET @J8 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@J8, 3, 1);
INSERT INTO Generates VALUES (@J8, 3);

-- Day 22
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-22', 30, 3, 12, 13); -- Kettlebell Swing
SET @J9 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@J9, 4, 1);
INSERT INTO Generates VALUES (@J9, 3);

-- Day 25
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-25', 35, 3, 5, 30); -- Overhead Press
SET @J10 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@J10, 5, 1);
INSERT INTO Generates VALUES (@J10, 3);

-- Day 28
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-28', 40, 3, 5, 60); -- Squat
SET @J11 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@J11, 1, 1);
INSERT INTO Generates VALUES (@J11, 3);

-- Day 31
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-31', 35, 3, 5, 44); -- Bench
SET @J12 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@J12, 2, 1);
INSERT INTO Generates VALUES (@J12, 3);

-- Day 34
INSERT INTO PerformanceLog VALUES
(NULL, '2025-02-03', 45, 1, 5, 100); -- Deadlift
SET @J13 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@J13, 3, 1);
INSERT INTO Generates VALUES (@J13, 3);

-- Day 37
INSERT INTO PerformanceLog VALUES
(NULL, '2025-02-06', 30, 3, 12, 14); -- Kettlebell Swing
SET @J14 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@J14, 4, 1);
INSERT INTO Generates VALUES (@J14, 3);

-- Day 40
INSERT INTO PerformanceLog VALUES
(NULL, '2025-02-09', 35, 3, 5, 32); -- Overhead Press
SET @J15 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@J15, 5, 1);
INSERT INTO Generates VALUES (@J15, 3);

-- Day 43
INSERT INTO PerformanceLog VALUES
(NULL, '2025-02-12', 40, 3, 5, 62); -- Squat
SET @J16 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@J16, 1, 1);
INSERT INTO Generates VALUES (@J16, 3);

-- Day 47
INSERT INTO PerformanceLog VALUES
(NULL, '2025-02-16', 35, 3, 5, 46); -- Bench
SET @J17 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@J17, 2, 1);
INSERT INTO Generates VALUES (@J17, 3);

-- Day 51
INSERT INTO PerformanceLog VALUES
(NULL, '2025-02-20', 45, 1, 5, 102); -- Deadlift
SET @J18 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@J18, 3, 1);
INSERT INTO Generates VALUES (@J18, 3);

-- Day 55
INSERT INTO PerformanceLog VALUES
(NULL, '2025-02-24', 30, 3, 12, 15); -- Kettlebell Swing
SET @J19 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@J19, 4, 1);
INSERT INTO Generates VALUES (@J19, 3);

-- Day 60
INSERT INTO PerformanceLog VALUES
(NULL, '2025-03-01', 35, 3, 5, 34); -- Overhead Press
SET @J20 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@J20, 5, 1);
INSERT INTO Generates VALUES (@J20, 3);
