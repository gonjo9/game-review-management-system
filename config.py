import mysql.connector

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Change to your MySQL username
    'password': 'root',  # Change to your MySQL password
    'database': 'game_db'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)
