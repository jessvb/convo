import logging

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/convo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db = SQLAlchemy(app)
sio = SocketIO(app, cors_allowed_origins="*")
logging.basicConfig(level=logging.DEBUG)
logger = app.logger

socket_clients = {}
socket_sessions = {}

@app.route('/')
def hello_world():
    return 'Hello, World!'