#!/usr/bin/python3
"""
Module to demonstrate a decorator for retrying database operations on failure.
"""
import time
import sqlite3
import functools

DB_NAME = 'users.db' 

_db_should_fail_count = 0 

def setup_database_for_retry_test():
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
            ('Retry User A', 'retry.a@example.com'),
            ('Retry User B', 'retry.b@example.com')
        ]
        cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", users_data)
        conn.commit()
        print("DB Setup: Sample users inserted for retry test.")
    conn.close()

def with_db_connection(func):
    """
    A decorator that automatically opens an SQLite database connection,
    passes the connection object as the first argument to the decorated function,
    and ensures the connection is closed afterwards, even if errors occur.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        global _db_should_fail_count
        conn = None
        result = None
        
        if _db_should_fail_count > 0:
            _db_should_fail_count -= 1
            print(f"LOG (with_db_connection): Simulating connection failure. Attempts remaining: {_db_should_fail_count +1 }")
            raise sqlite3.OperationalError("Simulated temporary connection unavailable")

        try:
            conn = sqlite3.connect(DB_NAME)
            result = func(conn, *args, **kwargs)
        except sqlite3.Error as e:
            print(f"ERROR (with_db_connection): Database error in '{func.__name__}': {e}")
            raise 
        except Exception as e:
            print(f"ERROR (with_db_connection): An unexpected error in '{func.__name__}': {e}")
            raise
        finally:
            if conn:
                conn.close()
        return result
    return wrapper

def retry_on_failure(retries=3, delay=1, allowed_exceptions=(sqlite3.Error,)):
    """
    A decorator that retries the execution of the decorated function
    if it raises one of the `allowed_exceptions`.

    Args:
        retries (int): The maximum number of times to retry the function.
        delay (int): The number of seconds to wait between retries.
        allowed_exceptions (tuple): A tuple of exception types that should trigger a retry.
                                    Defaults to (sqlite3.Error,).
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            last_exception = None
            while attempts <= retries:
                try:
                    if attempts > 0: 
                        print(f"LOG (retry_on_failure): Retrying '{func.__name__}' (Attempt {attempts}/{retries})...")
                    return func(*args, **kwargs)
                except allowed_exceptions as e:
                    last_exception = e
                    attempts += 1
                    if attempts > retries:
                        print(f"ERROR (retry_on_failure): '{func.__name__}' failed after {retries} retries. Last error: {e}")
                        raise 
                    
                    print(f"LOG (retry_on_failure): '{func.__name__}' failed with {type(e).__name__}: {e}. Waiting {delay}s before retrying ({attempts}/{retries}).")
                    time.sleep(delay)
                except Exception as e: 
                    print(f"ERROR (retry_on_failure): '{func.__name__}' failed with an unexpected error: {e}")
                    raise 
            if last_exception:
                raise last_exception 
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1) 
def fetch_users_with_retry(conn):
    """Fetches all users. Designed to be retried on failure."""
    print(f"Executing fetch_users_with_retry (connection: {conn is not None})...")
   
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print("Successfully fetched users.")
    return results

if __name__ == "__main__":
    setup_database_for_retry_test()

    print("\n--- Attempting to fetch users with potential retries ---")
    
    print("\nTest 1: Simulating 2 initial connection failures...")
    _db_should_fail_count = 2 
    try:
        users = fetch_users_with_retry()
        if users:
            print("\nFetched users after retries:")
            for user_row in users[:2]: 
                print(user_row)
        else:
            print("Failed to fetch users even after retries or no users found.")
    except Exception as e:
        print(f"Main: Test 1最終的に失敗しました: {e}")

    _db_should_fail_count = 0 
    print("-" * 40)

    print("\nTest 2: Fetching users without simulated failures...")
    try:
        users_no_fail = fetch_users_with_retry()
        if users_no_fail:
            print("\nFetched users successfully on first attempt:")
            for user_row in users_no_fail[:2]:
                print(user_row)
        else:
            print("No users found (or an unexpected issue).")
    except Exception as e:
        print(f"Main: Test 2 failed unexpectedly: {e}")

    
    print(f"\nName of ultimate decorated function: {fetch_users_with_retry.__name__}")
