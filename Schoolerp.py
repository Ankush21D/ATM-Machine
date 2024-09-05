import mysql.connector
from mysql.connector import Error

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ankush2003#",
    port="3306",
    database="school_erp"
)
cursor = conn.cursor()

# Create necessary tables
def create_tables():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS superadmin (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS class (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        class_id INT,
        FOREIGN KEY (class_id) REFERENCES class(id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id INT,
        date DATE,
        status VARCHAR(255),
        FOREIGN KEY (student_id) REFERENCES student(id)
    )
    """)
    conn.commit()

# Register Superadmin
def register_superadmin(username, password):
    cursor.execute("INSERT INTO superadmin (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()

# Register Admin
def register_admin(username, password):
    cursor.execute("INSERT INTO admin (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()

# Login Superadmin
def login_superadmin(username, password):
    cursor.execute("SELECT * FROM superadmin WHERE username = %s AND password = %s", (username, password))
    return cursor.fetchone()

# Login Admin
def login_admin(username, password):
    cursor.execute("SELECT * FROM admin WHERE username = %s AND password = %s", (username, password))
    return cursor.fetchone()

# Create Class
def create_class(class_name):
    cursor.execute("INSERT INTO class (name) VALUES (%s)", (class_name,))
    conn.commit()

# Add Student
def add_student(student_name, class_id):
    cursor.execute("INSERT INTO student (name, class_id) VALUES (%s, %s)", (student_name, class_id))
    conn.commit()

# Mark Attendance
def mark_attendance(student_id, date, status):
    cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)", (student_id, date, status))
    conn.commit()

# Example Usage
if __name__ == "__main__":
    create_tables()

    # Register and login Superadmin
    register_superadmin('superadmin', 'superpassword')
    superadmin = login_superadmin('superadmin', 'superpassword')
    if superadmin:
        print("Superadmin logged in")

        # Register Admin
        register_admin('admin', 'adminpassword')
        admin = login_admin('admin', 'adminpassword')
        if admin:
            print("Admin logged in")

            # Create Class
            create_class('Class A')

            # Add Student
            cursor.execute("SELECT id FROM class WHERE name = %s", ('Class A',))
            class_id = cursor.fetchone()[0]
            add_student('Student 1', class_id)

            # Mark Attendance
            cursor.execute("SELECT id FROM student WHERE name = %s", ('Student 1',))
            student_id = cursor.fetchone()[0]
            mark_attendance(student_id, '2024-08-05', 'Present')
        else:
            print("Admin login failed")
    else:
        print("Superadmin login failed")

# Close the connection
conn.close()
