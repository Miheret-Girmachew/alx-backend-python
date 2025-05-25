"""
Module to demonstrate a decorator for logging SQL queries.
"""
import sqlite3
import functools
import datetime 

DB_NAME = 'users.db'
TABLE_NAME = 'users'

def setup_database():
    """Sets up a simple SQLite database with a users table and some data."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
    ''')
    
    cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
    if cursor.fetchone()[0] == 0:
        users_data = [
            ('Alice Wonderland', 'alice@example.com'),
            ('Bob The Builder', 'bob@example.com'),
            ('Charlie Chaplin', 'charlie@example.com')
        ]
        cursor.executemany(f"INSERT INTO {TABLE_NAME} (name, email) VALUES (?, ?)", users_data)
        conn.commit()
        print("Database setup complete and sample data inserted.")
    else:
        print("Database already set up with data.")
        
    conn.close()

def log_queries(func):
    """
    A decorator that logs the SQL query string passed to the decorated function
    before the function executes it.
    It assumes the first argument to the decorated function is the SQL query.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query_to_log = None
        if args: 
            if 'query' in kwargs:
                query_to_log = kwargs['query']
            else:
                query_to_log = args[0] 
        elif 'query' in kwargs:
            query_to_log = kwargs['query']
        
        if query_to_log:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] LOG: Executing Query: \"{query_to_log}\" in function '{func.__name__}'")
        else:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] LOG: Executing function '{func.__name__}' (No query argument found to log specifically)")

        result = func(*args, **kwargs)
        return result
    return wrapper

@log_queries
def fetch_all_users(query):
    """Fetches all users from the database using the provided query."""
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(query) 
        results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        print(f"Database error in fetch_all_users: {e}")
        return []
    finally:
        if conn:
            conn.close()

@log_queries
def add_user(name, email, query_template="INSERT INTO users (name, email) VALUES (?, ?)", data=None):
    """Adds a new user to the database.
    The query is constructed or passed.
    """


    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        actual_data = data if data else (name, email)
       
        pass 
    except sqlite3.Error as e:
        print(f"Database error in add_user: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    setup_database() 
    
    print("\n--- Fetching users (decorator should log the query) ---")
    users = fetch_all_users(query="SELECT * FROM users")
    if users:
        print("Fetched users:")
        for user in users:
            print(user)
    else:
        print("No users found or error occurred.")

    print("\n--- Fetching specific user (decorator should log the query) ---")
    user_by_email_query = "SELECT * FROM users WHERE email = 'alice@example.com'"
    specific_users = fetch_all_users(user_by_email_query)
    if specific_users:
        print("Fetched specific user:")
        for user in specific_users:
            print(user)
    else:
        print("Specific user not found or error occurred.")

    print(f"\nName of decorated function: {fetch_all_users.__name__}")
    print(f"Docstring of decorated function: {fetch_all_users.__doc__}")