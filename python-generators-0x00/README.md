# Python Generators - Task 0: Database Seeding

## Project Objective
This initial task focuses on setting up a MySQL database, creating a specific table schema, and populating it with data from a CSV file. This serves as the foundational data source for subsequent tasks that will explore Python generators.

## Learning Objectives for this Task
- Understand how to connect to a MySQL database server using Python.
- Learn to create databases and tables programmatically.
- Practice reading data from a CSV file.
- Implement data insertion into a MySQL table.
- Follow a defined Python module structure with specific function prototypes.

## Files
- **`seed.py`**: The Python script containing functions to:
    - Connect to the MySQL server (`connect_db`).
    - Create the `ALX_prodev` database (`create_database`).
    - Connect to the `ALX_prodev` database (`connect_to_prodev`).
    - Create the `user_data` table with fields: `user_id` (VARCHAR(36), PK), `name` (VARCHAR), `email` (VARCHAR), `age` (INT). (`create_table`).
    - Insert data from a CSV file (`user_data.csv`) into the `user_data` table (`insert_data`).
- **`0-main.py`**: The main script provided to test the functionality of `seed.py`.
- **`user_data.csv`**: A CSV file containing sample user data to be seeded into the database. (You will need to create or obtain this file).
- **`README.md`**: This file.

## Requirements
- Python 3.x
- `mysql-connector-python` library (`pip install mysql-connector-python`)
- A running MySQL server instance.
- `user_data.csv` file with columns: `user_id,name,email,age`

## Setup and Execution

1.  **MySQL Server:** Ensure your MySQL server is running.
2.  **Credentials:**
    Update the `DB_USER` and `DB_PASSWORD` variables in `seed.py` with your MySQL credentials, or set the environment variables `ALX_MYSQL_USER` and `ALX_MYSQL_PASSWORD`.
    ```python
    DB_USER = os.getenv('ALX_MYSQL_USER', 'your_actual_mysql_user')
    DB_PASSWORD = os.getenv('ALX_MYSQL_PASSWORD', 'your_actual_mysql_password')
    ```
3.  **CSV File:** Place the `user_data.csv` file in the same directory as `seed.py` and `0-main.py`.
    An example `user_data.csv` might look like:
    ```csv
    user_id,name,email,age
    00234e50-34eb-4ce2-94ec-26e3fa749796,Dan Altenwerth Jr.,Molly59@gmail.com,67
    006bfede-724d-4cdd-a2a6-59700f40d0da,Glenda Wisozk,Miriam21@gmail.com,119
    ...
    ```
4.  **Run the Main Script:**
    Execute the `0-main.py` script from your terminal:
    ```bash
    ./0-main.py
    ```
    You should see output similar to the example provided in the task, indicating successful database and table creation, data presence, and a sample fetch.

## Function Prototypes in `seed.py`

-   `connect_db()`: Connects to the MySQL database server.
-   `create_database(connection)`: Creates the database `ALX_prodev` if it does not exist.
-   `connect_to_prodev()`: Connects to the `ALX_prodev` database.
-   `create_table(connection)`: Creates the `user_data` table if it does not exist with the specified fields.
-   `insert_data(connection, data_csv_filepath)`: Inserts data from the provided CSV file into the `user_data` table.

