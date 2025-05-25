#!/usr/bin/python3
"""
Module to demonstrate a reusable class-based context manager
for executing a specific database query.
"""
import sqlite3

DB_NAME = 'users.db' 
def setup_database_for_execute_query_test():
    """Sets up a simple SQLite database with a users table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        age INTEGER 
    )
    ''')
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        users_data = [
            ('Execute Alice', 'execute.alice@example.com', 30),
            ('Execute Bob', 'execute.bob@example.com', 22),
            ('Execute Charlie', 'execute.charlie@example.com', 35),
            ('Execute David', 'execute.david@example.com', 20),
            ('Execute Eve', 'execute.eve@example.com', 28)
        ]
        cursor.executemany("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", users_data)
        conn.commit()
        print("DB Setup: Sample users (with age) inserted for ExecuteQuery test.")
    else:
        print("DB Setup: Database already contains data (ensure 'age' column exists).")
    conn.close()

class ExecuteQuery:
    """
    A class-based context manager that handles connecting to an SQLite database,
    executing a given SQL query with parameters, and making the results available.
    The connection is automatically closed upon exiting the 'with' block.
    """
    def __init__(self, db_name, query_string, params=None):
        self.db_name = db_name
        self.query_string = query_string
        self.params = params if params is not None else ()
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """
        Called when entering the 'with' block.
        Establishes the database connection, creates a cursor,
        executes the query, and returns the cursor object
        so results can be fetched.
        """
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.connection.row_factory = sqlite3.Row
            
            self.cursor = self.connection.cursor()
            print(f"ExecuteQuery LOG: Connection to '{self.db_name}' opened.")
            print(f"ExecuteQuery LOG: Executing query: \"{self.query_string}\" with params: {self.params}")
            
            self.cursor.execute(self.query_string, self.params)
         
            return self.cursor 
        except sqlite3.Error as e:
            print(f"ExecuteQuery ERROR: Database error during __enter__: {e}")
            if self.connection:
                self.connection.close() 
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Called when exiting the 'with' block.
        Ensures the database connection is closed.
        If an exception occurred in the 'with' block, it might perform a rollback (if applicable).
        For SQLite with default autocommit behavior or simple SELECTs, explicit rollback might not be needed
        unless DML operations were part of a transaction started by the user within the `with` block.
        """
     
        
        if self.connection:
   
            try:
                self.connection.close()
                print(f"ExecuteQuery LOG: Connection to '{self.db_name}' closed.")
            except sqlite3.Error as e:
                print(f"ExecuteQuery ERROR: Error closing database connection: {e}")
        
        if exc_type:
            print(f"ExecuteQuery INFO: Exception occurred within 'with' block: {exc_type.__name__}: {exc_val}")
        
        return False 

if __name__ == "__main__":
    setup_database_for_execute_query_test()

    query_to_execute = "SELECT * FROM users WHERE age > ?"
    query_params = (25,) 

    print(f"\n--- Executing query: '{query_to_execute}' with params {query_params} ---")
    
    all_results = [] 

    try:
        with ExecuteQuery(DB_NAME, query_to_execute, query_params) as cursor:
            if cursor:
                results = cursor.fetchall() 
                
                if results:
                    print("\nQuery Results (users older than 25):")
                    for row_obj in results:
                        row_dict = dict(row_obj)
                        all_results.append(row_dict)
                        print(row_dict)
                else:
                    print("No users found matching the criteria.")
            else:
                print("Failed to get a cursor from the context manager.")
                
    except sqlite3.Error as e:
        print(f"Main ERROR: An SQLite error occurred: {e}")
    except Exception as e:
        print(f"Main ERROR: An unexpected error occurred: {e}")

    print(f"\nTotal results fetched and stored: {len(all_results)}")
    

    print("\n--- Example: Querying for users with age < 25 ---")
    query_younger = "SELECT * FROM users WHERE age < ?"
    params_younger = (25,)
    try:
        with ExecuteQuery(DB_NAME, query_younger, params_younger) as cursor:
            if cursor:
                young_users = [dict(row) for row in cursor.fetchall()]
                if young_users:
                    print("\nQuery Results (users younger than 25):")
                    for user in young_users:
                        print(user)
                else:
                    print("No users younger than 25 found.")
    except Exception as e:
        print(f"Main ERROR: {e}")
        
    print("\nScript finished.")