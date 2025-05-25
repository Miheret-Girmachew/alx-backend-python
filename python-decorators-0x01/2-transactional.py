#!/usr/bin/python3
"""
Module to demonstrate decorators for handling database connections and transactions.
"""
import sqlite3
import functools

DB_NAME = 'users.db' 
def setup_database_for_transaction_test():
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
            ('Alice Wonderland', 'alice@example.com'),
            ('Bob The Builder', 'bob@example.com')
        ]
        cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", users_data)
        conn.commit()
        print("DB Setup: Sample users inserted for transaction test.")
    conn.close()

def with_db_connection(func):
    """
    A decorator that automatically opens an SQLite database connection,
    passes the connection object as the first argument to the decorated function,
    and ensures the connection is closed afterwards, even if errors occur.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = None
        result = None
        try:
            conn = sqlite3.connect(DB_NAME)
            result = func(conn, *args, **kwargs)
        except sqlite3.Error as e:
            print(f"ERROR (with_db_connection): Database error in '{func.__name__}': {e}")
        except Exception as e:
            print(f"ERROR (with_db_connection): An unexpected error in '{func.__name__}': {e}")
        finally:
            if conn:
                conn.close()
        return result
    return wrapper

def transactional(func):
    """
    A decorator that wraps the decorated function's database operations
    within a transaction. It commits if the function completes successfully,
    and rolls back if any exception occurs within the function.
    Assumes the decorated function receives a database connection object as its first argument.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs): 
        if conn is None:
            print("ERROR (transactional): Database connection is None. Cannot start transaction.")
        
            return func(conn, *args, **kwargs)

        try:
            print(f"LOG (transactional): Beginning transaction for '{func.__name__}'.")
          
            result = func(conn, *args, **kwargs)
            
            conn.commit() 
            print(f"LOG (transactional): Transaction committed for '{func.__name__}'.")
            return result
        except Exception as e:
            print(f"ERROR (transactional): Exception in '{func.__name__}': {e}. Rolling back transaction.")
            if conn:
                conn.rollback() 
            raise 
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """Updates a user's email. Operations are transactional."""
    print(f"Executing update_user_email for user_id: {user_id} to new_email: {new_email}")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    print(f"Email for user_id {user_id} prepared for update in transaction.")

@with_db_connection
def get_user_details(conn, user_id):
    """Fetches user details by ID."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    data = cursor.fetchone()
    if data:
        cols = [desc[0] for desc in cursor.description]
        return dict(zip(cols, data))
    return None

if __name__ == "__main__":
    setup_database_for_transaction_test()

    USER_ID_TO_TEST = 1 

    print(f"\n--- Initial state of user {USER_ID_TO_TEST} ---")
    user_before = get_user_details(user_id=USER_ID_TO_TEST)
    print(user_before)

    print(f"\n--- Attempting successful email update for user {USER_ID_TO_TEST} ---")
    try:
        update_user_email(user_id=USER_ID_TO_TEST, new_email='Crawford_Cartwright@hotmail.com')
    except Exception as e:
        print(f"Main: Caught exception during successful update attempt: {e}")
    
    print(f"\n--- State of user {USER_ID_TO_TEST} after successful update attempt ---")
    user_after_success = get_user_details(user_id=USER_ID_TO_TEST)
    print(user_after_success)


    print(f"\n--- Attempting email update that will cause an error for user {USER_ID_TO_TEST} ---")
    original_email_for_rollback_test = user_after_success.get('email') if user_after_success else 'unknown@example.com'
    
    try:
       
        
        print(f"Simulating an update to 'error@example.com' which should trigger a rollback if error occurs in function.")
       
        if not get_user_details(user_id=2):
            add_user_conn = sqlite3.connect(DB_NAME)
            add_user_conn.execute("INSERT INTO users (id, name, email) VALUES (?, ?, ?)", (2, 'User Two', 'user.two@example.com'))
            add_user_conn.commit()
            add_user_conn.close()
            print("Added user 2 for unique constraint test.")

        print(f"Attempting to update user {USER_ID_TO_TEST} email to an existing email 'user.two@example.com' to cause IntegrityError...")
        try:
            update_user_email(user_id=USER_ID_TO_TEST, new_email='user.two@example.com')
        except sqlite3.IntegrityError:
            print("Main: Caught IntegrityError as expected, transaction should have rolled back.")
        except Exception as e:
            print(f"Main: Caught unexpected exception during conflict update attempt: {e}")

    except Exception as e:
        print(f"Main: Caught exception during rollback test setup: {e}")

    print(f"\n--- State of user {USER_ID_TO_TEST} after conflicting update attempt (should be rolled back) ---")
    user_after_rollback_attempt = get_user_details(user_id=USER_ID_TO_TEST)
    print(user_after_rollback_attempt)
    if user_after_rollback_attempt and user_after_rollback_attempt.get('email') == original_email_for_rollback_test:
        print("Rollback appears successful: Email reverted or remained unchanged.")
    else:
        print("Rollback test inconclusive or email changed unexpectedly.")