from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root", 
        password="NewPassword123!", 
        database="fitness_db"
    )

def get_performance_trends(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    WITH volume_data AS (
        SELECT 
            p.LogID,
            p.Date,
            (p.Sets * p.Reps * p.Load) AS Volume
        FROM PerformanceLog p
        JOIN Generates g ON p.LogID = g.LogID
        WHERE g.UserID = %s
        ORDER BY p.Date
    )
    SELECT
        LogID,
        Date,
        Volume,
        AVG(Volume) OVER (
            ORDER BY Date
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) AS MovingAvg
    FROM volume_data;
    """

    cursor.execute(query, (user_id,))
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data

# def detect_plateau(trend_data):
#     plateau = False

#     # Extract moving averages in order
#     moving_avgs = [row["MovingAvg"] for row in trend_data if row["MovingAvg"] is not None]

#     # Need at least 3 data points
#     if len(moving_avgs) < 3:
#         return False

#     # Check last 3 moving averages
#     if moving_avgs[-1] <= moving_avgs[-2] <= moving_avgs[-3]:
#         plateau = True

#     return plateau

def detect_plateau(trend_data, threshold=0.01):
    # Extract moving averages
    moving_avgs = [row["MovingAvg"] for row in trend_data if row["MovingAvg"] is not None]

    if len(moving_avgs) < 3:
        return False

    # Last 3 values
    a, b, c = moving_avgs[-3], moving_avgs[-2], moving_avgs[-1]

    # Calculate increases
    inc1 = b - a
    inc2 = c - b

    # Check if increases are below threshold
    if inc1 < threshold and inc2 < threshold:
        return True

    return False

def get_category_distribution(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT ts.Category, COUNT(*) AS Count
        FROM Perform p
        JOIN Training_Session ts ON p.WorkoutId = ts.WorkoutId
        WHERE p.UserID = %s
        GROUP BY ts.Category;
    """

    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

# @app.route("/")
# def home():
#     return redirect(url_for("global_dashboard"))

@app.route("/home")
def home():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # --- KPI Cards ---
    cursor.execute("SELECT COUNT(*) AS total_users FROM User")
    total_users = cursor.fetchone()["total_users"]

    cursor.execute("SELECT COUNT(*) AS total_workouts FROM PerformanceLog")
    total_workouts = cursor.fetchone()["total_workouts"]

    cursor.execute("SELECT COUNT(*) AS total_exercises FROM Includes")
    total_exercises = cursor.fetchone()["total_exercises"]

    cursor.execute("SELECT COUNT(*) AS total_nutrition FROM NutritionLog")
    total_nutrition = cursor.fetchone()["total_nutrition"]

    # --- Workouts per Week (Line Chart) ---
    cursor.execute("""
        SELECT 
            YEAR(Date) AS year,
            WEEK(Date) AS week,
            COUNT(*) AS count
        FROM PerformanceLog
        GROUP BY YEAR(Date), WEEK(Date)
        ORDER BY year, week
    """)
    workouts_per_week = cursor.fetchall()

    # --- Category Distribution (Pie Chart) ---
    cursor.execute("""
        SELECT 
            ts.Category,
            COUNT(*) AS count
        FROM Training_Session ts
        JOIN Includes i ON ts.WorkoutId = i.WorkoutId AND ts.ExerciseID = i.ExerciseID
        GROUP BY ts.Category
    """)
    category_distribution = cursor.fetchall()

    # --- Top 5 Active Users ---
    cursor.execute("""
        SELECT 
            u.Name,
            COUNT(pl.LogID) AS workout_count,
            SUM(pl.Sets * pl.Reps * pl.Load) AS total_volume
        FROM PerformanceLog pl
        JOIN Generates g ON pl.LogID = g.LogID
        JOIN User u ON g.UserID = u.UserID
        GROUP BY u.UserID
        ORDER BY workout_count DESC
        LIMIT 5
    """)
    top_users = cursor.fetchall()

    # --- Recent Activity Feed ---
    cursor.execute("""
        SELECT 
            u.Name,
            pl.Date,
            'workout' AS type
        FROM PerformanceLog pl
        JOIN Generates g ON pl.LogID = g.LogID
        JOIN User u ON g.UserID = u.UserID
        ORDER BY pl.Date DESC
        LIMIT 8
    """)
    recent_activity = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "home.html",
        total_users=total_users,
        total_workouts=total_workouts,
        total_exercises=total_exercises,
        total_nutrition=total_nutrition,
        workouts_per_week=workouts_per_week,
        category_distribution=category_distribution,
        top_users=top_users,
        recent_activity=recent_activity
    )


