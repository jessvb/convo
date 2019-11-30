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

Docker Compose automatically runs the `web` and `server` services that are defined in the `docker-compose.yml`.
1. `server` - Backend server
3. `web` - Frontend server that allows clients to interface with the backend

### Running
To run the system, run in the project root
```bash
docker-compose up --build
```

Now, head to `http://localhost:8080`.

## TODO
- [ ] Choose a good name (convercode's just a temp name :wink: cocoder? convercoder? coprogrammer? something totally different? feel free to add ideas!)
- [X] Initialize repo :sunglasses:
- [X] Add website/GUI to subfolder, "frontend"
- [X] Add Rasa to subfolder, "backend"
