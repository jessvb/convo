# Backend
Currently, the backend of *Convo* contains a Python Flask server that represents the regex-based semantic NLU, program editor and the dialog manager. Most, if not all, communications with the Flask server will be through API requests. In addition to the regex-based semantic NLU, Convo also utilizes a ML-based NLU called Rasa, which is located in the `rasa` directory. Rasa is entirely optional as it is still in a development phase.

## Setup
Install Python 3.7, if not on machine. If on MacOS, I recommend installing through [Homebrew](https://brew.sh/)
```bash
brew install python
```

Install the packages necessary to run the Flask server
```bash
cd backend/server
pip install -r requirements.txt
```

Create a SQLite3 database for Convo to use, open up an interactive Python shell in the `server` directory and run
```python
from db_manage import db
db.create_all()
```

This will create a SQLite3 database `convo.db` in `db` which you can access if you have `sqlite3` installed.

If you want to use Rasa with Convo locally, follow the installation steps detailed in `rasa/README.md` to train a model and start a server with the model.

Read more about Convo and Rasa in their READMEs located in their respective directorys `server` and `rasa`.

## Running the Server
Navigate to directory `server` and start the app
```bash
cd server
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 --log-level=info manage:app
```
Once the server starts, to verify that server is running, head to `http://localhost:5000/` and you should see `"Hello, World!"`.

If you have the frontend server running, to check if the frontend is successfully connected to the backend, go to `http://localhost:8080/debug`.
Once the page loads, in the terminal where the Python server is running, you should able to see logs similar to
```bash
[2020-04-04 20:53:27 -0500] [89720] [INFO] Starting gunicorn 19.9.0
[2020-04-04 20:53:27 -0500] [89720] [INFO] Listening at: http://0.0.0.0:5000 (89720)
[2020-04-04 20:53:27 -0500] [89720] [INFO] Using worker: eventlet
[2020-04-04 20:53:27 -0500] [89724] [INFO] Booting worker with pid: 89724
INFO:app:[cd7ff4194dbd4cbbbd20a24dd9856448][sandbox,sandbox] Client connected.
DEBUG:app:[cd7ff4194dbd4cbbbd20a24dd9856448] Created default dialog manager.
```
If you do not see something similar to the last two lines, it might be because you haven't (un)commented out the lines detailed in the README in the `frontend` directory.
