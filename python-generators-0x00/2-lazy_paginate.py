#!/usr/bin/python3
import mysql.connector
import os
import sys

DB_HOST = os.getenv('ALX_MYSQL_HOST', 'localhost')
DB_USER = os.getenv('ALX_MYSQL_USER', 'your_mysql_user')
DB_PASSWORD = os.getenv('ALX_MYSQL_PASSWORD', 'your_mysql_password')
DB_NAME = "ALX_prodev"

def connect_to_prodev_for_paginate():
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
    connection = None
    rows = []
    try:
        connection = connect_to_prodev_for_paginate()
        if connection:
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute(f"SELECT * FROM user_data ORDER BY user_id LIMIT {page_size} OFFSET {offset}")
            rows = cursor.fetchall()
            cursor.close()
        else:
            print("paginate_users: Failed to establish database connection.", file=sys.stderr)

    except mysql.connector.Error as err:
        print(f"paginate_users: Database error: {err}", file=sys.stderr)
    except ConnectionError as cerr:
        print(f"paginate_users: {cerr}", file=sys.stderr)
    finally:
        if connection and connection.is_connected():
            connection.close()
    return rows

def lazy_paginate(page_size):
    offset = 0
    while True:
        page_data = paginate_users(page_size=page_size, offset=offset)
        if not page_data:
            break
        yield page_data
        offset += page_size

lazy_pagination = lazy_paginate

if __name__ == '__main__':
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