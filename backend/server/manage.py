import requests
import json

from flask import request
from flask_socketio import join_room

from app import app, sio, logger, socket_clients, socket_sessions, rasa_ports, sid_to_rasa_port
from dialog import DialogManager
from userstudy import *
from client import *
from db_manage import get_or_create_user, get_procedures

@app.route('/')
def healthcheck():
    return 'Hello, World!'

@sio.on("join")
def join(data):
    """Connect to the backend server of Convo"""
    sid = data.get("sid")
    if sid is None:
        logger.info("Client connected without an SID.")
        return

    stage = data.get("stage", "sandbox")
    part = data.get("part", "sandbox")
    port = data.get("port")
    intents = data.get("intents")
    phrases = data.get("phrases")

    sid_to_rasa_port[sid] = port
    socket_sessions[request.sid] = (sid, stage, part, port)
    logger.info(f"[{sid}][{stage},{part},{port}] Client connected.")
    logger.info(f"Current connected SIDs: {socket_sessions}")

    # Join room with the SID as the name such that each "room" only contains a single user with the corresponding SID
    join_room(str(sid))

    # Grab client associated with SID, if not exist, create one
    client = socket_clients.get(sid, UserStudyClient(sid))
    get_or_create_user(client)

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
        client.dm = DialogManager(sid, port, get_procedures(sid))
        logger.debug(f"[{sid}] Created default dialog manager.")
        add_intents_and_entities(client.dm.context, intents, phrases)
        logger.debug(f"[{sid}] Finish adding intents {intents} to context.")

    sio.emit("joined", sid, room=str(sid))

    intro = '''
        Hi, I'm Convo! What would you like to do?
        To get started, you can create a procedure by saying "Create a procedure".
        If you want to run a procedure, say "Run" and the name of the procedure.
    '''
    response = {
        "message": intro,
        "state": client.dm.context.state,
        "speak": False
    }
    sio.emit("response", response, room=str(sid))

@sio.on("disconnect")
def disconnect():
    """Disconnect from server"""
    if request.sid:
        sid, stage, part, port = socket_sessions.get(request.sid)
        if sid:
            # Remove client from the list of connected clients in socket_sessions but keep the client object in socket_clients
            # This way if client reconnects, no work is lost
            client = socket_clients.get(sid)
            del socket_sessions[request.sid]
            del sid_to_rasa_port[sid]
            logger.info(f"[{sid}][{stage},{part},{port}] Client disconnected.")
            logger.info(f"[{sid}][{stage},{part},{port}] Conversation: {client.dm.context.conversation}")

@sio.on("rasaPort")
def connectRasaPort(data):
    sid = data.get("sid")
    rasaPort = data.get("port")
    if rasaPort not in rasa_ports:
        logger.info(f"Group ID {rasaPort} not a valid port.")
        return
    client = socket_clients.get(sid)
    if client is None:
        return
    dm = client.dm
    dm.context.rasa_port = rasaPort
    sid_to_rasa_port[sid] = rasaPort
    logger.debug(f"Current sid to rasa: {sid_to_rasa_port}")

@sio.on("train")
def train(data):
    sid = data.get("sid")
    intents = data.get("intents")
    trainingData = data.get("trainingData")
    # First, add all intents and respective entities to the context.
    client = socket_clients.get(sid)
    if client is None:
        return
    dm = client.dm
    add_intents_and_entities(dm.context, intents, trainingData)
    logger.debug(f"finished adding all intents and entities at port {dm.context.rasa_port}")

    # Then, train the NLU model using this new data.
    training_data = format_training_data(intents, trainingData)
    res = None
    try:
        rasa_url = "http://rasa" + dm.context.rasa_port + ":" + dm.context.rasa_port + "/model/train"
        res = requests.post(rasa_url, json=training_data)
    except requests.ConnectionError as e:
        logger.info("Cannot connect to Rasa server.")
        return None

    # If no response from Rasa NLU server, return None
    if (res is None or res.status_code != 200):
        logger.info("No response from the Rasa server.")
        return None

    logger.debug("Finished training Rasa.")

    # Replace the currently trained model
    model_file = res.headers["filename"]
    model_file_absolute = "/app/models/" + model_file
    request = {
        "model_file": model_file_absolute
    }

    payload = json.dumps(request)
    replace_res = None
    try:
        rasa_url = "http://rasa" + dm.context.rasa_port + ":" + dm.context.rasa_port + "/model"
        replace_res = requests.put(rasa_url, data=payload)
    except requests.ConnectionError as e:
        logger.info(f"Rasa server at port {dm.context.rasa_port} is restarting.")
        return None

    if (replace_res is None or replace_res.status_code != 204):
        logger.info("No response from the Rasa server when replacing the model.")
        return None

    logger.debug(f"Finished updating the trained model of Rasa at port {dm.context.rasa_port}.")

    res = dm.handle_train(intents)
    # If there is response message, log and send to client
    dm.context.add_message(res)
    response = {
        "message": res,
    }
    sio.emit("trained", response, room=str(sid))

