import sqlite3

conn = sqlite3.connect("remedial_class.db")
cursor = conn.cursor()

# Users
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    username TEXT UNIQUE,
    password_hash TEXT,
    role TEXT
)
""")

# Students
cursor.execute("""
CREATE TABLE IF NOT EXISTS Students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT,
    course TEXT,
    year TEXT
)
""")

# Teachers
cursor.execute("""
CREATE TABLE IF NOT EXISTS Teachers (
    teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT,
    subject TEXT
)
""")

# Subjects
cursor.execute("""
CREATE TABLE IF NOT EXISTS Subjects (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    department TEXT
)
""")

# RemedialClasses
cursor.execute("""
CREATE TABLE IF NOT EXISTS RemedialClasses (
    class_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER,
    teacher_id INTEGER,
    date TEXT,
    time TEXT,
    room TEXT
)
""")

# StudentClassMapping
cursor.execute("""
CREATE TABLE IF NOT EXISTS StudentClassMapping (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    class_id INTEGER
)
""")

# Attendance
cursor.execute("""
CREATE TABLE IF NOT EXISTS Attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_id INTEGER,
    student_id INTEGER,
    status TEXT,
    date TEXT
)
""")

# Performance
cursor.execute("""
CREATE TABLE IF NOT EXISTS Performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject_id INTEGER,
    score_before INTEGER,
    score_after INTEGER,
    date TEXT
)
""")

# Feedback
cursor.execute("""
CREATE TABLE IF NOT EXISTS Feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_id INTEGER,
    student_id INTEGER,
    comment TEXT,
    rating INTEGER
)
""")

conn.commit()
conn.close()

print("✅ Database initialized successfully.")
