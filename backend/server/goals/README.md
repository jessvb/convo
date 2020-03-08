# Goals
This directory contains all classes that inherit the base `BaseGoal` class, which represent the user and agent goals used in Convo. All `Goal` classes have the same inherent structure and standard methods. To see the basic structure, checkout out `BaseGoal` in `base.py`.

## Workflow of Goals
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

## Example - `CreateVariableActionGoal`
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
