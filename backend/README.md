# Backend
The backend of *convercode* is implemented using the [Rasa](https://rasa.com/) dialog manager and NLU system.

## Setup
Install [Rasa](https://rasa.com/docs/rasa/user-guide/installation/), if not on machine.
```bash
pip3 install rasa-x --extra-index-url https://pypi.rasa.com/simple
```

## Running Rasa
To run the Rasa shell or server, you must have a Rasa model trained. To train a model, run
```bash
rasa train
```
The command will train a model and output into the `models` directory, where it will be automatically referenced. Note that Rasa will by default use the latest trained model in `models`.

To run the Rasa server (which is what you need to do if you want to connect the frontend client to Rasa), run
```bash
rasa run
```
which starts at server at `http://localhost:5005`.

Because we use custom actions with our Rasa model, you have to run the Rasa actions server in a separate terminal as well, with
```bash
rasa run actions --actions actions.actions
```

You can view the full list of possible CLI commands [here](https://rasa.com/docs/rasa/user-guide/command-line-interface/).

## Connecting with Frontend
If you have the frontend server running, the Node server should automatically connect to the Rasa server through sockets. You should see a set of messages like the ones below to confirm that your client has connected to the Rasa server.
```bash
2019-10-03 11:35:27 INFO     engineio.server  - 2a568fc901e14f39911be81f461e7a31: Sending packet OPEN data {'sid': '2a568fc901e14f39911be81f461e7a31', 'upgrades': ['websocket'], 'pingTimeout': 60000, 'pingInterval': 25000}
2019-10-03 11:35:27 INFO     engineio.server  - 2a568fc901e14f39911be81f461e7a31: Sending packet MESSAGE data 0
2019-10-03 11:35:27 INFO     engineio.server  - 2a568fc901e14f39911be81f461e7a31: Received request to upgrade to websocket
2019-10-03 11:35:27 INFO     engineio.server  - 2a568fc901e14f39911be81f461e7a31: Upgrade to websocket successful
```

## Communicating with Rasa
Besides using the UI included in the frontend, you can also communicate with the Rasa model using the built-in Rasa run. To run the Rasa shell, run
```bash
rasa shell
```
The shell allows you to interact with Rasa through messages.

Rasa also provides a REST endpoint to post messages to and Rasa will respond back with a repsonse. To send a message, send a `POST` request to `/webhooks/rest/webhook`. For example, through curl
```bash
curl -d '{"sender":"user", "message":"Tell me a story at 9PM."}' -H "Content-Type: application/json" -X POST http://localhost:5005/webhooks/rest/webhook
```
Rasa will send a response back in the form of a JSON
```json
[{
    "recipient_id":"user",
    "text":"I will read a story at 9PM."
}]
```
