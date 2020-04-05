import re
import string
from goals import *
from models import *
from helpers import *

create_procedure_regex = "(?:make|create)(?: a)? (?:procedure|program)(?: (?:called|named) (.+))?$"
rename_procedure_regex = "rename(?: (.+) to (.+)| (.+))"
delete_procedure_regex = "(?!.*step)delete(?: (.+))"
execute_regex = "run(?: (.+))?"
edit_regex = "(?:open|edit)(?: (.+))?"

create_list_regex = "(?:make|create)(?: a)? list(?: (?:called|named) (.+)| (.+))?"
add_to_list_regex = "add(?: (.+))? to list(?: (.+))?"
say_regex = "say(?: (.+))?"
get_user_input_regex = "(?:listen to user|(?:listen for|get)(?: user)? input)(?: and (?:(?:call it)?|(?:name it)?|(?:save it as)?) (.+))?"
value_of_regex = "(?:the )?value of (?:(?:the )?variable )?(.+)"
play_sound_regex = "play(?: the)?(?: (.+))? sound"

create_variable_regex = "(?:create|make)(?: a)?(?: (.+))? variable(?: called| named)?(?:(?: (.+))? and set(?: it)? to (.+)| (.+))?"
set_variable_regex = "(?!change step$)(?:set|change)(?:(?: the)? value of)?(?:(?: (.+))? to (.+)| (.+))"
add_to_variable_regex = "add(?: (.+))? to (.+)"
subtract_from_variable_regex = "subtract(?: (.+))? from (.+)"

go_to_step_regex = "(?:go to step(?: (.+))?|go to(?: the)? (.+) step)"
delete_step_regex = "(?:delete|remove)(?: the)? step"
add_step_regex = "(?:add|create|make)(?: a)?(?: new)? step"
change_step_regex = "(?:change|replace)(?: the)? step"

create_conditional_regex = "(?:create|make)(?: a)? conditional|if (.+) then (.+)|(.+) if (.+)|if (.+)"
create_loop_regex = "(.+) (while|until) (.+)|(while|until) (.+)"

comparison_condition_regex = "(?:if |while |until )?(.+) is ((?:(?:less|greater) than(?: or equal to)?)) (.+)"
equality_condition_regex = "(?!.*less|.*greater)(?:if |while |until )?(.+) is(?: (not))?(?: equal to)? (.+)"

variable_regex = "(?:(?:a|the) variable)(?: (.+))?|variable (.+)"
procedure_regex = "(?:(?:a|the) procedure|procedure)(?: called)?(?: (.+))?"

say_hello_world_regex = "\bhello world\b"

action_regexes = [
    say_hello_world_regex,
    say_regex, play_sound_regex,
    set_variable_regex, create_variable_regex, add_to_variable_regex, subtract_from_variable_regex,
    get_user_input_regex,
    create_list_regex, add_to_list_regex
]
condition_regexes = [comparison_condition_regex, equality_condition_regex]

