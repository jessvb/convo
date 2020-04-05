# Convo
This directory contains the main components of Convo that make up the NLU, the dialog manager and the program editor.

Convo is deployed on a Flask Python server that utilizes WebSocket connections to communicate through a [Python port](https://flask-socketio.readthedocs.io/en/latest/) of the Javascript library [socket.io](https://socket.io/) as well the standard HTTP REST API.

# Implementation
The application is defined and managed in `app.py` and `manage.py`. More specifically, `app.py` implements the Flask application with WebSocket support and `manage.py` defines the routes and socket events that the application support. A client first connects to the socket opened by Convo and triggers the `join` event in `manage.py`. After successful connection, the client can send a message to Convo, starting a conversation, by sending a message with the `message` event.

The dialog manager of Convo is implemented in `dialog.py`. There are two NLU modules implemented. One is the regex-based semantic NLU in `nlu.py` while the other is ML-based Rasa NLU in `rasa_nlu.py`.

Other files include:
- `db_manage.py` contains any database schemas, models and functions that are used in Convo
- `error.py` contains custom `Error`s for errors that pop up during Convo.
- `helpers.py` contains useful helper functions.
- `client.py` define `Client`s that represent client connections to Convo. There are two clients implemented, one is the general `Client` and the other is a client `UserStudyClient` specifically made for the user study performed in February. It included details and information needed for the user study.
- `question.py` contains a simple question-and-answering module that Convo uses.

## Database
Convo currently uses a SQLite3 database which doesn't require a server. The database is simply stored in a DB file in `db`. You can interact with the database (say `test.db`) if you have `sqlite3` installed by running
```bash
sqlite3 test.db
```
To interact with the database in Python, Convo uses [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/), which provides an interface on top of the database so you don't have to write SQL queries. To setup a local database for Convo, check out `db/README.md`.

There are currently two tables in the database that are defined by `db.Model`s in `db_manage.py`
1. `user` - contains all users connected to Convo - defined by `User`
2. `program` - contains all procedures created in Convo - defined by `Program`

To store `Procedure` objects in the database, Convo essentially transforms the object into a dictionary of values before encoding it into JSON and storing the JSON string in the database. The opposite happens when retrieving a procedure from the database.

## Goals
The `goals` directory contains all classes that inherit the base `BaseGoal` class, which represent the user and agent goals used in Convo. All `Goal` classes have the same inherent structure and standard methods. To see the basic structure, checkout out `BaseGoal` in `base.py`.

### Workflow of Goals
The way `Goal`s work in Convo is as follows:

1. When user sends a message to Convo with the intent to perform an action that is supported by a goal (e.g. create a variable), a goal is created
2. `DM` checks if the goal is valid within the current context
3. If goal is valid, `DM` checks if the goal can already be completed using the `is_complete` property
4. If goal cannot be completed yet (usually due to needing some slot-filling values), responds appropriately to the user (usually asking user for response)
    * When a goal with slots is created, any values that have not been received, a `GetInputGoal` is created for each value not received
    * The response is determined by the current subgoals and the context
5. Once user sends the next message, `DM` tries to "advance" the goal using `advance()`
    * `advance()` looks at the goal and checks if it can be completed given new message by user. If it has any subgoals, the goal's `advance()` will call `advance()` on its subgoals and can call `complete()` on its subgoals when they get completed
    * Usually, the subgoal is `GetInputGoal` asking user to provide a value
6. Once goal is advanced, the `DM` checks if goal can be completed once again
    * If it cannot, once again, respond to user based on the subgoals
    * If it can, `DM` calls `complete` on the goal, which contains actions performed to complete the goal - which can include changing the context state, adding a variable to list of variables, adding an `Action` to a procedure, etc.

### Example - `CreateVariableActionGoal`
Here is an example of the workflow with `CreateVariableActionGoal` which adds a `CreateVariableAction` to a procedure.

1. User asks to "create a variable" so Convo creates a `CreateVariableActionGoal`.
    * `CreateVariableActionGoal` has two slots that need to be filled - `name` (variable name) and `value` (initial value) so it creates two `GetInputGoal` for each slot and adds them to its `todos`
2. The DM checks if `CreateVariableActionGoal` is complete, which is not complete since there are two `GetInputGoal`s that need to be completed first. Therefore, Convo responds to user with a message from the first `GetInputGoal` - asking for the `name`
3. Once user provides the next mesasge, the DM advances `CreateVariableActionGoal`
    * Advancing the goal involves advancing `GetInputGoal`, which it does and the first slot `name` gets filled, completing the first `GetInputGoal`.
4. DM once again checks if `CreateVariableActionGoal` is completed, which is still not because of the other `GetInputGoal`.
    * It repeats steps 2 and 3 except with slot `value`
5. DM checks `CreateVariableActionGoal` again and finally the goal is deemed complete as all of its subgoals and other completion conditions are complete. DM proceeds to call `complete()` on `CreateVariableActionGoal`
    * For `CreateVariableActionGoal`, calling `complete()` leads to creation of a `CreateVariableAction` that is added to the procedure currently being added or edited.

## Models
The `models` directory contains classes that are used in conjunction with `Goals` in `goals`.

The main models to note are `Action`, `Condition`, `Class`, `Execution`, `ValueOf` and `Procedure`.
1. `Procedure`s represent a procedure - in `procedure.py`
2. `Action`s represent actions in a `Procedure` - in `action.py`
3. `Condition`s represent a condition that can be used in a `LoopAction` and `ConditionalAction` - in `condition.py`
4. `Class`es represent a class - in `klass.py`
5. `Execution` represents a procedure execution - in `execution.py`
6. `ValueOf` represent a value of a variable at the moment in time during an execution - in `valueof.py`

Two models `Execution` and `ValueOf` have more detailed explanations below.

### `Execution`
`Execution` represents an execution of a procedure. The DM calls `run()` on `Execution` to execute the procedure in a child thread for two main reasons
1. Server does not hang when executing procedure so it can process other users' commands
2. Allows user to stop execution of a procedure while it's running

During execution, user currently can only tell Convo to stop execution.

### `ValueOf`
Because the value of a variable changes during the execution of a procedure, we need to have something that represents the value of a variable that only evaluates when it comes up during a moment in execution and that's what `ValueOf` does. It is essentially a placeholder for the variable such that it only retrieves the value of the specified variable when it is called upon to do so.

### Actions
`Actions` are defined as an action performed during the execution of a program created in Convo (e.g. creating a variable or making Convo say something). The basic structure of an `Action` can be found in `models/action.py` as well as some already-implemented `Action`s.

The `Action` classes contain any necessary properties and information needed during execution. How exactly these actions are "executed" are defined in the `evaluate_action` method of the `Execution` class in `models/execution.py`. This may range from saying something back to the user using the `emit` method or manipulating any variables during execution.

When an user is creating or editing a program, actions are added to a Convo program through the creation and completion of `ActionGoal`s, a subclass of `BaseGoal`. When Convo recognizes the intent of the user to create a specific action, an `ActionGoal` is created. When the goal is deemed complete, the corresponding `Action` is created and added to the program's list of actions in the goal's `complete` method. Therefore, each `ActionGoal` in `goals` directory has a corresponding `Action` model that it creates during completion in the `models` directory.

The source code for `ActionGoal` is in `goals/base.py`. Some examples of `ActionGoal`s can be found in `goals/variable.py`.

The basic structure of a `CustomAction` inheriting `Action` looks like
```python
class CustomAction(Action):
    """Custom action"""
    def __init__(self):
        # Initialize any properties needed here
        # by adding to the parameters of __init__
        pass

    def __str__(self):
        # String representation of the class
        name = self.__class__.__name__
        # Default is the just converting to snake case and removing "Action"
        # For AnotherCustomAction, the __str__ would return "another_custom"
        return to_snake_case(name[:-len("Action")])

    def json(self):
        # JSON representation of the action
        # Usually a dictionary of its properties to their values
        return { "name": str(self) }

    def python(self):
        # String representation of potential corresponding Python code
        # Currently not too important, since no Python support yet
        pass

    def to_nl(self):
        # The "natural language" representation of the action
        # Essentially, what is this action doing in simple terms?
        pass

    def __eq__(self, other):
        # Define equality between two CustomActions
        # Usually it's a check that all properties are equal in value
        pass
```

### Adding New Actions
To add and support a new action in Convo (let's call it `CustomAction`), here are high-level steps and things you must do or implement
1. Create a new `CustomAction` class for the new action
    - Make sure to define any necessary information or properties needed and to inherit `Action`
    - See `models/action.py` for existing `Action` classes
    - You can add the new action to `models/action.py` or a new file in `models` directory. For the latter, make sure to add an import to `models/__init__.py` for the new file.
2. Create a new `CustomActionGoal` class, inheriting from `ActionGoal`
    - Add necessary information needed for the corresponding `CustomAction` as parameters to the constructor `__init__`
    - For any parameters needed to be filled by the user, use `setattr` to set the parameter or to create a `GetInputGoal` asking the user for the information. See `goals/variable.py` for examples for this.
    - In `complete`, create the corresponding `CustomAction` and add it to `actions`
    - You can add the new goal to the `goals` directory in an existing file or a new file. For the latter, make sure to add an import to `goals/__init__.py` for the new file.
3.  Add the "execution" of the `CustomAction`
    - Located in `evaluate_action` of the `Execution` class in `models/execution.py`
    - To add, check for type using `isinstance(action, CustomAction)`
    - Define what `CustomAction` should do. For example, if the `CustomAction` should say something to the user, you can call `self.emit` to send something to the user. See the execution of the `SayAction` for an example of this.
4. Add intent recognition for `CustomAction` in the NLUs (see section "Intent Recognition of `Action`s" below).

### Testing New Actions
To test out the new action, go to `http(s):/<host>/debug` of the website (whether Docker or local)
1. Say or enter *"create a procedure called test"*. Convo should respond with something starting with *"What do you want to happen in the procedure first?"*
2. Say the utterance that you have Convo recognize to trigger the adding of the new action. For example, if you want to add a `CreateVariableAction`, say or enter *"create a variable"* to tell Convo you want to add the action. If the action is successfully added to the procedure, Convo should say something on the lines of *"Added action to the procedure!"*.
3. Once action is added to the procedure, say *"done"* to finish creating the procedure.
4. Now to test the execution of the new action, say *"run test"* to run the newly created procedure and make sure the action does what you wanted it to do.

### Intent Recognition of `Action`s
To allow Convo to recognize that user wants to add a certain action to their program, you must add support to the natural language understanding (NLU) modules. There are two NLUs, one is regex-based semantic parser and the other is the Rasa NLU. You can add support to either or both (recommended) of the NLUs.

#### Regex-based Semantic NLU
To add support for `CustomAction` in the regex-based semantic NLU (everything is done in `server/nlu.py`)
1. Add the regex for phrases that user will say to tell Convo they want to want to add `CustomAction` in the top of the file
2. Add the regex variable to `action_regexes`
3. Under the `parse_action_goal` method, add an `if` statement for matching the newly-created regex to create a `CustomActionGoal`
    - Follow the pattern used in matching of other regexes
    - Use helper function `group` to extract any captured groups from the regex that will be used for arguments to constructor parameters for the `CustomActionGoal`

#### Rasa NLU
Before working with the Rasa NLU be sure to read `backend/rasa/README.md`. To add support for `CustomAction` in Rasa NLU
1. Add the corresponding `CustomActionGoal` to `intent_goal` in `server/rasa_nlu.py`.
2. In `backend/rasa/data/nlu.md`, add a new intent with training examples that the user would say to tell Convo to create this new action
3. Train the Rasa NLU such that the newest model include this new intent with commands `rasa train nlu`

## Tests
No concrete testing framework has been developed for testing methods used in Convo but there are simple tests that were written while developing Convo in the `tests` directory