@app.route("/dashboard")
def global_dashboard():
    return render_template("global_dashboard.html")

@app.route("/")
def index():
    return "Hello, Fitness App!"

@app.route("/users")
def users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM User")
    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("users.html", users=users)

@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        name = request.form["name"]
        dob = request.form["dob"]
        height = request.form["height"]
        weight = request.form["weight"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO User (Name, Date_of_birth, Height, Weight)
            VALUES (%s, %s, %s, %s)
        """, (name, dob, height, weight))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("users"))

    return render_template("add_user.html")

@app.route("/edit_user/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # GET request → load existing user data
    if request.method == "GET":
        cursor.execute("SELECT * FROM User WHERE UserID = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template("edit_user.html", user=user)

    # POST request → update user
    name = request.form["name"]
    dob = request.form["dob"]
    height = request.form["height"]
    weight = request.form["weight"]

    cursor.execute("""
        UPDATE User
        SET Name=%s, Date_of_birth=%s, Height=%s, Weight=%s
        WHERE UserID=%s
    """, (name, dob, height, weight, user_id))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("users"))

@app.route("/user/<int:user_id>")
def user_detail(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM User WHERE UserID = %s", (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("user_detail.html", user=user)

@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM User WHERE UserID = %s", (user_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("users"))

@app.route("/performance/<int:user_id>")
def performance_logs(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            pl.LogID,
            pl.Date,
            pl.Duration,
            pl.Sets,
            pl.Reps,
            pl.Load,
            (pl.Sets * pl.Reps * pl.Load) AS Volume,
            ts.WorkoutId,
            ts.Exercise_Name AS Exercise,
            ts.Category,
            ts.Equipment
        FROM PerformanceLog pl
        JOIN Generates g ON pl.LogID = g.LogID
        JOIN Includes i ON pl.LogID = i.LogID
        JOIN Training_Session ts 
            ON i.WorkoutId = ts.WorkoutId 
           AND i.ExerciseID = ts.ExerciseID
        WHERE g.UserID = %s
        ORDER BY pl.Date DESC
    """, (user_id,))

    logs = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("performance.html", logs=logs, user_id=user_id)

@app.route("/performance/<int:user_id>/add", methods=["GET", "POST"])
def add_performance(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # get available exercises (training sessions)
    cursor.execute("""
        SELECT WorkoutId, ExerciseID, Exercise_Name, Category
        FROM Training_Session
        ORDER BY WorkoutId, Exercise_Name
    """)
    exercises = cursor.fetchall()

    if request.method == "POST":
        date = request.form["date"]
        duration = request.form["duration"]
        sets = request.form["sets"]
        reps = request.form["reps"]
        load = request.form["load"]
        workout_id = request.form["workout_id"]
        exercise_id = request.form["exercise_id"]

        # 1) insert into PerformanceLog
        cursor.execute("""
            INSERT INTO PerformanceLog (Date, Duration, Sets, Reps, Load)
            VALUES (%s, %s, %s, %s, %s)
        """, (date, duration, sets, reps, load))
        log_id = cursor.lastrowid

        # 2) link to user (Generates)
        cursor.execute("""
            INSERT INTO Generates (LogID, UserID)
            VALUES (%s, %s)
        """, (log_id, user_id))

        # 3) link to training session (Includes)
        cursor.execute("""
            INSERT INTO Includes (LogID, WorkoutId, ExerciseID)
            VALUES (%s, %s, %s)
        """, (log_id, workout_id, exercise_id))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("performance_logs", user_id=user_id))

    cursor.close()
    conn.close()
    return render_template("add_performance.html", user_id=user_id, exercises=exercises)

