"""
Script to set up MySQL database, create a table, and populate it from a CSV.
"""
import mysql.connector
import csv
import os
from uuid import uuid4 


DB_HOST = os.getenv('ALX_MYSQL_HOST', 'localhost')
DB_USER = os.getenv('ALX_MYSQL_USER', 'your_mysql_user') 
DB_PASSWORD = os.getenv('ALX_MYSQL_PASSWORD', 'your_mysql_password') 
DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"

def connect_db():
    """Connects to the MySQL database server."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("Successfully connected to MySQL server.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL server: {err}")
        return None

def create_database(connection):
    """Creates the database ALX_prodev if it does not exist."""
    if not connection:
        return
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database '{DB_NAME}' checked/created successfully.")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating database {DB_NAME}: {err}")

def connect_to_prodev():
    """Connects to the ALX_prodev database in MySQL."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database {DB_NAME}: {err}")
        return None

def create_table(connection):
    """Creates a table user_data if it does not exist with the required fields."""
    if not connection:
        return
    try:
        cursor = connection.cursor()
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age INT NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
      
        cursor.execute(create_table_query)
        print(f"Table '{TABLE_NAME}' created successfully (or already exists).") 
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating table {TABLE_NAME}: {err}")

def insert_data(connection, csv_file_path):
    """Inserts data from the CSV file into the database if it does not exist."""
    if not connection:
        return
    
    cursor = connection.cursor()
    
    cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
    if cursor.fetchone()[0] > 0:
        print(f"Table '{TABLE_NAME}' seems to already contain data. Skipping insertion.")
        cursor.close()
        return

    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            insert_query = f"""
            INSERT INTO {TABLE_NAME} (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE name=VALUES(name), email=VALUES(email), age=VALUES(age);
            """
           
            data_to_insert = []
            for row in reader:
                user_id = row.get('user_id', str(uuid4())) 
                name = row.get('name')
                email = row.get('email')
                try:
                    age = int(row.get('age')) 
                except (ValueError, TypeError):
                    print(f"Skipping row due to invalid age: {row}")
                    continue

                if not all([user_id, name, email]):
                    print(f"Skipping row due to missing data: {row}")
                    continue
                
                data_to_insert.append((user_id, name, email, age))

            if data_to_insert:
                cursor.executemany(insert_query, data_to_insert)
                connection.commit()
                print(f"Data inserted successfully into '{TABLE_NAME}'.")
            else:
                print("No valid data found in CSV to insert.")

    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file_path}' not found.")
    except mysql.connector.Error as err:
        print(f"Error inserting data into {TABLE_NAME}: {err}")
    except Exception as e:
        print(f"An unexpected error occurred during data insertion: {e}")
    finally:
        if cursor:
            cursor.close()

if __name__ == '__main__':
  
    print("Running seed.py directly for testing...")
    
  
    conn_server = connect_db()
    
    if conn_server:
      
        create_database(conn_server)
        conn_server.close()

        conn_db = connect_to_prodev()
        if conn_db:
           
            create_table(conn_db)
          
            csv_path = 'user_data.csv'
            if not os.path.exists(csv_path):
                print(f"Creating dummy '{csv_path}' for testing seed.py...")
                with open(csv_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['user_id', 'name', 'email', 'age'])
                    writer.writerow([str(uuid4()), 'Test User 1', 'test1@example.com', 30])
                    writer.writerow([str(uuid4()), 'Test User 2', 'test2@example.com', 25])
            
            insert_data(conn_db, csv_path)
            
            cursor = conn_db.cursor()
            cursor.execute(f"SELECT * FROM {TABLE_NAME} LIMIT 2;")
            print("\nSample data from table:")
            for row in cursor.fetchall():
                print(row)
            cursor.close()
            conn_db.close()
        else:
            print("Failed to connect to the database for table creation and data insertion.")
    else:
        print("Failed to connect to MySQL server.")