def add_intents_and_entities(context, intents, trainingData):
    for i in range(len(intents)):
        intent = intents[i]
        intent = intent.replace(" ", "_")
        entities = set([])

        trainingDatas = trainingData[i].split(",")
        for data in trainingDatas:
            _, extracted_entities = extract_entities(data)
            for entity in extracted_entities:
                entities.add(entity["entity"])
        original_intent = intent.replace("_", " ")
        context.add_intent(original_intent, list(entities))
    return


def create_rasa_nlu_data(intents, trainingData):
    common_examples = []
    for i in range(len(intents)):
        intent = intents[i]
        intent = intent.replace(" ", "_")
        trainingDatas = trainingData[i].split(",")
    
        for data in trainingDatas:
            text, entities = extract_entities(data)
            common_examples.append(
                {
                    "text": text,
                    "intent": intent,
                    "entities": entities
                }
            )

    return json.dumps({
        "rasa_nlu_data": {
            "regex_features": [],
            "entity_synonyms": [],
            "common_examples": common_examples,

        }
    })

def extract_entities(training_data):
    entities = []
    text, entity = extract_entity(training_data)
    while entity != []:
        entities.append(entity)
        text, entity = extract_entity(text)

    return (text, entities)

def extract_entity(text):
    try:
        start = text.index("[")
        end = text.index("]", start)
        entity_value = text[start+1:end]

        entity_start = text.index("(", end)
        entity_end = text.index(")", entity_start)
        entity = text[entity_start+1:entity_end]

        # remove brackets and entity from text
        new_text = text[:start] + text[start+1:]
        new_end = new_text.index("]")
        new_text = new_text[:new_end] + new_text[new_end+1:]

        new_entity_start = new_text.index("(")
        new_entity_end = new_text.index(")", new_entity_start)
        new_text = new_text[:new_entity_start] + new_text[new_entity_end+1:]

        return (new_text, {"start": start, "end": end - 1, "value": entity_value, "entity": entity, "role": "", "extractor": "DIETClassifier",})

    except ValueError:
        return (text, [])

def format_training_data(intents, training_datas):
    data = {
    "config": "language: en\r\npipeline:\r\n  - name: HFTransformersNLP\r\n    model_name: \"bert\"\r\n  - name: LanguageModelTokenizer\r\n  - name: LanguageModelFeaturizer\r\n  - name: LexicalSyntacticFeaturizer\r\n  - name: CountVectorsFeaturizer\r\n    OOV_token: oov\r\n    token_pattern: (?u)\\b\\w+\\b\r\n  - name: CountVectorsFeaturizer\r\n    analyzer: \"char_wb\"\r\n    min_ngram: 1\r\n    max_ngram: 4\r\n  - name: DIETClassifier\r\n    epochs: 100\r\n  - name: EntitySynonymMapper",
    "nlu": create_rasa_nlu_data(intents, training_datas),
    "force": False, 
    "save_to_default_model_directory": True
    }
    return data

@sio.on("message")
def message(data):
    message = data.get("message")
    sid = data.get("sid")
    isUnconstrained = data.get("isUnconstrained")

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

    res = dm.handle_message(message, isUnconstrained)
    if (res):
        # If there is response message, log and send to client
        dm.context.add_message(res)
        state = dm.context.state
        response = {
            "message": res,
            "state": dm.context.state,
            "speak": data.get("speak", False),
            "isUnconstrained": data.get("isUnconstrained")
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
