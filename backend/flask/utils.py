import spacy
import requests

from spacy import displacy
from spacy.symbols import *

nlp = spacy.load("en_core_web_sm")

texts = [
    "make a variable called strawberry and set it to 0",
    "create a variable",
    "make a variable and call it strawberry",
    "I want to make a variable",
    "make variable",
    "I want to make a variable and name it birds",
    "set strawberry to 0"
]

for text in texts:
    doc = nlp(text)
    for chunk in doc.noun_chunks:
        print(chunk.root.text, chunk.root.dep_, chunk.root.head.text)
    print()

# # for text in texts:
#     # print(get_part_of_speech(text))
#     # find_inputs(nlp(text))

# displacy.serve(nlp(texts[2]), style="dep")