@app.route("/performance/edit/<int:log_id>", methods=["GET", "POST"])
def edit_performance(log_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            pl.LogID,
            g.UserID,
            pl.Date,
            pl.Duration,
            pl.Sets,
            pl.Reps,
            pl.Load
        FROM PerformanceLog pl
        JOIN Generates g USING (LogID)
        WHERE pl.LogID = %s
    """, (log_id,))
    log = cursor.fetchone()

    if not log:
        cursor.close()
        conn.close()
        return "Log not found", 404

    user_id = log["UserID"]

    if request.method == "POST":
        date = request.form["date"]
        duration = request.form["duration"]
        sets = request.form["sets"]
        reps = request.form["reps"]
        load = request.form["load"]

        cursor.execute("""
            UPDATE PerformanceLog
            SET Date=%s, Duration=%s, Sets=%s, Reps=%s, Load=%s
            WHERE LogID=%s
        """, (date, duration, sets, reps, load, log_id))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("performance_logs", user_id=user_id))

    cursor.close()
    conn.close()
    return render_template("edit_performance.html", log=log)

@app.route("/performance/delete/<int:log_id>", methods=["POST"])
def delete_performance(log_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # get user_id first
    cursor.execute("""
        SELECT UserID FROM Generates WHERE LogID = %s
    """, (log_id,))
    row = cursor.fetchone()
    if not row:
        cursor.close()
        conn.close()
        return "Log not found", 404
    user_id = row["UserID"]

    # delete from Includes, Generates, then PerformanceLog
    cursor.execute("DELETE FROM Includes WHERE LogID = %s", (log_id,))
    cursor.execute("DELETE FROM Generates WHERE LogID = %s", (log_id,))
    cursor.execute("DELETE FROM PerformanceLog WHERE LogID = %s", (log_id,))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("performance_logs", user_id=user_id))

# -------------------------------------------------------------
# GLOBAL NUTRITION PAGE (The top navigation link)
# -------------------------------------------------------------
@app.route('/nutrition')
def nutrition():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch the most recent nutrition logs across ALL users
    query = """
        SELECT n.NutritionLogID, n.Date, n.Calorie_intake, n.Macros, u.Name, u.UserID
        FROM NutritionLog n
        JOIN Records r ON n.NutritionLogID = r.NutritionLogID
        JOIN User u ON r.UserID = u.UserID
        ORDER BY n.Date DESC
        LIMIT 50
    """
    cursor.execute(query)
    recent_logs = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('nutrition.html', logs=recent_logs)

@app.route("/nutrition/<int:user_id>")
def nutrition_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
        n.NutritionLogID,
        n.Date,
        n.Calorie_intake,
        n.Macros
    FROM NutritionLog n
    JOIN Records r ON n.NutritionLogID = r.NutritionLogID
    WHERE r.UserID = %s
    ORDER BY n.Date DESC;
    """

    cursor.execute(query, (user_id,))
    logs = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("nutrition_user.html", logs=logs, user_id=user_id)

@app.route("/workouts")
def workouts():
    # Get filter parameters from query string
    filter_user_id = request.args.get("user_id")
    filter_date = request.args.get("date")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Base query
    query = """
        SELECT 
            ts.WorkoutId AS WorkoutID,
            u.UserID,
            u.Name AS UserName,
            pl.Date,
            SUM(pl.Duration) AS TotalDuration,
            SUM(pl.Sets * pl.Reps * pl.Load) AS TotalVolume
        FROM PerformanceLog pl
        JOIN Includes i 
            ON pl.LogID = i.LogID
        JOIN Training_Session ts 
            ON i.WorkoutId = ts.WorkoutId 
            AND i.ExerciseID = ts.ExerciseID
        JOIN Generates g 
            ON pl.LogID = g.LogID
        JOIN User u 
            ON g.UserID = u.UserID
    """

    # Build WHERE clause based on filters
    where_clauses = []
    params = []

    if filter_user_id:
        where_clauses.append("u.UserID = %s")
        params.append(filter_user_id)

    if filter_date:
        where_clauses.append("pl.Date = %s")
        params.append(filter_date)

    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)

    query += " GROUP BY ts.WorkoutId, u.UserID, u.Name, pl.Date ORDER BY pl.Date DESC"

    cursor.execute(query, tuple(params))
    workouts = cursor.fetchall()

    # Get list of all users for the filter dropdown
    cursor.execute("SELECT UserID, Name FROM User ORDER BY Name")
    users = cursor.fetchall()

    # Get list of all unique dates for the filter dropdown
    cursor.execute("""
        SELECT DISTINCT Date FROM PerformanceLog ORDER BY Date DESC
    """)
    dates = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "workouts.html",
        workouts=workouts,
        users=users,
        dates=dates,
        selected_user_id=filter_user_id,
        selected_date=filter_date
    )

