import re
import string
from word2number import w2n

def to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name.replace(" ", "_"))
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def clean(s, words_to_remove=[]):
    cleaned = s
    for word in words_to_remove:
        cleaned = cleaned.replace(word, "")
    return cleaned.strip()

def strip_punctuation(s):
    return s.translate(str.maketrans('', '', string.punctuation.replace("-", "")))

def parse_number(message):
    if message is None or not isinstance(message, str):
        return message

    contains_negation = ("negative" in message) or ("-" in message)
    factor = -1 if contains_negation else 1
    negation_removed = message.replace("negative", "").replace("-", "").strip()

    if not negation_removed:
        return message

    if negation_removed.replace(".", "", 1).isnumeric():
        value = factor * float(negation_removed)
        return int(value) if value.is_integer() else value

    try:
        return factor * w2n.word_to_num(negation_removed)
    except ValueError as e:
        return None
