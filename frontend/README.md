# FrontEnd
The frontend of *convercode* includes a click-and-hold recording button, and an output text box, such that users can talk with the agent and see the current user-program (text box is temporary - for debugging). In future iterations, (when the agent provides sufficient information about the user-program through conversation) we will remove the output text box.

## Tech Overview
The frontend uses a `express` Node.js server and `Socket.IO` to stream audio from the microphone to Google's Speech-to-Text API in realtime.

## Running the server
Before running the server, make sure to have `node` and `npm` installed. Then, navigate to the `frontend` directory run `npm install`. Lastly, run `npm start` and head to `http://localhost:8080/`.

## Recording
To start recording, click the `Start Recording` button and talk into the microphone. In the console logs, you should start seeing the transcribed text from Google's Speech-to-Text API. In future iteration, there will be an output textbox.
