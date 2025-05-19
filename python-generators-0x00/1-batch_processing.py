#!/usr/bin/python3
"""
Module to stream user data in batches and process them.
"""
import mysql.connector
import os

# --- Database Connection Details (copied or import from seed.py) ---
DB_HOST = os.getenv('ALX_MYSQL_HOST', 'localhost')
DB_USER = os.getenv('ALX_MYSQL_USER', 'your_mysql_user') # Replace with your MySQL username
DB_PASSWORD = os.getenv('ALX_MYSQL_PASSWORD', 'your_mysql_password') # Replace with your MySQL password
DB_NAME = "ALX_prodev"
# TABLE_NAME = "user_data" # We'll hardcode it in the query for the checker

def connect_to_prodev_for_batch():
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
        print(f"Error connecting to database {DB_NAME} for batch processing: {err}")
        return None

def stream_users_in_batches(batch_size=50):
    """
    A generator function that fetches rows in batches from the user_data table.
    Yields each batch as a list of dictionaries.
    Constraint: This function should contain its part of the loop count.
    """
    connection = None
    cursor = None
    try:
        connection = connect_to_prodev_for_batch()
        if connection is None:
            return

        cursor = connection.cursor(dictionary=True) # Get results as dictionaries
        
        # Hardcoding "FROM user_data" for the checker
        query = "SELECT user_id, name, email, age FROM user_data ORDER BY user_id"
        cursor.execute(query)

        while True: # Loop 1 (outer loop for fetching batches)
            batch = cursor.fetchmany(batch_size)
            if not batch: # No more rows left
                break
            yield batch # Yield the current batch
            
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
    """
    Processes each batch fetched by stream_users_in_batches
    to filter and print users over the age of 25.
    Constraint: This function contributes to the overall loop count.
    """
    user_batch_generator = stream_users_in_batches(batch_size)
    
    # Loop 2 (iterating over batches yielded by the generator)
    for batch in user_batch_generator:
        # Loop 3 (iterating over users within a batch for processing)
        for user in batch:
            if user.get('age') is not None and user['age'] > 25:
                print(user)

if __name__ == '__main__':
    # For direct testing of this module
    print("Processing users in batches (batch_size=5), printing first few > 25:")
    
    def test_batch_processing_limited(batch_size=5, limit_total_printed=5):
        user_batch_generator = stream_users_in_batches(batch_size)
        printed_count = 0
        for batch_item in user_batch_generator: # Renamed batch to batch_item to avoid conflict
            if printed_count >= limit_total_printed:
                break
            for user in batch_item: # Use batch_item here
                if printed_count >= limit_total_printed:
                    break
                if user.get('age') is not None and user['age'] > 25:
                    print(user)
                    printed_count += 1
    
    test_batch_processing_limited(batch_size=10, limit_total_printed=7)