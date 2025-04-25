import re
import spacy
from typing import Dict, Any, List
from langdetect import detect
from deep_translator import GoogleTranslator

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def mask_pii(text: str) -> Dict[str, Any]:
    """
    Enhanced PII masking with JSON output format
    """
    lang = detect(text)
    if lang == 'en':
            #return text
            masked_text = text
    else:
            # Translate to English
            translated = GoogleTranslator(source=lang, target='en').translate(text)
            masked_text = translated
    entities = []
    
    def mask_and_record(pattern, label, group=0):
        nonlocal masked_text, entities
        for match in reversed(list(re.finditer(pattern, masked_text))):
            start, end = match.span(group)
            original = match.group(group)
            
            # Skip if already masked or overlaps
            if any(e['position'][0] <= start < e['position'][1] for e in entities):
                continue
            
            masked_text = masked_text[:start] + f"[{label}]" + masked_text[end:]
            entities.append({
                "position": [start, end],
                "classification": label,
                "entity": original
            })

    # Specific patterns first
    mask_and_record(r'\b(\d{4}[ -]?\d{4}[ -]?\d{4})\b', 'aadhar_num')
    mask_and_record(r'\b((?:\d[ -]*?){15,18}\d)\b', 'credit_debit_no')
    mask_and_record(r'(?:CVV|CVC|Security Code)[: ]*(\d{3,4})\b', 'cvv_no', 1)
    mask_and_record(r'\b((0[1-9]|1[0-2])[/-](\d{2}|\d{4}))\b', 'expiry_no', 1)

    dob_patterns = [
        r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b',
        r'\b(\d{4}[/-]\d{1,2}[/-]\d{1,2})\b',
        r'\b((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4})\b'
    ]
    for pattern in dob_patterns:
        mask_and_record(pattern, 'dob', 1)

    mask_and_record(r'(\+?\d{1,3}[-.\s]?)?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}', 'phone_number')
    mask_and_record(r'(\b[\w.-]+@[\w.-]+\.\w+\b)', 'email')

    # spaCy for full names
    doc = nlp(masked_text)
    for ent in reversed(doc.ents):
        if ent.label_ == "PERSON":
            if any(e['position'][0] <= ent.start_char < e['position'][1] for e in entities):
                continue
            masked_text = masked_text[:ent.start_char] + "[full_name]" + masked_text[ent.end_char:]
            entities.append({
                "position": [ent.start_char, ent.end_char],
                "classification": "full_name",
                "entity": ent.text
            })

    # Optional: Set category based on simple rule or ML model
    category = "Problem"
    eng_mask = masked_text


    # if lang == 'en':
    #      masked_text = masked_text
    # else:
    #      masked_text = GoogleTranslator(source='en', target=lang).translate(masked_text)
    text2 = text
    for ent in entities:
        entity_value = ent['entity']
        classification = ent['classification']
        text = text.replace(entity_value, f"[{classification}]")
    masked_text = text
    return {
        "input_email_body": text2,
        "list_of_masked_entities": sorted(entities, key=lambda x: x["position"][0]),
        "masked_email": masked_text,
        "category_of_the_email": category,
        "English_masked": eng_mask

    }


text = "Subject: Unvorhergesehener Absturz der Datenanalyse-Plattform\n\nDie Datenanalyse-Plattform brach unerwartet ab, da die Speicheroberfläche zu gering war My name is Sophia Rossi.. Ich habe versucht, Laravel 8 und meinen MacBook Pro neu zu starten, aber das Problem behält sich bei. Ich benötige Ihre Unterstützung, um diesen Fehler zu beheben. You can reach me at janesmith@company.com."
print(mask_pii(text))