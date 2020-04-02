# Convo
An interactive conversational programming agent.

## Structure
*Convo* consists of four modules: (1) a Voice User Interface (VUI), (2) a Natural Language Understanding (NLU) module, (3) a Dialog Manager (DM), and (4) a Program Editor (PE). The VUI can be found in the `frontend` directory. The other modules can be found in the `backend` directory.

![Convo's four modules](./figs/system_modules.png?raw=true "Convo's four modules")

## Tech Overview
There are two ways to run the system
1. Local
2. Docker (recommended)

## Local
### Setup
To setup locally, you must setup the frontend and backend separately and install the necessary components. For the frontend and backend setup, read the `README.md` files in their respective directories `frontend` and `backend`.

### Running
Once you successfully start the Node server and the backend server, head to `http://localhost:8080`.

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

Docker Compose automatically runs the `web`, `server` and `rasa` services that are defined in the `docker-compose.yml`.
1. `server` - Backend server
2. `web` - Frontend server that allows clients to interface with the backend
3. `rasa` - Rasa server containing a trained model

There are actually three YAML files that can be used with `docker-compose` - `docker-compose.yml` and `docker-compose.prod.yml` and `docker-compose.local.yml`
- `docker-compose.prod.yml` is used in the case where an admin username and password is required to enter the website
- `docker-compose.local.yml` is used for local development - main difference is no service is needed for a reverse-proxy and CertBot since everything is local

### Local Development and Deployment
To run the system using `docker-compose`, run in the project root
```bash
docker-compose -f docker-compose.local.yml up --build
```

To stop the system, use
```bash
docker-compose down
```

Now, head to `http://localhost:8080`.

## Remote Server Development and Deployment
AppInventor has provided a server for Convo at `userstudy.appinventor.mit.edu` where the system can be deployed.

To deploy the production system on the server, run
```bash
# Backs up the logs and deploys the production system
# Recommended
./deploy_prod.sh

# OR

# Just deploys the production system
docker-compose -f docker-compose.prod.yml up --build
```

If you are simply testing the system and want to deploy, use
```bash
# Backs up the logs and deploys the development system
# Recommended
./deploy.sh

# OR

# Just deploys the development system
docker-compose -f docker-compose.yml up --build
```

### Logs
Currently, logs are handled by the Docker system. Docker will automatically log console outputs from both the Node and Python servers.
- In the Node server, things are logged simply using `console.log`
- In the Python server, it uses the `logging` module which provides different levels of logging like `INFO` and `DEBUG` - however everything is automatically stored by Docker

You can customize the log options for each Docker container in the YAML config files (e.g. `docker-compose.yml`). For example, the logging options for `server` is
```
server:
  logging:
    driver: "json-file"
    options:
      max-size: "20m"
      max-file: "5"
```
`driver` refers to the type of logs that Docker will store and this value should not be changed from `json-file`. `max-size` refers the max size a single log file can get and `max-file` refers to the maximum number of log files Docker will. **Note that if you do not specify a `max-file` while specifying `max-size`, the default value of `max-file` becomes `1`.**

Docker logs (for the server) are stored at `/var/lib/docker/containers` with extension `*json.log`. Note that each service or Docker container (like `web` and `server`) are associated with a `container ID` and the logs are stored under a directory with the name as the `container ID`.

To view your containers and their IDs (the IDs are truncated), use
```bash
docker ps -a
```

For example, if the `server` service's container ID starts with `2df34de1716e`, its logs will be in
```bash
/var/lib/docker/containers/2df34de1716e.../2df34de1716e...-json.log
```
If you want to manually access these logs, you might have to elevate your permissions, which you can do by running `sudo -i` in the terminal and to exit, simply type `exit`

### Scripts
There are three scripts that can be used to help streamline and automate tasks involving retrieving logs and deploying the server.
1. `get_logs.sh` moves all Docker logs from the default location mentioned above to a `logs` directory in the project directory. More specifically, a directory with its name being the time when the script was invoked will be created and all logs will be copied to that directory. For example, if time in milliseconds was `382382328`, all logs at that moment will be copied to `logs/382382328`. This way, logs are backed up and not accidentally removed.
2. `deploy_prod.sh` and `deploy.sh` both retrieve the logs (by calling `get_logs.sh`) before deploying the respective Docker containers in case containers are overwritten or logs get lost