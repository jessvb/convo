import re

from goals import *

create_class_regex = "(?:make|create)(?: a)? class(?: (?:called|named) (.+))?"
add_property_regex = "add(?: a)?(?: (.+))? property(?: called| named)?(?:(?: (.+))? to (.+)| (.+))?"
add_procedure_regex = "add(?: an?)? (?:procedure|action)(?: called| named)?(?:(?: (.+))? to (.+)| (.+))?"
set_regex = "set(?: the)?(?: (.*))? (property|variable)(?:(?: (.+))? to (.+)| (.+))?"
create_variable_regex = "(?:create|make)(?: a)?(?: (.+))? variable(?: called| named)?(?:(?: (.+))? and set(?: it)? to (.+)| (.+))?"
increment_variable_regex = "(?:add(?: (.+))? to variable(?: (.+))?)|(?:increment variable(?:(?: (.+))? by (.+)| (.+))?)"
say_regex = "say(?: (.+))?"
create_conditional_regex = "(?:create(?: a)? conditional)|(?:(if .+) then (.+))|(?:(.+) (if .+))"
create_loop_regex = "(?:create(?: a)? loop)|(?:(.+) (until .+))"
say_condition_regex = "(?:until|if) i say (.+)"
comparison_condition_regex = "(?:if|until) (.+) is ((?:(?:less|greater) than(?: or equal to)?)|equal to) (.+)"

class SemanticNLU(object):
    def __init__(self, context):
        self.context = context

    def parse_message(self, message):
        message = message.lower()
        for parse in [self.try_parse_goal, self.try_parse_condition]:
            parsed = parse(message)
            if parsed is not None:
                return parsed

        return None

    def try_parse_goal(self, message):
        if message is None:
            return None
        elif re.match(create_conditional_regex, message):
            match = re.match(create_conditional_regex, message)
            condition = group(match, [1, 4])
            action = group(match, [2, 3])
            return CreateConditionalGoal(self.context, condition=self.try_parse_condition(condition), action=self.try_parse_goal(action))
        elif re.match(create_loop_regex, message):
            match = re.match(create_loop_regex, message)
            action = group(match, 1)
            condition = group(match, 2)
            return CreateLoopGoal(self.context, condition=self.try_parse_condition(condition), action=self.try_parse_goal(action))
        elif re.match(create_class_regex, message):
            match = re.match(create_class_regex, message)
            return CreateClassGoal(self.context, name=group(match, 1))
        elif re.match(add_property_regex, message):
            match = re.match(add_property_regex, message)
            return AddClassPropertyGoal(self.context, klass=group(match, 3), name=group(match, [2, 4]), type=group(match, 1))
        elif re.match(add_procedure_regex, message):
            match = re.match(add_procedure_regex, message)
            return AddClassProcedureGoal(self.context, klass=group(match, 2), name=group(match, [1, 3]))
        elif re.match(set_regex, message):
            match = re.match(set_regex, message)
            if group(match, 2) == "property":
                return SetClassPropertyValueGoal(self.context, name=group(match, [1, 3, 5]), value=group(match, 4))
            elif group(match, 2) == "variable":
                return SetVariableValueGoal(self.context, name=group(match, [1, 3, 5]), value=group(match, 4))
        elif re.match(create_variable_regex, message):
            match = re.match(create_variable_regex, message)
            return InitVariableGoal(self.context, name=group(match, [2, 4]), value=group(match, 3))
        elif re.match(increment_variable_regex, message):
            match = re.match(increment_variable_regex, message)
            return IncrementVariableGoal(self.context, name=group(match, [2, 3, 5]), value=group(match, [1, 4]))
        elif re.match(say_regex, message):
            match = re.match(say_regex, message)
            return SayGoal(self.context, phrase=group(match, 1))
        else:
            return None

    def try_parse_condition(self, message):
        if message is None:
            return None
        elif re.match(comparison_condition_regex, message):
            match = re.match(comparison_condition_regex, message)
            return ComparisonCondition(self.context, group(match, 1), group(match, 2), group(match, 3))
        elif re.match(say_condition_regex, message):
            match = re.match(say_condition_regex, message)
            return SayCondition(self.context, phrase=group(match, 1))
        else:
            return None

def group(match, indices):
    if isinstance(indices, int):
        idx = indices
        return match.group(idx) if match.group(idx) else None

    for idx in indices:
        if match.group(idx):
            return match.group(idx)
    return None
