import pymysql
from time import sleep
from datetime import datetime

# MySQL database connection details
DB_HOST = '192.168.99.102'
DB_USER = 'user'
DB_PASSWORD = 'password'
DB_NAME = 'mydb'
DB_PORT = 3306

# Function to get actions for a specific user from the 'users' table
def get_actions(user_id):
    connection = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    connection.autocommit(True)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        return result

# Function to search actions for a specific user from the 'users' table
def search_actions(user_id):
    connection = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    connection.autocommit(True)
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        print(result)
        return result

# Function to check if the 'users' table exists in the database
def users_table_exists():
    print("Database connection pending for 10 seconds to ensure dmysql is fully up")
    sleep(10)
    connection = None
    try:
        connection = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        print("Connection to DB established")
        connection.autocommit(True)
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES LIKE 'users'")
            result = cursor.fetchone()
            return result is not None
    except pymysql.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return False
    finally:
        if connection:
            connection.close()

# Function to create the 'users' table in the database if it doesn't exist
def create_users_table():
    connection = None
    print("About to Create New Table")
    try:
        print("Creating New Table")
        connection = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        with connection.cursor() as cursor:
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS users (user_id INT PRIMARY KEY, user_name VARCHAR(50) NOT NULL, creation_date VARCHAR(50) NOT NULL)"
            )
        connection.commit()
        return True
    except pymysql.Error as e:
        print(f"Error: {e}")
        return False
    finally:
        if connection:
            connection.close()

# Function to check if a user with the given user_id exists in the 'users' table
def user_exists(user_id):
    print(f"I got a request to check if user {user_id} exists")
    connection = None
    try:
        connection = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        connection.autocommit(True)
        print("Searching for user....")
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            result = cursor.fetchone()
            print(result)
            return result is not None
    except pymysql.Error as e:
        print(f"Error: {e}")
        return False
    finally:
        if connection:
            connection.close()

# Function to create a new user in the 'users' table
def create_user(user_id, user_name, creation_date):
    connection = None
    try:
        connection = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        print("Creating New User....")
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO users (user_id, user_name, creation_date) VALUES (%s, %s, %s)",
                           (user_id, user_name, creation_date))
        connection.commit()
        return True
    except pymysql.Error as e:
        print(f"Error: {e}")
        return False
    finally:
        if connection:
            connection.close()

# Function to delete a user from the 'users' table
def delete_user(user_id):
    connection = None
    try:
        connection = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        print("Deleting User...")
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        connection.commit()
        return True
    except pymysql.Error as e:
        print(f"Error: {e}")
        return False
    finally:
        if connection:
            connection.close()

# Function to update user information in the 'users' table
def update_user(user_id, new_user_name, creation_date):
    connection = None
    try:
        connection = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        print("Updating User...")
        with connection.cursor() as cursor:
            cursor.execute("UPDATE users SET user_name = %s, creation_date = %s WHERE user_id = %s", (new_user_name, creation_date, user_id))
        connection.commit()
        return True
    except pymysql.Error as e:
        print(f"Error: {e}")
        return False
    finally:
        if connection:
            connection.close()