@app.route("/workout/<int:user_id>/<date>")
def workout_detail(user_id, date):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            PerformanceLog.LogID,
            PerformanceLog.Date,
            PerformanceLog.Duration,
            PerformanceLog.Sets,
            PerformanceLog.Reps,
            PerformanceLog.`Load`,
            ts.Exercise_Name,
            ts.Category
        FROM PerformanceLog
        JOIN Includes 
            ON PerformanceLog.LogID = Includes.LogID
        JOIN Training_Session ts
            ON Includes.WorkoutID = ts.WorkoutID AND Includes.ExerciseID = ts.ExerciseID
        JOIN Generates
            ON PerformanceLog.LogID = Generates.LogID
        WHERE Generates.UserID = %s
          AND PerformanceLog.Date = %s
        ORDER BY PerformanceLog.LogID;
    """

    cursor.execute(query, (user_id, date))
    entries = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "workout_detail.html",
        user_id=user_id,
        date=date,
        entries=entries
    )

@app.route("/workouts/delete", methods=["POST"])
def delete_workout():
    user_id = request.form["user_id"]
    date = request.form["date"]

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # First, find the LogIDs to delete
        cursor.execute("""
            SELECT pl.LogID
            FROM PerformanceLog pl
            JOIN Generates g ON pl.LogID = g.LogID
            WHERE g.UserID = %s AND pl.Date = %s
        """, (user_id, date))
        rows = cursor.fetchall()
        log_ids = [row[0] for row in rows]

        if log_ids:
            placeholders = ','.join(['%s'] * len(log_ids))
            # Delete from Includes first (foreign key dependency)
            cursor.execute(f"DELETE FROM Includes WHERE LogID IN ({placeholders})", tuple(log_ids))
            # Delete from Generates
            cursor.execute(f"DELETE FROM Generates WHERE LogID IN ({placeholders})", tuple(log_ids))
            # Delete from PerformanceLog last
            cursor.execute(f"DELETE FROM PerformanceLog WHERE LogID IN ({placeholders})", tuple(log_ids))

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("workouts"))

@app.route("/workouts/create", methods=["GET", "POST"])
def create_workout():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Load users
    cursor.execute("SELECT UserID, Name FROM User")
    users = cursor.fetchall()

    # Load exercises from Training_Session
    # cursor.execute("SELECT ExerciseID, Exercise_Name FROM Training_Session")
    cursor.execute("""
        SELECT DISTINCT ExerciseID, Exercise_Name
        FROM Training_Session
        WHERE Exercise_Name IS NOT NULL
    """)

    exercises = cursor.fetchall()

    if request.method == "POST":
        user_id = request.form["user_id"]
        date = request.form["date"]
        duration = request.form["duration"]

        exercise_ids = request.form.getlist("exercise_id")
        sets_list = request.form.getlist("sets")
        reps_list = request.form.getlist("reps")
        load_list = request.form.getlist("load")

        # Validate that all lists have the same length
        if not (len(exercise_ids) == len(sets_list) == len(reps_list) == len(load_list)):
            cursor.close()
            conn.close()
            return "Error: Mismatched form data lengths", 400

        # Validate that we have at least one exercise
        if len(exercise_ids) == 0:
            cursor.close()
            conn.close()
            return "Error: No exercises selected", 400

        cursor2 = conn.cursor(dictionary=True)

        try:
            # ---------------------------------------------------------
            # 1. Generate a new WorkoutID (virtual grouping ID)
            # ---------------------------------------------------------
            # Use a more robust approach to avoid race conditions
            cursor2.execute("SELECT IFNULL(MAX(WorkoutID), 0) + 1 FROM (SELECT WorkoutID FROM Includes UNION SELECT WorkoutID FROM Perform) AS all_workouts")

            workout_id = list(cursor2.fetchone().values())[0]


            # ---------------------------------------------------------
            # 2. Insert each exercise as a PerformanceLog row
            # ---------------------------------------------------------
            for i in range(len(exercise_ids)):
                sets = int(sets_list[i])
                reps = int(reps_list[i])
                load = float(load_list[i])

                # Insert PerformanceLog
                cursor2.execute("""
                    INSERT INTO PerformanceLog (Date, Duration, Sets, Reps, `Load`)
                    VALUES (%s, %s, %s, %s, %s)
                """, (date, duration, sets, reps, load))

                log_id = cursor2.lastrowid

                # STEP 1 — fetch exercise metadata
                cursor2.execute("""
                    SELECT Exercise_Name, Category, Equipment, Target_Goal
                    FROM Training_Session
                    WHERE ExerciseID = %s
                    ORDER BY WorkoutID ASC
                    LIMIT 1
                """, (exercise_ids[i],))
                exercise_meta = cursor2.fetchone()

                # STEP 2 — insert full Training_Session row
                cursor2.execute("""
                    INSERT INTO Training_Session (WorkoutID, ExerciseID, Exercise_Name, Category, Equipment, Target_Goal)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    workout_id,
                    exercise_ids[i],
                    exercise_meta["Exercise_Name"],
                    exercise_meta["Category"],
                    exercise_meta["Equipment"],
                    exercise_meta["Target_Goal"]
                ))

                # Insert into Includes
                cursor2.execute("""
                    INSERT INTO Includes (LogID, WorkoutID, ExerciseID)
                    VALUES (%s, %s, %s)
                """, (log_id, workout_id, exercise_ids[i]))

                # Insert into Perform
                cursor2.execute("""
                    INSERT INTO Perform (WorkoutID, ExerciseID, UserID)
                    VALUES (%s, %s, %s)
                """, (workout_id, exercise_ids[i], user_id))

            conn.commit()
            cursor2.close()
            cursor.close()
            conn.close()

            return redirect(url_for("workouts"))

        except Exception as e:
            conn.rollback()
            cursor2.close()
            cursor.close()
            conn.close()
            return f"Error creating workout: {str(e)}", 500

    cursor.close()
    conn.close()

    return render_template("create_workout.html", users=users, exercises=exercises)

