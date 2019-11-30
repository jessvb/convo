# Backend
Currently, the backend of *convercode* contains a Python Flask server that represents the NLU, program editor and the dialog manager. Most, if not all, communications with the Flask server will be through API requests.

## Setup
Install Python 3.7, if not on machine. If on MacOS, I recommend installing through [Homebrew](https://brew.sh/)
```
brew install python
```

After installing Python, install the packages necessary to run the Flask server
```
cd convercode/backend/flask
pip install -r requirements.txt
```

## Running the Server
Navigate to directory `backend/flask` and start the app
```bash
cd convercode/backend/flask
flask run
```
Once the server starts, to verify that server is running, head to `http://localhost:5000/` and you should see `"Hello world!"`.
