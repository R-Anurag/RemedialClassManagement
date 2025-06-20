import sqlite3

DB_NAME = 'remedial_class.db'

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

# ---------- USERS ----------
def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result

# ---------- STUDENTS ----------
def add_student(name, email, phone, course, year):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Students (name, email, phone, course, year) VALUES (?, ?, ?, ?, ?)",
                   (name, email, phone, course, year))
    conn.commit()
    conn.close()

def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Students")
    rows = cursor.fetchall()
    conn.close()
    return rows

# ---------- TEACHERS ----------
def add_teacher(name, email, phone, subject):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Teachers (name, email, phone, subject) VALUES (?, ?, ?, ?)",
                   (name, email, phone, subject))
    conn.commit()
    conn.close()

def get_all_teachers():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Teachers")
    rows = cursor.fetchall()
    conn.close()
    return rows

# ---------- SUBJECTS ----------
def add_subject(name, department):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Subjects (name, department) VALUES (?, ?)", (name, department))
    conn.commit()
    conn.close()

def get_all_subjects():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Subjects")
    rows = cursor.fetchall()
    conn.close()
    return rows

# ---------- REMEDIAL CLASSES ----------
def add_remedial_class(subject_id, teacher_id, date, time, room):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO RemedialClasses (subject_id, teacher_id, date, time, room)
        VALUES (?, ?, ?, ?, ?)""",
        (subject_id, teacher_id, date, time, room))
    conn.commit()
    conn.close()

def get_all_remedial_classes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM RemedialClasses")
    rows = cursor.fetchall()
    conn.close()
    return rows

# ---------- STUDENT-CLASS MAPPING ----------
def assign_student_to_class(student_id, class_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO StudentClassMapping (student_id, class_id) VALUES (?, ?)",
                   (student_id, class_id))
    conn.commit()
    conn.close()

# ---------- ATTENDANCE ----------
def mark_attendance(class_id, student_id, status, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Attendance (class_id, student_id, status, date)
        VALUES (?, ?, ?, ?)""",
        (class_id, student_id, status, date))
    conn.commit()
    conn.close()

def get_attendance_for_class(class_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Attendance WHERE class_id = ?", (class_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_attendance_for_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            Attendance.attendance_id,
            Attendance.class_id,
            Attendance.student_id,
            Attendance.status,
            Attendance.date,
            Subjects.name AS subject_name
        FROM Attendance
        JOIN RemedialClasses ON Attendance.class_id = RemedialClasses.class_id
        JOIN Subjects ON RemedialClasses.subject_id = Subjects.subject_id
        WHERE Attendance.student_id = ?
        ORDER BY Attendance.date DESC
    """, (student_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# ---------- PERFORMANCE ----------
def record_performance(student_id, subject_id, score_before, score_after, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Performance (student_id, subject_id, score_before, score_after, date)
        VALUES (?, ?, ?, ?, ?)""",
        (student_id, subject_id, score_before, score_after, date))
    conn.commit()
    conn.close()

def get_performance_by_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT performance_id, student_id, subject_id, score_before, score_after, date
        FROM Performance
        WHERE student_id = ?
        ORDER BY date ASC
    """, (student_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


# ---------- FEEDBACK ----------
def add_feedback(class_id, student_id, comment, rating):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Feedback (class_id, student_id, comment, rating)
        VALUES (?, ?, ?, ?)""",
        (class_id, student_id, comment, rating))
    conn.commit()
    conn.close()

def get_feedback_for_class(class_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Feedback WHERE class_id = ?", (class_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows
