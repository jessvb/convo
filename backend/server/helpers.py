import re
import string
from word2number import w2n

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

    # If it doesn't contain just numeric characters, try to convert string to a numbr using word_to_num
    # which converts word-representation of numbers into a number, i.e "two" -> 2 or "twenty-five" -> 25
    try:
        return factor * w2n.word_to_num(negation_removed)
    except ValueError as e:
        return None
