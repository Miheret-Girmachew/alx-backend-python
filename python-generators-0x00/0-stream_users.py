#!/usr/bin/python3
import mysql.connector
import os

DB_HOST = os.getenv('ALX_MYSQL_HOST', 'localhost')
DB_USER = os.getenv('ALX_MYSQL_USER', 'your_mysql_user')
DB_PASSWORD = os.getenv('ALX_MYSQL_PASSWORD', 'your_mysql_password')
DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"

def connect_to_prodev_for_stream():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database {DB_NAME} for streaming: {err}")
        return None

def stream_users():
    connection = None
    cursor = None
    try:
        connection = connect_to_prodev_for_stream()
        if connection is None:
            return

        cursor = connection.cursor(dictionary=True, buffered=False)
        
        query = f"SELECT user_id, name, email, age FROM {TABLE_NAME}"
        cursor.execute(query)

        for row in cursor:
            yield row
            
    except mysql.connector.Error as err:
        print(f"Database error during streaming: {err}")
    except Exception as e:
        print(f"An unexpected error occurred during streaming: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

if __name__ == '__main__':
    from itertools import islice
    print("Streaming first 3 users directly from 0-stream_users.py for testing:")
    user_generator = stream_users()
    for user_data in islice(user_generator, 3):
        print(user_data)