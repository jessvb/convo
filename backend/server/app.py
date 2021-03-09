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
rasa_ports = ["5005", "5006"]
# rasa_connections = {"5005": 0, "5006": 0}
sid_to_rasa_port = {}
