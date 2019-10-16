from flask import Flask, request, jsonify
from agent import Agent

app = Flask(__name__)
agent = Agent()

@app.route('/')
def hello_world():
    return "Hello world!"

@app.route('/message', methods=['POST'])
def message():
    if request.method == "POST":
        req_data = request.get_json()
        message = req_data.get("message")
        if not message:
            return

        response, action = agent.parse_message(message)
        return jsonify({
            "response": response,
            "debug": action
        })

@app.route('/actions', methods=['GET'])
def actions():
    if request.method == "GET":
        return jsonify({ "actions": agent.actions })

@app.route('/agent', methods=['GET'])
def info():
    if request.method == "GET":
        return jsonify(agent.get_info())

@app.route('/code', methods=['GET'])
def code():
    if request.method == "GET":
        return agent.to_code()

from dm import DialogManager
tracker = DialogManager()

@app.route('/debug', methods=['POST'])
def debug():
    if request.method == "POST":
        req_data = request.get_json()
        message = req_data.get("message")
        if not message:
            return

        response = tracker.add(message)

        return jsonify({
            "response": response,
            "_editor": tracker.editor._info(),
            "_stack": [action._json() for action in tracker.stack],
            "_variables": list(tracker.editor.variables),
            "_messages": tracker.conversation
        })
