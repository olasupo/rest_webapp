from flask import Flask, request, jsonify, render_template
import requests
import signal

app = Flask(__name__)

@app.route('/stop_server')
def stop_server():
    os.kill(os.getpid(), signal.CTRL_C_EVENT)
    return 'Server Stopped'

@app.route('/users/get_user_id/<user_id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def user_form(user_id):
    # Log the received user_id
    print(f"Received user_id: {user_id}")

    # Check if the user_id exists
    user_exists = check_user_existence(user_id)
    user_name = get_user_name(user_id)

    if user_exists:
        # Get user name if user_id exists

        print(f"We found the user with id {user_id} and name {user_name}")
        return render_template('user_form.html', user_exists=True, user_id=user_id, user_name=user_name)
    else:
        print(f"We could not find the user with id {user_id} and name {user_name}")
        # Render form with dropdown menu if user_id does not exist
        return render_template('user_form.html', user_exists=False, user_id=user_id, default_user_id=user_id)


def check_user_existence(user_id):
    # Perform an AJAX request to check if the user_id exists
    response = fetch_backend_data(f'http://127.0.0.1:5001/users/{user_id}', method='GET')
    return response.status_code == 200


def get_user_name(user_id):
    # Perform an AJAX request to get the user name based on the user_id
    response = fetch_backend_data(f'http://127.0.0.1:5001/users/{user_id}', method='GET')
    user_data = response.json()

    return user_data.get('user_name', '')


def fetch_backend_data(url, method='GET', data=None):
    # Helper function to perform HTTP requests using the requests library
    headers = {'Content-Type': 'application/json'}
    options = {
        'headers': headers,
        'data': json.dumps(data) if data is not None else None
    }

    response = requests.request(method, url, **options)

    return response


if __name__ == '__main__':
    # Run the Flask app
    app.run(host='127.0.0.1', debug=True, port=5000)