class SemanticNLU(object):
    """
    A semantic NLU parser using on regex-based expressions

    Uses the main function parse_message to parse message with supported regexes and corresponding helper functions
    """
    def __init__(self, context):
        self.context = context

    def parse_message(self, message):
        """Parse and try to extract goal from input messages using various specific functions"""
        message = message.lower()
        for parse in [self.parse_home_goal, self.parse_action_goal, self.parse_step_goal, self.parse_condition, self.parse_value_of]:
            # Try to parse with each parse function and returns the first object that is not None
            parsed = parse(message)
            if parsed is not None:
                return parsed

    def parse_home_goal(self, message):
        """Parse function for goals and intents that happen in the home state"""
        if message is None:
            return message
        elif re.search(create_procedure_regex, message):
            match = re.search(create_procedure_regex, message)
            return CreateProcedureGoal(self.context, name=group(match, 1))
        elif re.search(execute_regex, message):
            match = re.search(execute_regex, message)
            return ExecuteGoal(self.context, name=self.parse_procedure(group(match, 1)))
        elif re.search(edit_regex, message):
            match = re.search(edit_regex, message)
            return EditGoal(self.context, name=self.parse_procedure(group(match, 1)))
        elif re.search(rename_procedure_regex, message):
            match = re.search(rename_procedure_regex, message)
            return RenameProcedureGoal(self.context, name=self.parse_procedure(group(match, [1, 3])), new_name=group(match, 2))
        elif re.search(delete_procedure_regex, message):
            match = re.search(delete_procedure_regex, message)
            return DeleteProcedureGoal(self.context, name=self.parse_procedure(group(match, 1)))
        elif message == "hello world"
            return SayHelloWorldActionGoal(self.context)


    def parse_step_goal(self, message):
        """Parse function for goals and intents that relate to editing"""
        if message is None:
            return message
        elif re.match(go_to_step_regex, message):
            # Going to specific step
            match = re.match(go_to_step_regex, message)
            return GoToStepGoal(self.context, step=group(match, [1, 2]))
        elif re.match(delete_step_regex, message):
            # Deleting step
            match = re.match(delete_step_regex, message)
            return DeleteStepGoal(self.context)
        elif re.match(add_step_regex, message):
            # Adding step
            match = re.match(add_step_regex, message)
            return AddStepGoal(self.context)
        elif re.match(change_step_regex, message):
            # Changing step
            match = re.match(change_step_regex, message)
            return ChangeStepGoal(self.context)

    def parse_action_goal(self, message):
        """Parse function for goals and intents that lead to adding actions to procedures"""
        if message is None:
            return message
        elif re.match(create_conditional_regex, message):
            # Creating conditional
            match = re.match(create_conditional_regex, message)
            condition = group(match, [1, 4])
            action = group(match, [2, 3])
            if not (condition and action) and group(match, 5):
                # If neither condition nor action was detected in message - e.g. "create a conditional"
                condition, action = self.parse_condition_and_action(group(match, 5))
                return ConditionalActionGoal(self.context, condition=condition, action=action) if condition and action else None
            else:
                # If message with pattern - "If <condition>, <action>" - was detected
                return ConditionalActionGoal(self.context, condition=self.parse_condition(condition), action=self.parse_action_goal(action))
        elif re.match(create_loop_regex, message):
            # Creating loop
            match = re.match(create_loop_regex, message)
            loop = group(match, [2, 4])
            condition = group(match, 3)
            action = group(match, 1)
            if not (condition and action) and group(match, 5):
                # If neither condition nor action was detected in message - e.g. "create a while/until loop"
                condition, action = self.parse_condition_and_action(group(match, 5))
                return LoopActionGoal(self.context, loop=loop, condition=condition, action=action) if condition and action else None
            else:
                # If message with pattern - "While/Until <condition>, <action>" or "<action> while/until <condition" - was detected
                return LoopActionGoal(self.context, loop=loop, condition=self.parse_condition(condition), action=self.parse_action_goal(action))
        elif re.match(set_variable_regex, message):
            # Setting value of an existing variable
            match = re.match(set_variable_regex, message)
            return SetVariableActionGoal(self.context, name=self.parse_variable(group(match, [1, 3])), value=self.parse_value(group(match, 2)))
        elif re.match(create_variable_regex, message):
            # Creating a new variable
            match = re.match(create_variable_regex, message)
            return CreateVariableActionGoal(self.context, name=group(match, [2, 4]), value=self.parse_value(group(match, 3)))
        elif re.match(add_to_variable_regex, message):
            # Adding to a variable
            match = re.match(add_to_variable_regex, message)
            variable = self.parse_variable(group(match, 2))
            if variable == "variable":
                # If parsed value of variable string is just "variable", assume that name of variable was not given
                variable = None
            return AddToVariableActionGoal(self.context, name=variable, value=self.parse_value(group(match, 1)))
        elif re.match(subtract_from_variable_regex, message):
            # Subtracting from a variable
            match = re.match(subtract_from_variable_regex, message)
            variable = self.parse_variable(group(match, 2))
            if variable == "variable":
                # If parsed value of variable string is just "variable", assume that name of variable was not given
                variable = None
            return SubtractFromVariableActionGoal(self.context, name=variable, value=self.parse_value(group(match, 1)))
        elif re.match(say_regex, message):
            # Telling Convo to say something
            match = re.match(say_regex, message)
            return SayActionGoal(self.context, phrase=self.parse_value(group(match, 1)))
        elif re.match(create_list_regex, message):
            # Creating a list
            match = re.match(create_list_regex, message)
            return CreateListActionGoal(self.context, name=group(match, [1, 2]))
        elif re.match(add_to_list_regex, message):
            # Adding to existing list
            match = re.match(add_to_list_regex, message)
            return AddToListActionGoal(self.context, name=group(match, 2), value=group(match, 1))
        elif re.match(play_sound_regex, message):
            # Playing a sound
            match = re.match(play_sound_regex, message)
            return PlaySoundActionGoal(self.context, sound=group(match, 1))
        elif re.match(get_user_input_regex, message):
            # Getting user input
            match = re.match(get_user_input_regex, message)
            return GetUserInputActionGoal(self.context, variable=group(match, 1))
        elif message == "hello world"
            return SayHelloWorldActionGoal(self.context)

    def parse_condition(self, message):
        """Parse condition"""
        if message is None:
            return message
        elif re.match(comparison_condition_regex, message):
            # Comparison conditions which includes >, =>, <, <=
            match = re.match(comparison_condition_regex, message)
            value_of = self.parse_value_of(group(match, 1))
            parsed_variable = self.parse_variable(group(match, 1))
            if isinstance(value_of, ValueOf):
                variable = value_of
            else:
                variable = ValueOf(parsed_variable)
            return ComparisonCondition(variable=variable, op=group(match, 2), value=self.parse_value(group(match, 3)))
        elif re.match(equality_condition_regex, message):
            # Equality condition which includes =, !=
            match = re.match(equality_condition_regex, message)
            value_of = self.parse_value_of(group(match, 1))
            parsed_variable = self.parse_variable(group(match, 1))
            if isinstance(value_of, ValueOf):
                variable = value_of
            else:
                variable = ValueOf(parsed_variable)
            return EqualityCondition(variable=variable, value=self.parse_value(group(match, 3)), negation=(group(match, 2) is not None))

    def parse_condition_and_action(self, message):
        """
        Try to separate and parse condition and action in conditionals and loops where condition and action are not separated by a word like "then"

        To do this, try to parse for an action within the message.
        If action is successfully found, parse for the condition of the substring of the message
        from the start of the message to the start of part where the action was parsed.
        """
        message = strip_punctuation(message)
        for rgx in action_regexes:
            match = re.search(rgx, message)
            if not match:
                continue
            for condition_rgx in condition_regexes:
                condition_match = re.search(condition_rgx, message[:match.start()].strip())
                if not condition_match:
                    continue
                return self.parse_condition(condition_match.group(0)), self.parse_action_goal(match.group(0))
        return None, None

    def parse_variable(self, message):
        """Try to parse variable name from a message"""
        if message is None:
            return message
        elif re.match(variable_regex, message):
            match = re.match(variable_regex, message)
            return match.group(1) if match.group(1) else match.group(2)
        else:
            return message

    def parse_procedure(self, message):
        """Try to parse procedure name from a message"""
        if message is None:
            return message
        elif re.match(procedure_regex, message):
            match = re.match(procedure_regex, message)
            return match.group(1)
        else:
            return message

    def parse_value(self, message):
        """Try to parse a value which may in the form of a string, a number or a ValueOf object"""
        value_of = self.parse_value_of(message)
        if value_of:
            return value_of

        number = parse_number(message)
        if number is not None:
            return number

        return message

    def parse_value_of(self, message):
        """Try to parse message of the form "value of <variable>" and return a ValueOf object"""
        if not message:
            return message
        elif re.match(value_of_regex, message):
            match = re.match(value_of_regex, message)
            return ValueOf(variable=group(match, 1))

def group(match, idx):
    if isinstance(idx, int) and len(match.groups()) > 0 and match.group(idx):
        return match.group(idx)
    elif isinstance(idx, list):
        for i in idx:
            res = group(match, i)
            if res:
                return res
    return None
