from flask import Flask, jsonify, request, render_template, Response
import requests
import argparse
import os

app = Flask(__name__)

DEFAULT_PORT = 8080
ENVIRONMENT_VAR_NAME_PORT = 'WEBAPP_PORT'
USERS_SERVICE_ADDRESS = 'users-service' #'localhost:50001' OR k8s 'users-service'

def get_port():
    parser = argparse.ArgumentParser(description='A Flask app that renders and returns webapp pages')
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
   # file_path = os.path.join(os.path.dirname(__file__), 'app', 'login.html')
   return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
   external_response = requests.post(f'http://{USERS_SERVICE_ADDRESS}/login', json=request.json)
   
   content = external_response.content
   status_code = external_response.status_code
   
   return Response(content, status=status_code, content_type=external_response.headers.get('Content-Type'))

if __name__ == '__main__':
    port = get_port()
    print(f"Starting server on port {port}...")
    app.run(host='0.0.0.0', port=port)
