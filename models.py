# models.py
from get_db_connection import get_db_connection

# Members table
def create_members_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Members (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100) UNIQUE
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# WorkoutSessions table
def create_workout_sessions_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS WorkoutSessions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            member_id INT,
            session_date DATETIME,
            duration INT,
            FOREIGN KEY (member_id) REFERENCES Members(id)
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

# Call to create tables
create_members_table()
create_workout_sessions_table()
