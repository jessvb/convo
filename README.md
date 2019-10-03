# convercode
An interactive conversational programming agent.

## Structure
*convercode* consists of four modules: (1) a Voice User Interface (VUI), (2) a Natural Language Understanding (NLU) module, (3) a Dialog Manager (DM), and (4) a Program Editor (PE). The VUI can be found in the `frontend` directory. The other modules can be found in the `backend` directory.

![Convercode's four modules](./figs/system_modules.png?raw=true "Convercode's four modules")

## Tech Overview
There are two ways to run the system
1. Local
2. Docker (recommended)

## Local
### Setup
To setup locally, you must setup the frontend and backend separately and install the necessary components. For the frontend and backend setup, read the `README.md` files in their respective directories `frontend` and `backend`.

### Running
Once you successfully start the Node server and the Rasa servers, head to `http://localhost:8080`.

## Docker
### Setup
The easiest way to run the whole system is through Docker and Docker Compose.

Install [Docker for Mac](https://docs.docker.com/docker-for-mac/install/) or [Docker for Windows](https://docs.docker.com/docker-for-windows/install/) and Docker Compose should be included. You should be able to run
```bash
docker -v && docker-compose -v
```
and output should be similar to
```bash
Docker version 19.03.2, build 6a30dfc
docker-compose version 1.24.1, build 4667896b
```

Docker Compose automatically runs three connected services that are defined in the `docker-compose.yml`.
1. `rasa` - Rasa server
2. `action_server` - Rasa actions server
3. `web` - Frontend client that can be used to interface with the Rasa server

To run using Docker, you must still train a Rasa model locally. To do this, install [Rasa](https://rasa.com/docs/rasa/user-guide/installation/), if not on machine.
```bash
pip3 install rasa-x --extra-index-url https://pypi.rasa.com/simple
```
After installing, go to directory `backend/rasa` and run
```bash
rasa train
```
This trains a model and outputs the model into `backend/rasa/models`.

### Running
To run the system, run in the project root
```bash
docker-compose up
```
You should see similar lines in the output as below
```bash
action_server_1  | 2019-10-03 21:47:05 INFO     rasa_sdk.endpoint  - Action endpoint is up and running on http ('0.0.0.0', 5055)
...
web_1            | Server started at 0.0.0.0:8080.
...
rasa_1           | 2019-10-03 21:47:13 INFO     root  - Starting Rasa server on http://localhost:5005
```

Now, head to `http://localhost:8080`.

## TODO
- [ ] Choose a good name (convercode's just a temp name :wink: cocoder? convercoder? coprogrammer? something totally different? feel free to add ideas!)
- [X] Initialize repo :sunglasses:
- [X] Add website/GUI to subfolder, "frontend"
- [X] Add Rasa to subfolder, "backend"
