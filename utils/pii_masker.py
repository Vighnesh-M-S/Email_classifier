import spacy
import re

nlp = spacy.load("xx_ent_wiki_sm")

def mask_pii(text):
    doc = nlp(text)
    masked_text = text
    
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'ORG', 'GPE', 'DATE', 'Email', ]:
            masked_text = masked_text.replace(ent.text, f"{{{{{ent.label_}}}}}")

    masked_text = re.sub(r'\b[\w.-]+?@\w+?\.\w+?\b', '{{EMAIL}}', masked_text)
    phone_pattern = re.compile(
        r'(\+?\d{1,3}[-\s]?)?(\(?\d{1,4}\)?[-\s]?)\d{3,4}[-\s]?\d{4}'
    )
    text = phone_pattern.sub('{{PHONE}}', masked_text)
    return (text)
# test the function


text = '''Subject: Änderungsantrag zur Abrechnungsstruktur

Sehr geehrter Kundenservice, 

ich schreibe, um eine Änderung in der Abrechnungsstruktur für den AWS-Management-Service anzufordern, wobei meine Kontonummer <acc_num> ist. Da wir derzeit einen Anstieg der Nutzung während unserer Bereitstellungsphasen erleben, benötigen wir ein Abrechnungsmodell, das diese erweiterte Nutzung besser berücksichtigen kann My name is Sophia Rossi.. Derzeit haben unsere Kosten die üblichen Grenzen überschritten, was sich erheblich auf unser Budget auswirkt. 

Für alle notwendigen Diskussionen oder Klarstellungen kontaktieren Sie mich bitte unter <tel_num> oder per E-Mail an <email>. Ich freue mich auf Ihre Unterstützung bei der Anpassung unseres Vertrags, um unseren spezifischen Anforderungen während dieser intensiven Bereitstellungsphasen gerecht zu werden.

Vielen Dank.

Mit freundlichen Grüßen,
<name> You can reach me at fatima.farsi@help.com.'''

x = mask_pii(text)
print(x)
  # prints the count of each type of PII