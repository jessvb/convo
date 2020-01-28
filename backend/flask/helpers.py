import re

def to_snake_case(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name.replace(" ", "_"))
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def clean(string, words_to_remove=[]):
    cleaned = string
    for word in words_to_remove:
        cleaned = cleaned.replace(word, "")
    return cleaned.strip()
