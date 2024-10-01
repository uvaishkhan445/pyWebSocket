from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import pymysql
import json
from datetime import date, datetime

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow CORS for all domains for testing purposes
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins

# MySQL Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': '',  # Replace with your MySQL password
    'database': 'oyly',  # Replace with your MySQL database name
}

# Function to fetch users from the database
def fetch_users():
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM contact_us"  # Adjust this query as needed
            cursor.execute(query)
            result = cursor.fetchall()
        return result
    finally:
        connection.close()

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.strftime('%Y-%m-%d')
        return super(DateTimeEncoder, self).default(obj)

# Use it in your response
@socketio.on('get_users')
def handle_get_users():
    try:
        users = fetch_users()
        emit('user_data', {'data': json.loads(json.dumps(users, cls=DateTimeEncoder))})
    except Exception as e:
        emit('error', {'message': str(e)})

# Route to test if the server is running
@app.route('/')
def index():
    return jsonify({"message": "WebSocket server is running."})

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
