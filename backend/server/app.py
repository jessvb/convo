import logging

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
CORS(app)
sio = SocketIO(app, cors_allowed_origins="*")
logging.basicConfig(level=logging.INFO)
logger = app.logger

socket_clients = {}
socket_sessions = {}
