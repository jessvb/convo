from flask import request
from flask_socketio import join_room

from app import app, sio, socket_clients, socket_sessions
from dialog import DialogManager
from userstudy import *
from client import Client

@sio.on("join")
def join(data):
    if isinstance(data, str):
        sid = data
        stage = None
    else:
        sid = request.sid if data.get("sid") is None else data.get("sid")
        stage = data.get("stage")
    stage_log = f" and at the {stage} stage" if stage else ""
    app.logger.info(f"Client {sid} has connected{stage_log}.")

    join_room(str(sid))
    client = socket_clients.get(sid, Client(sid))
    socket_clients[sid] = client

    if stage:
        if stage in ["novice", "practice"]:
            client.dm = UserStudyDialogManager(sid, stage, userstudy_scenarios[stage])
        elif stage == "advanced":
            inputs, check = userstudy_scenarios[stage]
            client.dm = UserStudyAdvancedDialogManager(sid, inputs, check)
        else:
            client.dm = DialogManager(sid)
    else:
        client.dm = DialogManager(sid)

    socket_sessions[request.sid] = (sid, stage)
    sio.emit("joined", sid, room=str(sid))

@sio.on("disconnect")
def disconnect():
    sid, stage = socket_sessions.get(request.sid)
    if sid:
        del socket_sessions[request.sid]
        app.logger.info(f"Client {sid} disconnected from the {stage} stage.")

@sio.on("message")
def message(data):
    message = data.get("message")
    sid = data.get("sid")

    client = socket_clients.get(sid, Client(sid))
    if not message:
        return

    dm = client.dm
    res = dm.handle_message(message)
    if (res):
        dm.context.add_message(res)
        state = dm.context.state
        response = {
            "message": res,
            "state": dm.context.state,
            "speak": data.get("speak")
        }

        sio.emit("response", response, room=str(sid))
