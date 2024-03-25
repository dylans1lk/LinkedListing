from flask import Flask, jsonify, request
import firebase_config
from firebase_admin import auth, credentials
import json

app = Flask(__name__)

# Function to load items from test.json
def load_items():
    with open('backend/test.json') as f:
        return json.load(f)["items"]

@app.route('/')
def hello_world():
    return jsonify({'message': 'Hello, World!'})

@app.route('/items', methods=['GET'])
def get_items():
    items = load_items()
    return jsonify({'items': items})

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    items = load_items()
    item = next((item for item in items if item['id'] == item_id), None)
    if item:
        return jsonify(item)
    else:
        return jsonify({'message': 'Item not found'}), 404
    
"""
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'message': 'Missing email or password'}), 400
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return jsonify({'uid': user.uid, 'email': email}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'message': 'Missing email or password'}), 400
    # Firebase Authentication does not directly support login in server-side code
    # You would typically use Firebase SDK on client-side to handle login
    # This endpoint could be used to verify a token obtained after login on client-side
    return jsonify({'message': 'See comments in source code for login handling.'}), 200
"""

if __name__ == '__main__':
    app.run(debug=True)
