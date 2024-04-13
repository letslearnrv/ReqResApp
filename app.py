from flask import Flask, render_template, request, jsonify
import requests
import re

app = Flask(__name__)


# Validation function for email format
def validate_email(email):
    pattern = r'^[\w\-\.]+@([\w-]+\.)+[\w-]{2,}$'
    return re.match(pattern, email)


# Validation function for positive user ID
def validate_user_id(user_id):
    return user_id > 0


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<int:user_id>')
def get_user(user_id):
    if not validate_user_id(user_id):
        return jsonify({'error': 'Invalid user ID'}), 400

    api_url = f'http://localhost:57167/api/users/{user_id}'  # Updated API URL
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if 'email' not in data['data'] or not validate_email(data['data']['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        return jsonify(data['data'])
    else:
        return jsonify({'error': 'User not found'}), 404


if __name__ == "__main__":
    app.config["CACHE_TYPE"] = "null"
    app.run(debug=True)
