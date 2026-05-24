import sqlite3

DB_NAME = "classroom.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Core Students Table (Remains the same)
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
    
    # 2. NEW: Users & Permissions Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            phone_number TEXT PRIMARY KEY,
            user_name TEXT NOT NULL,
            role TEXT NOT NULL,          -- 'TEACHER', 'PARENT', or 'STUDENT'
            associated_student TEXT      -- Name of their child if PARENT, else NULL
        )
    ''')
    
    # Seed Students if empty
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
        
    # Seed Users with your actual Sandbox phone number to test both roles!
    # Note: We will dynamically mock your number in main.py so you can experience how both roles behave.
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
            INSERT INTO users (phone_number, user_name, role, associated_student)
            VALUES (?, ?, ?, ?)
        ''', [
            ("whatsapp:+916397369084", "Anjali Sharma", "PARENT", "Rohan"), 
            ("whatsapp:+919999999999", "Vikram Sai", "TEACHER", None),
            ("whatsapp:+911111111111", "Kabir", "STUDENT", None)
        ])
        
    conn.commit()
    conn.close()

def get_user_profile(phone_number: str):
    """Fetches user permissions based on their incoming WhatsApp phone identifier."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_name, role, associated_student FROM users WHERE phone_number = ?", (phone_number,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"name": row[0], "role": row[1], "associated_student": row[2]}
    return None

def query_student_database(student_name: str) -> str:
    """Core SQL lookup engine for student records."""
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