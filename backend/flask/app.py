from flask import Flask, request, jsonify, abort
from dialog import DialogManager
from client import Client
from flask_cors import CORS

app = Flask(__name__)
clients = {}
CORS(app)

@app.route('/')
def index():
    return "Hello world!"

@app.route('/message', methods=['POST'])
def message():
    if request.method == "POST":
        data = request.get_json()
        message = data.get("message")
        clientId = data.get("clientId")

        if clientId is None:
            abort(404, description="Resource not found")

        client = clients.get(clientId, Client(clientId))
        if clientId not in clients:
            clients[clientId] = client

        if not message:
            return

        dm = client.dm
        response = {
            "message": dm.handle_message(message),
            "conversation": dm.context.conversation,
            "classes": [str(v) for k, v in dm.context.classes.items()],
            "goal": str(dm.current_goal())
        }

        return jsonify(response)

@app.route('/messages', methods=['POST'])
def messages():
    if request.method == "POST":
        data = request.get_json()
        messages = data.get("messages")
        clientId = data.get("clientId")

        if clientId is None:
            abort(404, description="Resource not found")

        client = clients.get(clientId, Client(clientId))
        if clientId not in clients:
            clients[clientId] = client

        if not messages:
            return

        dm = client.dm
        for i, message in enumerate(messages):
            dm.handle_message(message)

        response = {
            "conversation": dm.context.conversation,
            "classes": [c.json() for c in dm.context.classes.values()],
            "current": dm.context.current.json() if dm.context.current else None,
            "procedures": [p.json() for p in dm.context.procedures.values()],
            "goal": str(dm.current_goal())
        }

        return jsonify(response)

@app.route('/reset', methods=['POST'])
def reset():
    if request.method == "POST":
        data = request.get_json()
        clientId = data.get("clientId")

        if clientId is None:
            abort(404, description="Resource not found")

        client = clients.get(clientId, Client(clientId))
        if clientId not in clients:
            clients[clientId] = client

        return client.dm.reset()
