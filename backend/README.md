# Backend
Currently, the backend of *Convo* contains a Python Flask server that represents the regex-based semantic NLU, program editor and the dialog manager. Most, if not all, communications with the Flask server will be through API requests. In addition to the regex-based semantic NLU, Convo also utilizes a ML-based NLU called Rasa, which is located in the `rasa` directory. Rasa is entirely optional as it is still in a development phase.

## Setup
Install Python 3.7, if not on machine. If on MacOS, I recommend installing through [Homebrew](https://brew.sh/)
```
brew install python
```

After installing Python, install the packages necessary to run the Flask server
```
cd backend/server
pip install -r requirements.txt
```

## Running the Server
Navigate to directory `server` and start the app
```bash
cd server
flask run
```
Once the server starts, to verify that server is running, head to `http://localhost:5000/` and you should see `"Hello world!"`.

If you want to use Rasa with Convo locally, follow the installation steps detailed in `rasa/README.md` to train a model and start a server with the model.

Read more about Convo and Rasa in their READMEs located in their respective directorys `server` and `rasa`.
