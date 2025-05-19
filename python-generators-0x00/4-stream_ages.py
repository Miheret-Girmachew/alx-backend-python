#!/usr/bin/python3
import mysql.connector
import os
import sys

DB_HOST = os.getenv('ALX_MYSQL_HOST', 'localhost')
DB_USER = os.getenv('ALX_MYSQL_USER', 'your_mysql_user')
DB_PASSWORD = os.getenv('ALX_MYSQL_PASSWORD', 'your_mysql_password')
DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"

def connect_to_prodev_for_ages():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        raise ConnectionError(f"Failed to connect to database {DB_NAME} for streaming ages: {err}") from err

def stream_user_ages():
    connection = None
    cursor = None
    try:
        connection = connect_to_prodev_for_ages()
        cursor = connection.cursor(dictionary=True, buffered=False)
        
        query = f"SELECT age FROM {TABLE_NAME}"
        cursor.execute(query)

        for row in cursor:
            if row.get('age') is not None:
                try:
                    yield int(row['age'])
                except (ValueError, TypeError):
                    pass
            
    except mysql.connector.Error as err:
        print(f"Database error during age streaming: {err}", file=sys.stderr)
    except ConnectionError as cerr:
        print(f"Connection error during age streaming: {cerr}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred during age streaming: {e}", file=sys.stderr)
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def calculate_average_age():
    age_generator = stream_user_ages()
    
    total_age = 0
    count = 0
    
    for age in age_generator:
        total_age += age
        count += 1
        
    if count > 0:
        average_age = total_age / count
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("Average age of users: No user data found or no valid ages to calculate average.")

if __name__ == '__main__':
    calculate_average_age()