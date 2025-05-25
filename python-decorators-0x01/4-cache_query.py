#!/usr/bin/python3
"""
Module to demonstrate a decorator for caching database query results.
"""
import time
import sqlite3
import functools
import hashlib

DB_NAME = 'users.db' 
query_cache = {} 

def setup_database_for_cache_test():
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
            ('Cache User Foo', 'cache.foo@example.com'),
            ('Cache User Bar', 'cache.bar@example.com'),
            ('Cache User Baz', 'cache.baz@example.com')
        ]
        cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", users_data)
        conn.commit()
        print("DB Setup: Sample users inserted for cache test.")
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

def cache_query(func):
    """
    A decorator that caches the results of a database query function.
    The cache key is based on the SQL query string (and potentially other arguments).
    It assumes the decorated function receives a database connection as its first argument
    and the SQL query string as its second positional argument or as a keyword argument 'query'.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query_string = None
        
        if args: 
            query_string = args[0] 
        elif 'query' in kwargs: 
            query_string = kwargs['query']
        
        if query_string is None:
            print("LOG (cache_query): Could not determine query string for caching. Executing function directly.")
            return func(conn, *args, **kwargs)

        cache_key = query_string 

        if cache_key in query_cache:
            print(f"LOG (cache_query): Cache HIT for query: \"{query_string[:50]}...\"")
            return query_cache[cache_key]
        else:
            print(f"LOG (cache_query): Cache MISS for query: \"{query_string[:50]}...\" Executing and caching.")
        
            result = func(conn, *args, **kwargs) 
            query_cache[cache_key] = result 
            return result
    return wrapper

@with_db_connection 
@cache_query        
def fetch_users_with_cache(conn, query):
    """Fetches users based on the query, results may be cached."""
    print(f"Executing fetch_users_with_cache with query: \"{query[:50]}...\" (DB operation)")
    cursor = conn.cursor()
    cursor.execute(query) 
    results = cursor.fetchall()
    print("DB query executed.")
    return results

if __name__ == "__main__":
    setup_database_for_cache_test()

    print("\n--- First call to fetch_users_with_cache (should execute DB query and cache) ---")
    sql_query = "SELECT * FROM users ORDER BY name"
    users1 = fetch_users_with_cache(query=sql_query)
    if users1:
        print(f"Fetched {len(users1)} users (1st call):")
    else:
        print("No users found or error on 1st call.")

    print(f"\nCurrent cache state: {len(query_cache)} items. Keys: {list(query_cache.keys())}")

    print("\n--- Second call to fetch_users_with_cache with THE SAME query (should use cache) ---")
    users2 = fetch_users_with_cache(query=sql_query)
    if users2:
        print(f"Fetched {len(users2)} users (2nd call, from cache):")
    else:
        print("No users found or error on 2nd call (cache).")
    
    assert users1 == users2, "Results from DB and cache should be identical for the same query"
    print("Assertion: Results from DB and cache are identical for the same query.")


    print("\n--- Third call with a DIFFERENT query (should execute DB query and cache) ---")
    different_sql_query = "SELECT * FROM users WHERE email LIKE 'cache.foo%'"
    users3 = fetch_users_with_cache(query=different_sql_query)
    if users3:
        print(f"Fetched {len(users3)} users (3rd call, new query):")
    else:
        print("No users found or error on 3rd call (new query).")

    print(f"\nCurrent cache state: {len(query_cache)} items. Keys: {list(query_cache.keys())}")

    print(f"\nName of decorated function: {fetch_users_with_cache.__name__}")
