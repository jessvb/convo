from flask import Flask, request, jsonify
from dialog import DialogManager

app = Flask(__name__)
dm = DialogManager()

@app.route('/message', methods=['POST'])
def message():
    if request.method == "POST":
        data = request.get_json()
        message = data.get("message")
        if not message:
            return

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
        if not messages:
            return

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
