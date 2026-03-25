-- ============================================
-- BLOCK 3-B: PERFORMANCE LOGS FOR MARIA (UserID = 2)
-- Smooth progression, no plateau
-- ============================================

-- Day 2
INSERT INTO PerformanceLog (Date, Duration, Sets, Reps, `Load`)
VALUES ('2025-01-02', 45, 3, 8, 45); -- Squat
SET @M1 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@M1, 1, 1);
INSERT INTO Generates VALUES (@M1, 2);

-- Day 4
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-04', 40, 3, 8, 30); -- Bench Press
SET @M2 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@M2, 2, 1);
INSERT INTO Generates VALUES (@M2, 2);

-- Day 6
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-06', 50, 1, 5, 85); -- Deadlift
SET @M3 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@M3, 3, 1);
INSERT INTO Generates VALUES (@M3, 2);

-- Day 9
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-09', 35, 3, 12, 16); -- Kettlebell Swing
SET @M4 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@M4, 4, 1);
INSERT INTO Generates VALUES (@M4, 2);

-- Day 11
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-11', 40, 3, 8, 32); -- Overhead Press
SET @M5 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@M5, 5, 1);
INSERT INTO Generates VALUES (@M5, 2);

-- Day 13
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-13', 45, 3, 8, 48); -- Squat
SET @M6 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@M6, 1, 1);
INSERT INTO Generates VALUES (@M6, 2);

-- Day 16
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-16', 40, 3, 8, 33); -- Bench
SET @M7 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@M7, 2, 1);
INSERT INTO Generates VALUES (@M7, 2);

-- Day 19
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-19', 50, 1, 5, 88); -- Deadlift
SET @M8 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@M8, 3, 1);
INSERT INTO Generates VALUES (@M8, 2);

-- Day 22
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-22', 35, 3, 12, 17); -- Kettlebell Swing
SET @M9 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@M9, 4, 1);
INSERT INTO Generates VALUES (@M9, 2);

-- Day 25
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-25', 40, 3, 8, 34); -- Overhead Press
SET @M10 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@M10, 5, 1);
INSERT INTO Generates VALUES (@M10, 2);

-- Day 28
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-28', 45, 3, 8, 50); -- Squat
SET @M11 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@M11, 1, 1);
INSERT INTO Generates VALUES (@M11, 2);

-- Day 31
INSERT INTO PerformanceLog VALUES
(NULL, '2025-01-31', 40, 3, 8, 35); -- Bench
SET @M12 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@M12, 2, 1);
INSERT INTO Generates VALUES (@M12, 2);

-- Day 34
INSERT INTO PerformanceLog VALUES
(NULL, '2025-02-03', 50, 1, 5, 90); -- Deadlift
SET @M13 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@M13, 3, 1);
INSERT INTO Generates VALUES (@M13, 2);

-- Day 38
INSERT INTO PerformanceLog VALUES
(NULL, '2025-02-07', 35, 3, 12, 18); -- Kettlebell Swing
SET @M14 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@M14, 4, 1);
INSERT INTO Generates VALUES (@M14, 2);

-- Day 41
INSERT INTO PerformanceLog VALUES
(NULL, '2025-02-10', 40, 3, 8, 36); -- Overhead Press
SET @M15 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@M15, 5, 1);
INSERT INTO Generates VALUES (@M15, 2);

-- Day 45
INSERT INTO PerformanceLog VALUES
(NULL, '2025-02-14', 45, 3, 8, 52); -- Squat
SET @M16 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@M16, 1, 1);
INSERT INTO Generates VALUES (@M16, 2);

-- Day 49
INSERT INTO PerformanceLog VALUES
(NULL, '2025-02-18', 40, 3, 8, 37); -- Bench
SET @M17 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@M17, 2, 1);
INSERT INTO Generates VALUES (@M17, 2);

-- Day 53
INSERT INTO PerformanceLog VALUES
(NULL, '2025-02-22', 50, 1, 5, 92); -- Deadlift
SET @M18 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@M18, 3, 1);
INSERT INTO Generates VALUES (@M18, 2);

-- Day 57
INSERT INTO PerformanceLog VALUES
(NULL, '2025-02-26', 35, 3, 12, 19); -- Kettlebell Swing
SET @M19 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@M19, 4, 1);
INSERT INTO Generates VALUES (@M19, 2);

-- Day 60
INSERT INTO PerformanceLog VALUES
(NULL, '2025-03-01', 40, 3, 8, 38); -- Overhead Press
SET @M20 = LAST_INSERT_ID();
INSERT INTO Includes VALUES (@M20, 5, 1);
INSERT INTO Generates VALUES (@M20, 2);
