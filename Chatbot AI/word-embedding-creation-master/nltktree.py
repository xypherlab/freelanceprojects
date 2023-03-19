import nltk 
from nltk import Tree
sentence = [("bayad", "payment"), ("clinic", "floor"), ("first year", "enrollment"), ("transferee", "enrollment"), ("magbayad","payment"), ("canteen", "floor"), ("DO", "floor"), ("registrar", "registrartime")]

pattern = """Payment Directory: {<payment>}
Enrollment Directory: {<enrollment>}
Floor Directory: {<floor>}
Registrar Schedule: {<registrartime>}"""
NPChunker = nltk.RegexpParser(pattern) 
result = NPChunker.parse(sentence)
Tree.fromstring(str(result)).pretty_print()