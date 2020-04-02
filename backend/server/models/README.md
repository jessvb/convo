# Models
This directory contains classes that are used in conjunction with `Goals` in `goals`.

The main models to note are `Action`, `Condition`, `Class`, `Execution`, `ValueOf` and `Procedure`.
1. `Procedure`s represent a procedure - in `procedure.py`
2. `Action`s represent actions in a `Procedure` - in `action.py`
3. `Condition`s represent a condition that can be used in a `LoopAction` and `ConditionalAction` - in `condition.py`
4. `Class`es represent a class - in `klass.py`
5. `Execution` represents a procedure execution - in `execution.py`
6. `ValueOf` represent a value of a variable at the moment in time during an execution - in `valueof.py`

Two models `Execution` and `ValueOf` have more detailed explanations below.

## `Execution`
`Execution` represents an execution of a procedure. The DM calls `run()` on `Execution` to execute the procedure in a child thread for two main reasons
1. Server does not hang when executing procedure so it can process other users' commands
2. Allows user to stop execution of a procedure while it's running

During execution, user currently can only tell Convo to stop execution.

## `ValueOf`
Because the value of a variable changes during the execution of a procedure, we need to have something that represents the value of a variable that only evaluates when it comes up during a moment in execution and that's what `ValueOf` does. It is essentially a placeholder for the variable such that it only retrieves the value of the specified variable when it is called upon to do so.

# Actions
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


## Adding New Actions
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
4. Add intent recognition for `CustomAction` in the NLUs (see next section).

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
