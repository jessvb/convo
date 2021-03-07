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
rasa_ports = ["5005", "5006", "5007", "5008", "5009", "5010", "5011", "5012", "5013", "5014", "5015", "5016", "5017", "5018", "5019", "5020", "5021", "5022", "5023", "5024", "5025"]
rasa_available = {"5005": True, "5006": True, "5007": True, "5008": True, "5009": True, "5010": True, "5011": True, "5012": True, "5013": True, "5014": True, "5015": True, "5016": True, "5017": True, "5018": True, "5019": True, "5020": True, "5021": True, "5022": True, "5023": True, "5024": True, "5025": True}
sid_to_rasa_port = {}
