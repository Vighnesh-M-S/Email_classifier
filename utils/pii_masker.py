# import spacy
import re

def mask_pii(text):
    
    text = re.sub(r'\b[\w.-]+?@\w+?\.\w+?\b', '{{EMAIL}}', text)
    phone_pattern = re.compile(
        r'(\+?\d{1,3}[-\s]?)?(\(?\d{1,4}\)?[-\s]?)\d{3,4}[-\s]?\d{4}'
    )
    text = phone_pattern.sub('{{PHONE}}', text)

    # doc = nlp(text)
    # masked_text = text
    
    # for ent in doc.ents:
    #     if ent.label_ in ['PERSON', 'ORG', 'GPE', 'DATE', 'Email', ]:
    #         if not re.match(r'\{\{.*?\}\}', ent.text):
    #             masked_text = masked_text.replace(ent.text, f"{{{{{ent.label_}}}}}")


    return (text)


