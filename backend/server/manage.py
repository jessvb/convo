import json

from flask import request
from flask_socketio import join_room

from app import app, db, sio, logger, socket_clients, socket_sessions
from dialog import DialogManager
from userstudy import *
from client import *
from db_manage import add_user, get_user, get_procedures

@sio.on("join")
def join(data):
    """Connect to the backend server of Convo"""
    sid = data.get("sid")
    if sid is None:
        logger.info("Client connected without an SID.")
        return

    stage = data.get("stage", "sandbox")
    part = data.get("part", "sandbox")

    # Keep track of all connected clients
    socket_sessions[request.sid] = (sid, stage, part)
    logger.info(f"[{sid}][{stage},{part}] Client connected.")

    # Join room with the SID as the name such that each "room" only contains a single user with the corresponding SID
    join_room(str(sid))

    # Grab client associated with SID, if not exist, create one
    client = socket_clients.get(sid, UserStudyClient(sid))
    if get_user(client.id) is None:
        add_user(client)

    socket_clients[sid] = client

    if stage in ["practice", "novice", "advanced"] and part in ["voice", "text", "voice-text"]:
        # If (stage, part) corresponds to stages/parts of user study, create special dialog manaager
        scenario = client.inputs[stage][part]
        if stage == "practice":
            client.dm = UserStudyDialogManager(sid, stage, part, scenario)
        elif stage == "novice":
            client.dm = UserStudyDialogManager(sid, stage, part, scenario[1])
            sio.emit("noviceInstructions", { "sounds": scenario[0] }, room=str(sid))
            logger.info(f"[{sid}][{stage},{part}] Sounds: {scenario[0]}")
            logger.info(f"[{sid}][{stage},{part}] Created dialog manager for user studies.")
        else:
            client.dm = UserStudyAdvancedDialogManager(sid, part, scenario[1], advanced_scenario_check)
            logger.info(f"[{sid}][{stage},{part}] Sounds: {scenario[0]}")
            logger.info(f"[{sid}][{stage},{part}] Iterations: {len(scenario[1])}")
            logger.info(f"[{sid}][{stage},{part}] Inputs: {scenario[1]}")
            logger.debug(f"[{sid}][{stage},{part}] Created dialog manager for user studies.")
            sio.emit("advancedInstructions", { "sounds": scenario[0], "iters": len(scenario[1]) }, room=str(sid))
    else:
        # Default client and dialog manager
        client.dm = DialogManager(sid, get_procedures(sid))
        logger.debug(f"[{sid}] Created default dialog manager.")

    sio.emit("joined", sid, room=str(sid))

@sio.on("disconnect")
def disconnect():
    """Disconnect from server"""
    sid, stage, part = socket_sessions.get(request.sid)
    if sid:
        # Remove client from the list of connected clients in socket_sessions but keep the client object in socket_clients
        # This way if client reconnects, no work is lost
        client = socket_clients.get(sid)
        del socket_sessions[request.sid]
        logger.info(f"[{sid}][{stage},{part}] Client disconnected.")
        logger.info(f"[{sid}][{stage},{part}] Conversation: {client.dm.context.conversation}")

@sio.on("message")
def message(data):
    message = data.get("message")
    sid = data.get("sid")

    client = socket_clients.get(sid)
    if client is None or message is None:
        return

    voice_or_text = "voice" if data.get("speak", False) else "text"
    dm = client.dm
    if isinstance(dm, UserStudyDialogManager) or isinstance(dm, UserStudyAdvancedDialogManager):
        logger.info(f"[{dm.sid}][{dm.stage},{dm.part}][Message]({voice_or_text}) {message}")
        logger.debug(f"[{dm.sid}][{dm.stage},{dm.part}][State] {dm.context.state}")
    else:
        logger.info(f"[{dm.sid}][Message] {message}")
        logger.debug(f"[{dm.sid}][State] {dm.context.state}")

    res = dm.handle_message(message)
    if (res):
        # If there is response message, log and send to client
        dm.context.add_message(res)
        state = dm.context.state
        response = {
            "message": res,
            "state": dm.context.state,
            "speak": data.get("speak", False)
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
    """Log survey data from user study"""
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
    """Log email and level for gift card for user study"""
    email = data.get("email")
    advanced = data.get("advanced")
    logger.info(f"[Amazon Gift Card][{email}][{advanced}]")

@sio.on("displayTextbox")
def textbox(data):
    """Log when the textbox was manually displayed in a voice-only stage"""
    sid = data.get("sid")
    stage = data.get("currStage")
    part = data.get("currPart")
    logger.info(f"[{sid}][{stage},{part}] User's voice couldn't be recognized, so the textbox was displayed.")

@sio.on("displayButton")
def next_button(data):
    """Log when the "Next" button was manually displayed"""
    sid = data.get("sid")
    stage = data.get("currStage")
    part = data.get("currPart")
    logger.info(f"[{sid}][{stage},{part}] User could not complete a section, so the next button was displayed.")

@sio.on("wordReplace")
def word(data):
    """Log a word replacement"""
    sid = data.get("sid")
    stage = data.get("stage")
    part = data.get("part")
    original = data.get("original")
    replacement = data.get("replacement")
    logger.info(f"[{sid}][{stage},{part}][Replacement] The word, {original}, was replaced with the word, {replacement}.")
