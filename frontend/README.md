# Frontend
The frontend of *convercode* includes a click-and-hold recording button, and an output text box, such that users can talk with the agent and see the current user-program (text box is temporary - for debugging). In future iterations, (when the agent provides sufficient information about the user-program through conversation) we will remove the output text box.

## Tech Overview
The frontend uses an Express Node server and the Socket.IO library to stream audio from the microphone to Google's [Speech-to-Text API](https://cloud.google.com/speech-to-text/docs/streaming-recognize) in realtime. The audio is transcribed and the transcript is communicated back via sockets. The transcribed text is used to communicate with the Rasa NLU in the backend.

## Setup
Install Node.js through a [package manager](https://nodejs.org/en/download/package-manager/)(recommended) or through an [installer](https://nodejs.org/en/download/). Run
```bash
npm install
```
in directory `frontend` once Node.js and `npm` is installed.

To be able to use Google's Speech-to-Text API, you must create an account and a project on Google Cloud Platform (GCP). Go to Google's [Quickstart](https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries) for instructions on setting everything up. Download your private key as a JSON file and name it `gcpkey.json` (or another name that you can remember).

Once you obtain your private key, move your key `gcpkey.json` to `frontend`. Copy the file `.env.sample` and rename it `.env`. Set the value of the environment variable `GOOGLE_APPLICATION_CREDENTIALS` in `.env` to the relative path of the key so the `.env` file should be
```bash
GOOGLE_APPLICATION_CREDENTIALS="gcpkey.json"
```

## Running the Server
Navigate to directory `frontend` and start the app
```bash
cd convercode/frontend
npm start
```
Once the server starts, head to `http://localhost:8080/`.

## Communicating with Rasa
To start recording and communicating with the Rasa NLU, click and hold the `Hold Down to Talk` button and speak into the microphone. Once you are done speaking, release the button. Any of your spoken commands or messages will be shown and prefixed with `Client`. Once your message is transcribed, the message will also be sent to the Rasa server. Responses by the Rasa server will be sent back to you and prefixed with `Rasa`.