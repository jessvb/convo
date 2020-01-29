import re
import string

def to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name.replace(" ", "_"))
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def clean(s, words_to_remove=[]):
    cleaned = s
    for word in words_to_remove:
        cleaned = cleaned.replace(word, "")
    return cleaned.strip()

def strip_punctuation(s):
    return s.translate(str.maketrans('', '', string.punctuation))
