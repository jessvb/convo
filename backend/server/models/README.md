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