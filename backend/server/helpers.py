import re
import string
from word2number import w2n
from app import logger

def to_snake_case(name):
    """Convert string to snakecase"""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name.replace(" ", "_"))
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def strip_punctuation(s):
    """Strip punctuations from string"""
    return s.translate(str.maketrans('', '', string.punctuation.replace("-", "")))

def parse_number(message):
    """Try to parse a number from a string"""
    if message is None or not isinstance(message, str):
        return message

    # Check if message contains a negation of number
    contains_negation = ("negative" in message) or ("-" in message)
    factor = -1 if contains_negation else 1
    negation_removed = message.replace("negative", "").replace("-", "").strip()

    # After removing negation, if result is empty string, not a number
    if not negation_removed:
        return message

    # Check if string contains just numeric characters (also removing the first instance of a period which may represent a decimal)
    if negation_removed.replace(".", "", 1).isnumeric():
        value = factor * float(negation_removed)
        # Cast float into an integer if it can
        return int(value) if value.is_integer() else value

    # If it doesn't contain just numeric characters, try to convert string to a number using word_to_num
    # which converts word-representation of numbers into a number, i.e "two" -> 2 or "twenty-five" -> 25
    try:
        current_value = factor * w2n.word_to_num(negation_removed)
    except ValueError as e:
        return None

    # This is kind of a hack. To make sure we don't convert phrases that aren't just a number to a number, 
    # (e.g. I have seven cats should not return 7) we try removing certain words from the phrase to see if it changes
    # the outcome of the number. For example, removing 'twenty' from 'twenty two' would result in a different 
    # numerical value (22 to 2), whereas removing 'I' from 'I have seven cats' would still return 7, making it
    # not a phrase that should be numerically converted.
    words_in_negation = negation_removed.split(" ")
    if len(words_in_negation) > 1:
        for i in range(len(words_in_negation)):
            new_string = recreate_string(words_in_negation, i)
            try:
                new_value = factor * w2n.word_to_num(new_string)
                if new_value == current_value:
                    return None
            except ValueError as e:
                continue
    return current_value

def recreate_string(words, index_to_exclude):
    new_string = ""
    for i in range(len(words)):
        if i != index_to_exclude:
            new_string += words[i]
            new_string += " "
    return new_string

def convert_to_dict(obj):
    """
    A function takes in a custom object and returns a dictionary representation of the object.
    This dict representation includes meta data such as the object's module and class names.
    """

    if isinstance(obj, set):
        return list(obj)

    #  Populate the dictionary with object meta data
    obj_dict = {
        "__class__": obj.__class__.__name__,
        "__module__": obj.__module__
    }

    #  Populate the dictionary with object properties
    obj_dict.update(obj.__dict__)

    return obj_dict

def convert_to_object(obj_dict):
    """
    Function that takes in a dict and returns a custom object associated with the dict.
    This function makes use of the "__module__" and "__class__" metadata in the dictionary
    to know which object type to create.
    """
    if "__class__" in obj_dict:
        # Pop ensures we remove metadata from the dict to leave only the instance arguments
        class_name = obj_dict.pop("__class__")

        # Get the module name from the dict and import it
        module_name = obj_dict.pop("__module__")

        # We use the built in __import__ function since the module name is not yet known at runtime
        module = __import__(module_name)

        # Get the class from the module
        class_ = getattr(module,class_name)

        # Use dictionary unpacking to initialize the object
        obj = class_(**obj_dict)
    else:
        obj = obj_dict
    return obj
