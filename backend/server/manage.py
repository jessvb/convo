from flask import request
from flask_socketio import join_room

from app import sio, logger, socket_clients, socket_sessions
from dialog import DialogManager
from userstudy import *
from client import *

@sio.on("join")
def join(data):
    sid = data.get("sid")
    if sid is None:
        logger.info("Client connected without an SID.")
        return

    stage = data.get("stage")
    part = data.get("part")
    stage_log = f" at {stage} stage" if stage else ""
    part_log = f" on part {part}" if part else ""
    logger.info(f"Client {sid} has connected{stage_log}{part_log}.")

    join_room(str(sid))
    client = socket_clients.get(sid, UserStudyClient(sid))
    socket_clients[sid] = client

    if stage in ["practice", "novice", "advanced"] and part in ["voice", "text", "voice-text"]:
        scenario = client.inputs[stage][part]
        if stage == "practice":
            client.dm = UserStudyDialogManager(sid, stage, scenario)
        elif stage == "novice":
            client.dm = UserStudyDialogManager(sid, stage, scenario[1])
            sio.emit("noviceInstructions", { "sounds": scenario[0] }, room=str(sid))
        else:
            client.dm = UserStudyAdvancedDialogManager(sid, scenario[1], advanced_scenario_check)
            sio.emit("advancedInstructions", { "sounds": scenario[0], "iters": len(scenario[1]) }, room=str(sid))
    else:
        client.dm = DialogManager(sid)

    socket_sessions[request.sid] = (sid, stage, part)
    sio.emit("joined", sid, room=str(sid))

@sio.on("disconnect")
def disconnect():
    sid, stage, part = socket_sessions.get(request.sid)
    if sid:
        del socket_sessions[request.sid]
        logger.info(f"Client {sid} disconnected from {stage} stage at part {part}.")

@sio.on("message")
def message(data):
    message = data.get("message")
    sid = data.get("sid")

    client = socket_clients.get(sid)
    if client is None or message is None:
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

@sio.on("survey")
def survey(data):
    sid = data.get("sid")
    survey_type = data.get("type")
    survey_data = data.get("data")

@sio.on("email")
def email(data):
    email = data.get("email")
    advanced = data.get("advanced")
