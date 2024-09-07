from flask import Flask, jsonify, request
import argparse
import os

app = Flask(__name__)

DEFAULT_PORT = 8080
ENVIRONMENT_VAR_NAME_PORT = 'USERS_PORT'

def get_port():
    parser = argparse.ArgumentParser(description='A Flask app that returns user information')
    parser.add_argument('-p', '--port', type=int, help='Port number for the server to listen on')
    args = parser.parse_args()

    if args.port and (0 <= args.port <= 65536):
        return args.port

    port = os.getenv(ENVIRONMENT_VAR_NAME_PORT)
    if port and (0 <= port <= 65536):
        try:
            return int(port)
        except ValueError:
            print(f"Invalid PORT environment variable: {port}. Using default port {DEFAULT_PORT}.")
    
    return DEFAULT_PORT

@app.route('/')
def index():
    response = {
        "message": "Hello, World From Users",
        "status": "success"
    }
    return jsonify(response)


@app.route('/login', methods=['POST'])  # Not ideal HTTP naming conventions
def login():
   response = {
      "message": "Login Failed: Invalid Credentials",
      "status": "error"
   }
   data = request.get_json()
   if  'username' in data and 'password' in data and data["username"] == 'admin' and data['password'] == 'admin':
      response['message'] = "Welcome to the demo project!"
      response['status'] = "ok"
   
   return jsonify(response)

if __name__ == '__main__':
    port = get_port()
    print(f"Starting server on port {port}...")
    app.run(host='0.0.0.0', port=port)
