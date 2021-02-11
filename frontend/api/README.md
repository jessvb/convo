# API
The frontend of *convercode* currently contains the experiment site. Various experiments are performed to find the efficacy of different conversational programming setups. For a list of experiments, after successfully getting the server running, go to `/experiments`.

You can also visit `/debug` to have an interface where you can test against your locally-running Convo server.

## Tech Overview
The frontend uses an Express Node server and the Socket.IO library to stream audio from the microphone to Google's [Speech-to-Text API](https://cloud.google.com/speech-to-text/docs/streaming-recognize) in realtime. The audio is transcribed and the transcript is communicated back via sockets. The transcribed text is used to communicate with the Rasa NLU in the backend.

## Setup
Install Node.js through a [package manager](https://nodejs.org/en/download/package-manager/)(recommended) or through an [installer](https://nodejs.org/en/download/). Run
```bash
npm install
```
in directory `api` once Node.js and `npm` is installed.

By default, the pages on the website connects via WebSockets to the production servers on `userstudy.appinventor.mit.edu`. To have the website connect to your local servers, you have to comment and uncomment a couple of lines in a couple of the JS files.
1. `experiment.js` - Comment line 2 and uncomment line 4
2. `socket.js` - Comment lines 2-3 and uncomment lines 5-6

### Speech-To-Text
To be able to use Google's Speech-to-Text API, you must create an account and a project on Google Cloud Platform (GCP). When prompted, you can choose to go for the 90 day free trial, but afterwards you must upgrade to a full account. As of right now, we ask you to enter in your personal credit card information and set that as your billing for the project. In most cases, you won't be using the API enough to ever get charged. You can either choose to make an end user key or a service key. We recommend using a service key. Go to Google's [Quickstart](https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries) for instructions on setting everything up. 

If you choose to create a user key, download your private key as a JSON file and name it `gcpkey.json` (or another name that you can remember).

Once you obtain your private key, move your key `gcpkey.json` to `api`. Copy the file `.env.sample` and rename it `.env`. Set the value of the environment variable `GOOGLE_APPLICATION_CREDENTIALS` in `.env` to the relative path of the key so the `.env` file should be
```bash
GOOGLE_APPLICATION_CREDENTIALS="gcpkey.json"
```

If you choose to create a service account key, download your private key as a JSON file and name it `servicekey.json` (or another name that you can remember).

Once you obtain your private key, move your key `servicekey.json` to `api`. Copy the file `.env.sample` and rename it `.env`. Set the value of the environment variable `GOOGLE_APPLICATION_CREDENTIALS` in `.env` to the relative path of the key so the `.env` file should be
```bash
GOOGLE_APPLICATION_CREDENTIALS="servicekey.json"
```

## Running the Server
In the directory of this README, start the app using
```bash
npm start
```
Once the server starts, head to `http://localhost:8080/` to check out the front page of the user study website.

If you have Convo's backend locally running, chect out `http://localhost:8080/debug` where you can use to interact and test Convo.

When you visit this page, in the terminal where the Node server is running, you should able to see logs similar to
```bash
> convo-client@1.0.0 start /convo/frontend
> node app.js

HTTP server started at http://0.0.0.0:8080/.
[cd7ff4194dbd4cbbbd20a24dd9856448][sandbox,sandbox] Client connected to server.
[cd7ff4194dbd4cbbbd20a24dd9856448][sandbox,sandbox] Client disconnected.
```