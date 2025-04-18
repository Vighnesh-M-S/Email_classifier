import spacy
import re

nlp = spacy.load("en_core_web_sm")

def mask_pii(text):
    doc = nlp(text)
    masked = text
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'ORG', 'GPE', 'DATE', 'EMAIL', 'PHONE']:
            masked = masked.replace(ent.text, f"{{{{{ent.label_}}}}}")
    return masked


text = "Seeking information on digital strategies that can aid in brand growth and details on the available services. Looking forward to learning more to help our business grow My name is Elena Ivanova.. Thank you, and I look forward to hearing from you soon. You can reach me at fatima.farsi@help.com."

print(mask_pii(text))