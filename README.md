# convercode
An interactive conversational programming agent.

## structure
*convercode* consists of four modules: (1) a Voice User Interface (VUI), (2) a Natural Language Understanding (NLU) module, (3) a Dialog Manager (DM), and (4) a Program Editor (PE). The VUI can be found in the `frontend` directory. The other modules can be found in the `backend` directory.

![Convercode's four modules](./figs/system_modules.png?raw=true "Convercode's four modules")

## setup
The backend setup is explained in `backend/README.md`. Once this is set up, you can locally interact with the agent through a web browser and the code contained in `frontend/`.

## TODO
- [ ] Choose a good name (convercode's just a temp name :wink: cocoder? convercoder? coprogrammer? something totally different? feel free to add ideas!)
- [X] Initialize repo :sunglasses:
- [X] Add website/GUI to subfolder, "frontend"
- [X] Add Rasa to subfolder, "backend"