@app.route("/workouts/<int:user_id>")
def workouts_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
        ts.WorkoutId,
        ts.ExerciseID,
        ts.Exercise_Name,
        ts.Category,
        ts.Equipment,
        ts.Target_goal
    FROM Perform p
    JOIN Training_Session ts 
        ON p.WorkoutId = ts.WorkoutId
    WHERE p.UserID = %s
    ORDER BY ts.WorkoutId, ts.ExerciseID;
    """

    cursor.execute(query, (user_id,))
    workouts = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("workouts_user.html", workouts=workouts, user_id=user_id)

@app.route("/dashboard/<int:user_id>")
def dashboard(user_id):
    # Get date range filter from query string
    date_range = request.args.get("range", "all")  # Default to All Time

    # Get trend data (volume + moving average)
    trend_data = get_performance_trends(user_id)

    # Filter by date range if not "all"
    if date_range != "all" and trend_data:
        try:
            days = int(date_range)
            # Find the most recent date in the data
            max_date = max(row["Date"] for row in trend_data)
            from datetime import timedelta
            cutoff_date = max_date - timedelta(days=days)
            trend_data = [row for row in trend_data if row["Date"] >= cutoff_date]
        except (ValueError, TypeError):
            pass  # If invalid range, show all data

    plateau = detect_plateau(trend_data)

    # Line chart data
    dates = [row["Date"].strftime("%Y-%m-%d") for row in trend_data]
    volumes = [row["Volume"] for row in trend_data]
    moving_avg = [row["MovingAvg"] for row in trend_data]

    # Pie chart data
    category_data = get_category_distribution(user_id)
    categories = [row["Category"] for row in category_data]
    category_counts = [row["Count"] for row in category_data]

    return render_template(
        "dashboard.html",
        user_id=user_id,
        dates=dates,
        volumes=volumes,
        moving_avg=moving_avg,
        plateau=plateau,
        categories=categories,
        category_counts=category_counts,
        selected_range=date_range
    )


if __name__ == "__main__":
    app.run(debug=True, port=5002)