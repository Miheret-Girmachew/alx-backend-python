#!/usr/bin/python3
"""
Module to demonstrate a class-based context manager for database connections.
"""
import sqlite3

DB_NAME = 'users.db' 

def setup_database_for_context_manager_test():
    """Sets up a simple SQLite database with a users table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
    ''')
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        users_data = [
            ('Context Alice', 'context.alice@example.com'),
            ('Context Bob', 'context.bob@example.com'),
            ('Context Charlie', 'context.charlie@example.com')
        ]
        cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", users_data)
        conn.commit()
        print("DB Setup: Sample users inserted for context manager test.")
    else:
        print("DB Setup: Database already contains data.")
    conn.close()

class DatabaseConnection:
    """
    A class-based context manager for handling SQLite database connections.
    Automatically opens a connection upon entering the 'with' block
    and closes it upon exiting.
    """
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None 

    def __enter__(self):
        """
        Called when entering the 'with' block.
        Establishes the database connection and returns it.
        """
        try:
            self.connection = sqlite3.connect(self.db_name)
            print(f"ContextManager LOG: Connection to '{self.db_name}' opened.")
            return self.connection 
        except sqlite3.Error as e:
            print(f"ContextManager ERROR: Failed to connect to database '{self.db_name}': {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Called when exiting the 'with' block.
        Ensures the database connection is closed.
        exc_type, exc_val, exc_tb contain exception information if an exception occurred
        within the 'with' block.
        """
        if self.connection:
            try:
                self.connection.close()
                print(f"ContextManager LOG: Connection to '{self.db_name}' closed.")
            except sqlite3.Error as e:
                print(f"ContextManager ERROR: Error closing database connection: {e}")
        
        if exc_type:
            print(f"ContextManager INFO: Exception occurred within 'with' block: {exc_type.__name__}: {exc_val}")
       
        return False

if __name__ == "__main__":
    setup_database_for_context_manager_test()

    print("\n--- Attempting to fetch users using DatabaseConnection context manager ---")
    try:
        with DatabaseConnection(DB_NAME) as conn:
            if conn: 
                cursor = conn.cursor()
                
                conn.row_factory = sqlite3.Row 
                cursor = conn.cursor()

                print("Executing query: SELECT * FROM users")
                cursor.execute("SELECT * FROM users")
                results = cursor.fetchall()

                if results:
                    print("\nQuery Results:")
                    for row in results:
                        print(dict(row)) 

                else:
                    print("No users found.")
            else:
                print("Failed to get a database connection from the context manager.")
                
    except sqlite3.Error as e:
        print(f"Main ERROR: An SQLite error occurred outside or propagated from context manager: {e}")
    except Exception as e:
        print(f"Main ERROR: An unexpected error occurred: {e}")

    print("\n--- Example: Simulating an error within the 'with' block ---")
    try:
        with DatabaseConnection(DB_NAME) as conn:
            print("ContextManager INFO: Inside 'with' block, about to raise an error.")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM non_existent_table") 
            print("This line will not be reached if the query fails.")
    except sqlite3.OperationalError as e:
        
        print(f"Main INFO: Caught expected sqlite3.OperationalError: {e}")
    except Exception as e:
        print(f"Main ERROR: Caught an unexpected error during error simulation: {e}")
    
    print("\nScript finished.")