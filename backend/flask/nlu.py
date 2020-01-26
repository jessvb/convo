import re
from goals import *
from models import *

create_class_regex = "(?:make|create)(?: a)? class(?: (?:called|named) (.+))?"
create_conditional_regex = "(?:create(?: a)? conditional)|(?:(if .+) then (.+))|(?:(.+) (if .+))"
create_list_regex = "(?:make|create)(?: a)? list(?: (?:called|named) (.+)| (.+))?"
create_until_loop_regex = "(?:(?:make|create)(?: a)? until loop)|(?:(.+) (until .+))"
create_while_loop_regex = "(?:(?:make|create)(?: a)? while loop)|(?:(while .+) then (.+))"
create_procedure_regex = "(?:make|create)(?: a)? procedure(?: (?:called|named) (.+))?"
add_property_regex = "add(?: a)?(?: (.+))? property(?: called| named)?(?:(?: (.+))? to (.+)| (.+))?"
add_procedure_regex = "add(?: an?)? (?:procedure|action)(?: called| named)?(?:(?: (.+))? to (.+)| (.+))?"
add_to_list_regex = "add(?: (.+))? to list(?: (.+))?"
say_regex = "say(?: (.+))?"
set_regex = "set(?: the)?(?: (.*))? (property|variable)(?:(?: (.+))? to (.+)| (.+))?"
create_variable_regex = "(?:create|make)(?: a)?(?: (.+))? variable(?: called| named)?(?:(?: (.+))? and set(?: it)? to (.+)| (.+))?"
increment_variable_regex = "(?:add(?: (.+))? to variable(?: (.+))?)|(?:increment variable(?:(?: (.+))? by (.+)| (.+))?)"
say_condition_regex = "(?:until|if) i say (.+)"
comparison_condition_regex = "(?:if|until) (.+) is ((?:(?:less|greater) than(?: or equal to)?)|equal to) (.+)"
run_regex = "(?:run|play)(?: (.+))?"
get_user_input_regex = "get(?: user)? input(?: and (?:(?:call it)?|(?:name it)?|(?:save it as)?) (.+))?"
value_of_regex = "(?:the )?value of (?:(?:the )?variable )?(.+)"
edit_regex = "(?:open|edit)(?: (.+))?"
go_to_step_regex = "(?:go to step(?: (.+))?|go to(?: the)? (.+) step)"
delete_step_regex = "(?:delete|remove) step"
add_step_regex = "add step"

class SemanticNLU(object):
    def __init__(self, context):
        self.context = context

    def parse_message(self, message):
        message = message.lower()
        for parse in [self.try_parse_goal, self.try_parse_value_of, self.try_parse_condition]:
            parsed = parse(message)
            if parsed is not None:
                return parsed

    def try_parse_goal(self, message):
        if message is None:
            return message
        elif re.match(create_conditional_regex, message):
            match = re.match(create_conditional_regex, message)
            condition = group(match, [1, 4])
            action = group(match, [2, 3])
            return ConditionalActionGoal(self.context, condition=self.try_parse_condition(condition), action=self.try_parse_goal(action))
        elif re.match(create_until_loop_regex, message):
            match = re.match(create_until_loop_regex, message)
            action = group(match, 1)
            condition = group(match, 2)
            return UntilLoopActionGoal(self.context, condition=self.try_parse_condition(condition), action=self.try_parse_goal(action))
        elif re.match(create_while_loop_regex, message):
            match = re.match(create_while_loop_regex, message)
            condition = group(match, 1)
            action = group(match, 2)
            return WhileLoopActionGoal(self.context, condition=self.try_parse_condition(condition), action=self.try_parse_goal(action))
        elif re.match(create_class_regex, message):
            match = re.match(create_class_regex, message)
            return CreateClassGoal(self.context, name=group(match, 1))
        elif re.match(create_procedure_regex, message):
            match = re.match(create_procedure_regex, message)
            return AddProcedureGoal(self.context, name=group(match, 1))
        elif re.match(add_property_regex, message):
            match = re.match(add_property_regex, message)
            return AddPropertyGoal(self.context, klass=group(match, 3), name=group(match, [2, 4]), type=group(match, 1))
        elif re.match(add_procedure_regex, message):
            match = re.match(add_procedure_regex, message)
            return AddClassProcedureGoal(self.context, name=group(match, [1, 3]), klass=group(match, 2))
        elif re.match(set_regex, message):
            match = re.match(set_regex, message)
            if group(match, 2) == "property":
                return SetPropertyActionGoal(self.context, name=group(match, [1, 3, 5]), value=group(match, 4))
            elif group(match, 2) == "variable":
                return SetVariableActionGoal(self.context, name=group(match, [1, 3, 5]), value=self.try_parse_value_of(group(match, 4)))
        elif re.match(create_variable_regex, message):
            match = re.match(create_variable_regex, message)
            return CreateVariableActionGoal(self.context, name=group(match, [2, 4]), value=self.try_parse_value_of(group(match, 3)))
        elif re.match(increment_variable_regex, message):
            match = re.match(increment_variable_regex, message)
            return IncrementVariableActionGoal(self.context, name=group(match, [2, 3, 5]), value=self.try_parse_value_of(group(match, [1, 4])))
        elif re.match(say_regex, message):
            match = re.match(say_regex, message)
            return SayActionGoal(self.context, phrase=self.try_parse_value_of(group(match, 1)))
        elif re.match(create_list_regex, message):
            match = re.match(create_list_regex, message)
            return CreateListActionGoal(self.context, name=group(match, [1, 2]))
        elif re.match(add_to_list_regex, message):
            match = re.match(add_to_list_regex, message)
            return AddToListActionGoal(self.context, name=group(match, 2), value=group(match, 1))
        elif re.match(run_regex, message):
            match = re.match(run_regex, message)
            return RunGoal(self.context, name=group(match, 1))
        elif re.match(get_user_input_regex, message):
            match = re.match(get_user_input_regex, message)
            return GetUserInputActionGoal(self.context, variable=group(match, 1))
        elif re.match(edit_regex, message):
            match = re.match(edit_regex, message)
            return EditGoal(self.context, name=group(match, 1))
        elif re.match(go_to_step_regex, message):
            match = re.match(go_to_step_regex, message)
            return GoToStepGoal(self.context, step=group(match, [1, 2]))
        elif re.match(delete_step_regex, message):
            match = re.match(delete_step_regex, message)
            return DeleteStepGoal(self.context)
        elif re.match(add_step_regex, message):
            match = re.match(add_step_regex, message)
            return AddStepGoal(self.context)

    def try_parse_condition(self, message):
        if message is None:
            return message
        elif re.match(comparison_condition_regex, message):
            match = re.match(comparison_condition_regex, message)
            return ComparisonCondition(variable=group(match, 1), op=group(match, 2), value=group(match, 3))
        elif re.match(say_condition_regex, message):
            match = re.match(say_condition_regex, message)
            return SayCondition(phrase=group(match, 1))

    def try_parse_value_of(self, message):
        if message is None:
            return message
        elif re.match(value_of_regex, message):
            match = re.match(value_of_regex, message)
            return ValueOf(variable=group(match, 1))
        else:
            return message

def group(match, indices):
    if isinstance(indices, int):
        idx = indices
        return match.group(idx) if len(match.groups()) > 0 and match.group(idx) else None

    for idx in indices:
        if match.group(idx):
            return match.group(idx)
