import re

from goals import *

create_class_regex = "(?:make|create)(?: a)? class ?(?:called|named)? ?(.+)?"
add_property_regex = "(?:add)(?: a)? ?(.+)?(?: property) ?(?:called|named)? ?(?:(?:(.+)?(?: to )(.+))|(?:(.+)))?"
add_procedure_regex = "(?:add)(?: a)? ?(.+)?(?: procedure) ?(?:called|named)? ?(?:(?:(.+)?(?: to )(.+))|(?:(.+)))?"

class SemanticNLU(object):
    def __init__(self, context):
        self.context = context

    def parse_message(self, message):
        message = message.lower()

        if re.match(create_class_regex, message):
            match = re.match(create_class_regex, message)
            self.context.parsed = CreateClassGoal(self.context, match.group(1) if match.group(1) else None)
        elif re.match(add_property_regex, message):
            match = re.match(add_property_regex, message)
            name = match.group(2) if match.group(2) else (match.group(4) if match.group(4) else None)
            type = match.group(1) if match.group(1) else None
            klass = match.group(3) if match.group(3) else None
            self.context.parsed = AddClassPropertyGoal(self.context, klass, name, type)
        elif message in ["add a procedure", "add an action"]:
            self.context.parsed = AddClassProcedureGoal(self.context)
        elif message in ["set property value"]:
            self.context.parsed = SetClassPropertyValueGoal(self.context)
        elif message in ["create a variable", "make a variable"]:
            self.context.parsed = InitVariableGoal(self.context)
        elif message in ["set variable"]:
            self.context.parsed = SetVariableValueGoal(self.context)
        elif message in ["increment variable"]:
            self.context.parsed = IncrementVariableGoal(self.context)
        elif message == "say":
            self.context.parsed = SayGoal(self.context)
        elif message == "create a conditional":
            self.context.parsed = CreateConditionalGoal(self.context)
        elif message == "create a loop":
            self.context.parsed = CreateLoopGoal(self.context)
        elif message == "if count is less than 5":
            self.context.parsed = ComparisonCondition(self.context, "count", "<", 5)
        elif message == "until i say stop":
            self.context.parsed = SayCondition(self.context, "stop")

        return self.context.parsed
