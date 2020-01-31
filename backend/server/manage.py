from flask import request
from flask_socketio import join_room

from app import app, sio, socket_clients, socket_sessions
from dialog import DialogManager
from client import Client

@sio.on("join")
def join(sid):
    sid = request.sid if sid is None else sid
    app.logger.info(f"Client {sid} connected.")
    join_room(str(sid))
    client = socket_clients.get(sid, Client(sid))
    socket_clients[sid] = client
    socket_sessions[request.sid] = sid
    client.dm.reset()
    sio.emit("joined", sid, room=str(sid))

@sio.on("disconnect")
def disconnect():
    sid = socket_sessions[request.sid]
    del socket_sessions[request.sid]
    app.logger.info(f"Client {sid} disconnected.")

@sio.on("message")
def message(data):
    message = data.get("message")
    sid = data.get("sid")

    client = socket_clients.get(sid, Client(sid))
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

        sio.emit("response", response, room=str(sid))
