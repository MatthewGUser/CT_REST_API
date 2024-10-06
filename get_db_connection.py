import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',   # Update to your MySQL username
        password='',  # Update to your MySQL password
        database='fitness'  # Update to your database name
    )
