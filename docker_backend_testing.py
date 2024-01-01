import requests
import pymysql
from pymysql.cursors import DictCursor

# Base URL of your Flask app
base_url = 'http://192.168.99.100:5001/users/'

def test_post_user(user_id):
    try:
        # Data to be posted
        data = {
            'action': 'create user',
            'user_name': ran_user_name
        }

        # Make a POST request to create a new user
        response = requests.post(base_url + user_id, json=data)

        # Check if the status code is 200
        assert response.status_code == 200, f"Failed to create user because it already exists. Status code: {response.status_code}"

        print(f"User created successfully with ID: {user_id}")
    except Exception as e:
        print(f"Error: {str(e)}")

def test_get_user(user_id):
    try:
        # Make a GET request to retrieve user data
        response = requests.get(base_url + user_id)

        # Check if the status code is 200
        assert response.status_code == 200, f"Failed to get user data. Status code: {response.status_code}"

        if 'user_id' in response.json():
            user_id = response.json()['user_id']
            user_name = response.json().get('user_name', '')
            creation_date = response.json().get('creation_date', '')

            print(f"User ID: {user_id}, User name: {user_name}, Creation Date: {creation_date}")
        else:
            print("User ID not found in response.")

        print("User data retrieved successfully.")
    except Exception as e:
        print(f"Error: {str(e)}")

def test_database(user_id, expected_user_name):
    # Connect to the MySQL database using pymysql
    connection = pymysql.connect(host='192.168.99.102',
                                 user='user',
                                 password='password',
                                 database='mydb',
                                 port=3306,
                                 cursorclass=DictCursor)  # Use DictCursor to get results as dictionaries

    try:
        with connection.cursor() as cursor:
            # Assuming you have a function to fetch data from the 'users' table
            # Modify the following code based on your database schema and query
            query = f"SELECT * FROM users WHERE user_id = {user_id}"
            cursor.execute(query)
            result = cursor.fetchone()

            # Check if the fetched data matches the expected data
            if result is not None:
                if result['user_name'] != expected_user_name:
                    print(f"User Name in the database '{result['user_name']}' does not match the expected value '{expected_user_name}'")
                else:
                    print("Database testing completed successfully.")
            else:
                print(f"No data found for user_id: {user_id}")

    finally:
        connection.close()

if __name__ == '__main__':
    # Define the user_id once
    test_user_id = '100'
    ran_user_name = 'John Bravo'

    # Call test functions with the same user_id
    test_post_user(test_user_id)
    test_get_user(test_user_id)
    test_database(test_user_id, ran_user_name)
