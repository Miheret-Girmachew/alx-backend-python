#!/usr/bin/python3
"""
Module to demonstrate running multiple database queries concurrently
using asyncio and aiosqlite.
"""
import asyncio
import aiosqlite

DB_NAME = 'users.db' 

async def setup_database_for_async_test():
    """
    Sets up a simple SQLite database with a users table if it doesn't exist.
    Uses aiosqlite for consistency, though setup is often synchronous.
    """
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            age INTEGER 
        )
        ''')
        async with db.execute("SELECT COUNT(*) FROM users") as cursor:
            count_result = await cursor.fetchone()
            if count_result and count_result[0] == 0:
                users_data = [
                    ('Async Alice', 'async.alice@example.com', 30),
                    ('Async Bob', 'async.bob@example.com', 22),
                    ('Async Charlie', 'async.charlie@example.com', 45),
                    ('Async David', 'async.david@example.com', 50),
                    ('Async Eve', 'async.eve@example.com', 38)
                ]
                await db.executemany("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", users_data)
                await db.commit()
                print("DB Setup: Sample users (with age) inserted for async test.")
            else:
                print("DB Setup: Database already contains data for async test.")

async def async_fetch_users(db_name=DB_NAME):
    """
    Asynchronously fetches all users from the users table.
    Returns a list of user records (as dictionaries or tuples).
    """
    print("Starting async_fetch_users...")
    try:
        async with aiosqlite.connect(db_name) as db:
            db.row_factory = aiosqlite.Row 
            async with db.execute("SELECT * FROM users ORDER BY name") as cursor:
                results = await cursor.fetchall()
                print(f"async_fetch_users: Fetched {len(results)} users.")
                return [dict(row) for row in results]
    except Exception as e:
        print(f"Error in async_fetch_users: {e}")
        return []

async def async_fetch_older_users(db_name=DB_NAME, age_threshold=40):
    """
    Asynchronously fetches users older than a specified age_threshold.
    Returns a list of user records.
    """
    print(f"Starting async_fetch_older_users (age > {age_threshold})...")
    try:
        async with aiosqlite.connect(db_name) as db:
            db.row_factory = aiosqlite.Row 
            query = "SELECT * FROM users WHERE age > ? ORDER BY name"
            async with db.execute(query, (age_threshold,)) as cursor:
                results = await cursor.fetchall()
                print(f"async_fetch_older_users: Fetched {len(results)} users older than {age_threshold}.")
                return [dict(row) for row in results]
    except Exception as e:
        print(f"Error in async_fetch_older_users: {e}")
        return []

async def fetch_concurrently():
    """
    Uses asyncio.gather() to execute async_fetch_users and 
    async_fetch_older_users concurrently.
    """
    print("Starting concurrent fetching...")
  
    all_users_task = async_fetch_users()
    older_users_task = async_fetch_older_users(age_threshold=40) 
    
    results = await asyncio.gather(
        all_users_task,
        older_users_task
    )
    
    print("\n--- Results from concurrent fetching ---")
    
    all_users_result = results[0]
    older_users_result = results[1]
    
    print(f"\nAll Users ({len(all_users_result)} found):")
    if all_users_result:
        for user in all_users_result[:3]:
            print(user)
        if len(all_users_result) > 3:
            print("...")
    else:
        print("No users found by async_fetch_users.")

    print(f"\nUsers Older Than 40 ({len(older_users_result)} found):")
    if older_users_result:
        for user in older_users_result[:3]: 
            print(user)
        if len(older_users_result) > 3:
            print("...")
    else:
        print("No users found older than 40 by async_fetch_older_users.")

if __name__ == "__main__":
  
    asyncio.run(setup_database_for_async_test())
    
    asyncio.run(fetch_concurrently())
    
    print("\nConcurrent fetching process complete.")