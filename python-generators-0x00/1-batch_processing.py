#!/usr/bin/python3
import mysql.connector
import os

DB_HOST = os.getenv('ALX_MYSQL_HOST', 'localhost')
DB_USER = os.getenv('ALX_MYSQL_USER', 'your_mysql_user')
DB_PASSWORD = os.getenv('ALX_MYSQL_PASSWORD', 'your_mysql_password')
DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"

def connect_to_prodev_for_batch():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database {DB_NAME} for batch processing: {err}")
        return None

def stream_users_in_batches(batch_size=50):
    connection = None
    cursor = None
    try:
        connection = connect_to_prodev_for_batch()
        if connection is None:
            return

        cursor = connection.cursor(dictionary=True)
        
        query = f"SELECT user_id, name, email, age FROM {TABLE_NAME} ORDER BY user_id"
        cursor.execute(query)

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
            
    except mysql.connector.Error as err:
        print(f"Database error during batch streaming: {err}")
    except Exception as e:
        print(f"An unexpected error occurred during batch streaming: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def batch_processing(batch_size=50):
    user_batch_generator = stream_users_in_batches(batch_size)
    
    for batch in user_batch_generator:
        for user in batch:
            if user.get('age') is not None and user['age'] > 25:
                print(user)

if __name__ == '__main__':
    print("Processing users in batches (batch_size=5), printing first few > 25:")
    
    def test_batch_processing_limited(batch_size=5, limit_total_printed=5):
        user_batch_generator = stream_users_in_batches(batch_size)
        printed_count = 0
        for batch in user_batch_generator:
            if printed_count >= limit_total_printed:
                break
            for user in batch:
                if printed_count >= limit_total_printed:
                    break
                if user.get('age') is not None and user['age'] > 25:
                    print(user)
                    printed_count += 1
    
    test_batch_processing_limited(batch_size=10, limit_total_printed=7)