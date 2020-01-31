import logging
import threading

from flask import Flask, request, jsonify, abort
from flask_socketio import SocketIO, join_room
from dialog import DialogManager
from client import Client
from flask_cors import CORS

app = Flask(__name__)
logger = app.logger

if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

clients = {}
sessions = {}
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# @app.route('/')
# def index():
#     return "Hello world!"

@socketio.on("join")
def join(sid):
    sid = request.sid if sid is None else sid
    print(f"Client {sid} connected.", flush=True)
    join_room(str(sid))
    client = clients.get(sid, Client(sid))
    clients[sid] = client
    sessions[request.sid] = sid
    client.dm.reset()
    socketio.emit("joined", sid, room=str(sid))

@socketio.on("disconnect")
def disconnect():
    sid = sessions[request.sid]
    del sessions[request.sid]
    print(f"Client {sid} disconnected.")

@socketio.on("message")
def message(data):
    with app.test_request_context('/'):
        message = data.get("message")
        sid = data.get("sid")

        client = clients.get(sid, Client(sid))
        if not message:
            return

        dm = client.dm
        res = dm.handle_message(message.lower())
        if (res):
            dm.context.add_message(res)
            state = dm.context.state
            response = {
                "message": res,
                "state": dm.context.state,
                "speak": data.get("speak")
            }

            socketio.emit("response", response, room=str(sid))
