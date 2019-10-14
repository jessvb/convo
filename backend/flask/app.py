from flask import Flask, request, jsonify
from utils import *
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

        response = agent.process_message(message)
        return jsonify({ "response": response.message })
