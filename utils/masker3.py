import re
import spacy
from typing import Dict, Any, List

# Load spaCy model
nlp = spacy.load("en_core_web_lg")

def mask_pii(text: str) -> Dict[str, Any]:
    """
    Enhanced PII masking with JSON output format
    """
    masked_text = text
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
    category = "sensitive_information"

    return {
        "input_email_body": text,
        "list_of_masked_entities": sorted(entities, key=lambda x: x["position"][0]),
        "masked_email": masked_text,
        "category_of_the_email": category
    }

# Example usage
sample = """
Hello, my name is John Doe, and my email is johndoe@example.com.
My phone is +1 (555) 123-4567, DOB: 01/01/1990.
Aadhar: 1234 5678 9012, Visa: 4111 1111 1111 1111 (exp 12/24, CVV: 123).
"""

import json
result = mask_pii(sample)
print(json.dumps(result, indent=2))
