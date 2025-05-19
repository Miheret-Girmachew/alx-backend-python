"""
Module for lazy pagination of user data from the database.
"""
import mysql.connector
import os

DB_HOST = os.getenv('ALX_MYSQL_HOST', 'localhost')
DB_USER = os.getenv('ALX_MYSQL_USER', 'your_mysql_user') 
DB_PASSWORD = os.getenv('ALX_MYSQL_PASSWORD', 'your_mysql_password') 
DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"

def connect_to_prodev_for_paginate():
    """Connects to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
     
        raise ConnectionError(f"Failed to connect to database {DB_NAME}: {err}") from err

def paginate_users(page_size, offset):
    """
    Fetches a specific page of users from the user_data table.
    This function is provided as per the task instructions.
    """
    connection = None
    rows = [] 
    try:
        connection = connect_to_prodev_for_paginate()
        if connection:
            cursor = connection.cursor(dictionary=True)
            query = f"SELECT * FROM {TABLE_NAME} ORDER BY user_id LIMIT {page_size} OFFSET {offset}"
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
        else:
         
            print("paginate_users: Failed to establish database connection.", file=sys.stderr if 'sys' in globals() else None)

    except mysql.connector.Error as err:
        print(f"paginate_users: Database error: {err}", file=sys.stderr if 'sys' in globals() else None)
    except ConnectionError as cerr: 
        print(f"paginate_users: {cerr}", file=sys.stderr if 'sys' in globals() else None)
    finally:
        if connection and connection.is_connected():
            connection.close()
    return rows

def lazy_paginate(page_size):
    """
    A generator function that implements lazy pagination.
    It fetches the next page of users only when needed, starting at offset 0.
    Uses only one loop.
    """
    offset = 0
    while True:
        page_data = paginate_users(page_size=page_size, offset=offset)
        if not page_data:
            break         
        
        yield page_data  
       
        offset += page_size 

lazy_pagination = lazy_paginate

if __name__ == '__main__':
    import sys 
    print("Testing lazy_paginate directly (fetching 2 pages of 3 users each):")
    
    page_count = 0
    for page in lazy_pagination(page_size=3):
        page_count += 1
        print(f"\n--- Page {page_count} ---")
        if not page: 
            print("Empty page received, stopping.")
            break
        for user in page:
            print(user)
        if page_count >= 2:
            break
    
