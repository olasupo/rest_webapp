from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS
from db_connector import users_table_exists, create_users_table, user_exists, create_user, delete_user, update_user, search_actions
import signal

app = Flask(__name__)
CORS(app)

# Check if 'users' table exists, and create it if not
if not users_table_exists():
    create_users_table()

@app.route('/stop_server')
def stop_server():
    os.kill(os.getpid(), signal.CTRL_C_EVENT)
    return 'Server Stopped'

# Route for handling GET requests
@app.route('/users/<user_id>', methods=['GET'])
def get_user_data(user_id):
    print(f"Received GET request for user_id: {user_id}")
    try:
        user_id = int(user_id)

        if user_exists(user_id):
            print("Search User Exists")
            get_data = search_actions(user_id)
            print(get_data)
            user_data = {'user_id': get_data[0], 'user_name': get_data[1], 'creation_date': get_data[2]}
            print(f"We found the user with id {user_data['user_id']} and name {user_data['user_name']}. His record was created on {user_data['creation_date']}")
            return jsonify(user_data), 200
        else:
            print("User does not exist")
            return jsonify({'error': 'User not found', 'status': 'failed'}), 404

    except Exception as e:
        return jsonify({'error': str(e), 'status': 'failed'}), 500

# Route for handling POST requests
@app.route('/users/<user_id>', methods=['POST'])
def user_forms(user_id):
    print(f"Connection TO NEW CODE detected from webapp.py")

    try:
        creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user_id = int(user_id)
        data = request.get_json()
        print(f"Data is: {data}")
        action = data.get('action')
        print(f"Received user_id: {user_id} and Action: {action}")

        if action == 'search user':
            if user_exists(user_id):
                get_data = search_actions(user_id)
                user_data = {'user_id': get_data[0], 'user_name': get_data[1], 'creation_date': get_data[2]}
                return jsonify([user_data]), 200
            else:
                return jsonify({'error': 'User not found', 'status': 'failed'}), 404

        elif action == 'create user':
            # Handle create logic for POST requests
            data = request.get_json()
            inp_user_name = data.get('user_name')

            if user_exists(user_id):
                return jsonify({'Error': 'User ID already exists', 'Status': 'failed'}), 500

            if not create_user(user_id, inp_user_name, creation_date):
                return jsonify({'error': 'Failed to save user to database', 'status': 'failed'}), 500
            return jsonify({'user id': user_id, 'user name': inp_user_name, 'creation_date': creation_date,
                            'status': 'saved'}), 200

        elif action == 'update user':
            # Handle update logic for POST requests
            if user_exists(user_id):
                new_user_name = data.get('user_name')
                if update_user(user_id, new_user_name, creation_date):
                    return jsonify({'status': 'ok', 'user_updated': new_user_name}), 200
                else:
                    return jsonify({'status': 'error', 'reason': 'unknown error'}), 500
            else:
                return jsonify({'status': 'error', 'reason': 'no such id'}), 500

        elif action == 'delete user':
            # Handle delete logic for POST requests
            if user_exists(user_id):
                if delete_user(user_id):
                    return jsonify({'status': 'ok', 'user_deleted': user_id}), 200
                else:
                    return jsonify({'status': 'error', 'reason': 'unknown error'}), 500
            else:
                return jsonify({'status': 'error', 'reason': 'no such id'}), 500

        else:
            return jsonify({'error': 'Invalid action', 'status': 'failed'}), 400

    except Exception as e:
        return jsonify({'error': str(e), 'status': 'failed'}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5001)
