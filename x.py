import spacy

# Directly load the model from the path if not recognized by the package
nlp = spacy.load("en_core_web_sm")
print(nlp("My name is Elon Musk and I work at SpaceX.").ents)