from config import get_db_connection

def clear_database():
    """Clear all data from the database tables, but keep the tables."""
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Disable foreign key checks temporarily
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

        # Clear all tables in the correct order (reverse of dependencies)
        tables = ['REVIEWS', 'GAMETAGS', 'GAMES', 'TAGS', 'USERS']
        for table in tables:
            cursor.execute(f"DELETE FROM {table}")
            print(f"Cleared table: {table}")

        # Reset auto-increment counters
        cursor.execute("ALTER TABLE REVIEWS AUTO_INCREMENT = 1")
        cursor.execute("ALTER TABLE TAGS AUTO_INCREMENT = 1")

        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        connection.commit()
        print("Database cleared successfully!")

    except Exception as e:
        connection.rollback()
        print(f"Error clearing database: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    clear_database()