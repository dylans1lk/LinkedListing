from flask import Flask, jsonify
import json

app = Flask(__name__)

# Function to load items from test.json
def load_items():
    with open('test.json') as f:
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

if __name__ == '__main__':
    app.run(debug=True)
