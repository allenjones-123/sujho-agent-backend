import sqlite3

DB_NAME = "classroom.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            grade TEXT NOT NULL,
            attendance TEXT NOT NULL,
            missing_homework TEXT NOT NULL,
            latest_math_score INTEGER
        )
    ''')
    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
            INSERT INTO students (name, grade, attendance, missing_homework, latest_math_score)
            VALUES (?, ?, ?, ?, ?)
        ''', [
            ("Rohan", "Class 7", "94%", "Chapter 3: Fractions", 82),
            ("Aanya", "Class 9", "98%", "None", 95),
            ("Kabir", "Class 6", "88%", "Chapter 2: Decimals & Chapter 3", 61)
        ])
        conn.commit()
    conn.close()

def query_student_database(student_name: str) -> str:
    """Searches the core database layer for a student's real-time academic metrics."""
    print(f"🔍 [DATA LAYER]: Fetching records for student: '{student_name}'")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name, grade, attendance, missing_homework, latest_math_score FROM students WHERE name LIKE ?", 
        (f"%{student_name}%",)
    )
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return f"Student: {row[0]}, Grade: {row[1]}, Attendance: {row[2]}, Missing Homework: {row[3]}, Latest Math Score: {row[4]}/100."
    return f"No records found for '{student_name}'."