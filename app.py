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

@app.route("/")
def home():
    return redirect(url_for("global_dashboard"))

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

@app.route("/nutrition")
def nutrition():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM NutritionLog ORDER BY Date DESC")
    logs = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("nutrition.html", logs=logs)

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
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            MIN(PerformanceLog.LogID) AS WorkoutID,
            User.UserID,
            User.Name AS UserName,
            PerformanceLog.Date,
            SUM(PerformanceLog.Duration) AS TotalDuration,
            SUM(PerformanceLog.Sets * PerformanceLog.Reps * PerformanceLog.`Load`) AS TotalVolume
        FROM PerformanceLog
        JOIN Includes 
            ON PerformanceLog.LogID = Includes.LogID
        JOIN Perform 
            ON Includes.WorkoutID = Perform.WorkoutID
            AND Includes.ExerciseID = Perform.ExerciseID
        JOIN User 
            ON Perform.UserID = User.UserID
        GROUP BY User.UserID, PerformanceLog.Date
        ORDER BY PerformanceLog.Date DESC;
    """

    cursor.execute(query)
    workouts = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("workouts.html", workouts=workouts)

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
            ExerciseLibrary.Exercise_Name,
            ExerciseLibrary.Category
        FROM PerformanceLog
        JOIN Includes 
            ON PerformanceLog.LogID = Includes.LogID
        JOIN ExerciseLibrary 
            ON Includes.ExerciseID = ExerciseLibrary.ExerciseID
        WHERE PerformanceLog.UserID = %s
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

    cursor.execute("""
        DELETE FROM PerformanceLog
        WHERE UserID = %s AND Date = %s
    """, (user_id, date))

    conn.commit()
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
    cursor.execute("SELECT ExerciseID, Exercise_Name FROM Training_Session")
    exercises = cursor.fetchall()

    if request.method == "POST":
        user_id = request.form["user_id"]
        date = request.form["date"]
        duration = request.form["duration"]

        exercise_ids = request.form.getlist("exercise_id")
        sets_list = request.form.getlist("sets")
        reps_list = request.form.getlist("reps")
        load_list = request.form.getlist("load")

        cursor2 = conn.cursor()

        # ---------------------------------------------------------
        # 1. Generate a new WorkoutID (virtual grouping ID)
        # ---------------------------------------------------------
        cursor2.execute("SELECT IFNULL(MAX(WorkoutID), 0) + 1 FROM Includes")
        workout_id = cursor2.fetchone()[0]

        # ---------------------------------------------------------
        # 2. Insert each exercise as a PerformanceLog row
        # ---------------------------------------------------------
        for i in range(len(exercise_ids)):

            cursor2.execute("""
                INSERT INTO PerformanceLog (Date, Duration, Sets, Reps, `Load`)
                VALUES (%s, %s, %s, %s, %s)
            """, (date, duration, sets_list[i], reps_list[i], load_list[i]))

            log_id = cursor2.lastrowid

            # ---------------------------------------------------------
            # 3. Link LogID → WorkoutID + ExerciseID in Includes
            # ---------------------------------------------------------
            cursor2.execute("""
                INSERT INTO Includes (LogID, WorkoutID, ExerciseID)
                VALUES (%s, %s, %s)
            """, (log_id, workout_id, exercise_ids[i]))

            # ---------------------------------------------------------
            # 4. Link WorkoutID + ExerciseID → UserID in Perform
            # ---------------------------------------------------------
            cursor2.execute("""
                INSERT INTO Perform (WorkoutID, ExerciseID, UserID)
                VALUES (%s, %s, %s)
            """, (workout_id, exercise_ids[i], user_id))

        conn.commit()
        cursor2.close()
        cursor.close()
        conn.close()

        return redirect(url_for("workouts"))

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
    # Get trend data (volume + moving average)
    trend_data = get_performance_trends(user_id)
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
        category_counts=category_counts
    )


if __name__ == "__main__":
    app.run(debug=True)
