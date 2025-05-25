#!/usr/bin/python3
"""
Module to demonstrate a decorator for automatically handling database connections.
"""
import sqlite3
import functools

DB_NAME = 'users.db' # Assuming the database from the previous task

# --- Database Setup (can be reused from 0-log_queries.py or simplified for this task) ---
def setup_database_for_connection_test():
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
    # Insert a sample user if table is empty, for get_user_by_id to find something
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ('Test User One', 'test1@example.com'))
        conn.commit()
        print("DB Setup: Sample user inserted for connection test.")
    conn.close()

# --- Decorator to handle database connections ---
def with_db_connection(func):
    """
    A decorator that automatically opens an SQLite database connection,
    passes the connection object as the first argument to the decorated function,
    and ensures the connection is closed afterwards, even if errors occur.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None  # Initialize conn to None
        result = None
        try:
            # Connect to the database
            conn = sqlite3.connect(DB_NAME)
            print(f"LOG: Connection to '{DB_NAME}' opened by decorator for '{func.__name__}'.")
            
            # Call the original function, passing the connection as the first argument
            # The decorated function expects 'conn' as its first argument.
            # We prepend it to the existing *args.
            result = func(conn, *args, **kwargs)
            
        except sqlite3.Error as e:
            print(f"ERROR: Database error in '{func.__name__}': {e}")
            # Depending on requirements, you might re-raise the exception or handle it
        except Exception as e:
            print(f"ERROR: An unexpected error occurred in '{func.__name__}': {e}")
        finally:
            if conn:
                conn.close()
                print(f"LOG: Connection to '{DB_NAME}' closed by decorator for '{func.__name__}'.")
        return result # Return the result from the original function call
    return wrapper

# --- Decorated function ---
@with_db_connection
def get_user_by_id(conn, user_id): # 'conn' is now passed by the decorator
    """Fetches a user by their ID using the provided database connection."""
    print(f"Executing get_user_by_id with user_id: {user_id}")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone() # cursor.fetchone() returns a tuple or None
    # To match expected dictionary-like output for consistency with previous task,
    # we can convert the tuple to a dict if row_factory was not set.
    if user_data:
        # Assuming columns are id, name, email in that order
        # A more robust way is to set conn.row_factory = sqlite3.Row
        # Or get column names from cursor.description
        column_names = [description[0] for description in cursor.description]
        return dict(zip(column_names, user_data))
    return None


@with_db_connection
def add_another_user(conn, name, email): # 'conn' is passed by the decorator
    """Adds another user to the database."""
    print(f"Executing add_another_user for: {name}")
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        print(f"User '{name}' added successfully.")
        return cursor.lastrowid # Return the ID of the newly inserted row
    except sqlite3.Error as e:
        print(f"ERROR: Could not add user '{name}': {e}")
        return None

# --- Main execution block (for testing) ---
if __name__ == "__main__":
    setup_database_for_connection_test() # Ensure DB and table exist with at least one user

    print("\n--- Fetching user by ID (decorator handles connection) ---")
    user = get_user_by_id(user_id=1) # We pass user_id, decorator handles conn
    if user:
        print(f"Fetched user: {user}")
    else:
        print("User with ID 1 not found.")

    print("\n--- Fetching non-existent user ---")
    non_existent_user = get_user_by_id(user_id=999)
    if non_existent_user:
        print(f"Fetched user: {non_existent_user}")
    else:
        print("User with ID 999 not found.")

    print("\n--- Adding a new user (decorator handles connection) ---")
    new_user_id = add_another_user("Bob The Tester", "bob.tester@example.com")
    if new_user_id:
        print(f"New user Bob added with ID: {new_user_id}")
        # Verify Bob
        bob = get_user_by_id(user_id=new_user_id)
        if bob:
            print(f"Verified Bob: {bob}")

    # Demonstrating metadata preservation
    print(f"\nName of decorated function: {get_user_by_id.__name__}")
    print(f"Docstring of decorated function: {get_user_by_id.__doc__}")