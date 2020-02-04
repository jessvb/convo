import json

from flask import request
from flask_socketio import join_room

from app import app, sio, logger, socket_clients, socket_sessions
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
    logger.info(f"[{sid}][{stage},{part}] Client connected.")

    join_room(str(sid))
    client = socket_clients.get(sid, UserStudyClient(sid))
    socket_clients[sid] = client

    if stage in ["practice", "novice", "advanced"] and part in ["voice", "text", "voice-text"]:
        scenario = client.inputs[stage][part]
        if stage == "practice":
            client.dm = UserStudyDialogManager(sid, stage, part, scenario)
        elif stage == "novice":
            client.dm = UserStudyDialogManager(sid, stage, part, scenario[1])
            sio.emit("noviceInstructions", { "sounds": scenario[0] }, room=str(sid))
        else:
            client.dm = UserStudyAdvancedDialogManager(sid, part, scenario[1], advanced_scenario_check)
            sio.emit("advancedInstructions", { "sounds": scenario[0], "iters": len(scenario[1]) }, room=str(sid))
    else:
        client.dm = DialogManager(sid)

    socket_sessions[request.sid] = (sid, stage, part)
    sio.emit("joined", sid, room=str(sid))

@sio.on("disconnect")
def disconnect():
    sid, stage, part = socket_sessions.get(request.sid)
    if sid:
        client = socket_clients.get(sid)
        del socket_sessions[request.sid]
        logger.info(f"[{sid}][{stage},{part}] Client disconnected.")
        logger.info(f"[{sid}][{stage},{part}] Conversation: {client.context.conversation}")

@sio.on("message")
def message(data):
    message = data.get("message")
    sid = data.get("sid")

    client = socket_clients.get(sid)
    if client is None or message is None:
        return

    dm = client.dm
    if isinstance(dm, UserStudyDialogManager) or isinstance(dm, UserStudyAdvancedDialogManager):
        logger.info(f"[{dm.sid}][{dm.stage},{dm.part}][Message] {message}")
        logger.debug(f"[{dm.sid}][{dm.stage},{dm.part}][State] {dm.context.state}")
    else:
        logger.info(f"[{dm.sid}][Message] {message}")
        logger.debug(f"[{dm.sid}][State] {dm.context.state}")

    res = dm.handle_message(message)
    if (res):
        dm.context.add_message(res)
        state = dm.context.state
        response = {
            "message": res,
            "state": dm.context.state,
            "speak": data.get("speak")
        }

        if isinstance(dm, UserStudyDialogManager) or isinstance(dm, UserStudyAdvancedDialogManager):
            logger.info(f"[{dm.sid}][{dm.stage},{dm.part}][Response] {res}")
            logger.debug(f"[{dm.sid}][{dm.stage},{dm.part}][State] {dm.context.state}")
        else:
            logger.info(f"[{dm.sid}][Response] {res}")
            logger.debug(f"[{dm.sid}][State] {dm.context.state}")

        sio.emit("response", response, room=str(sid))

@sio.on("survey")
def survey(data):
    sid = data.get("sid")
    survey_type = data.get("type")
    survey_data = data.get("data")
    if survey_type == "demographics":
        logger.info(f"[{sid}][survey:demographics] {json.dumps(survey_data)}")
    elif survey_type == "stage":
        logger.info(f"[{sid}][survey:stage] {json.dumps(survey_data)}")
    else:
        logger.debug(json.dumps(data))

@sio.on("email")
def email(data):
    email = data.get("email")
    advanced = data.get("advanced")
    logger.info(f"[Amazon Gift Card][{email}][{advanced}]")

@sio.on("displayTextbox")
def textbox(data):
    sid = data.get("sid")
    stage = data.get("currStage")
    part = data.get("currPart")
    logger.info(f"[{sid}][{stage},{part}] User's voice couldn't be recognized, so the textbox was displayed.")

@sio.on("displayTextbox")
def textbox(data):
    sid = data.get("sid")
    stage = data.get("currStage")
    part = data.get("currPart")
    logger.info(f"[{sid}][{stage},{part}] User could not complete a section, so the next button was displayed.")
