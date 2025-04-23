import spacy
import re
import json
from typing import List, Dict, Any

nlp = spacy.load("xx_ent_wiki_sm")

def mask_pii(email_body: str) -> Dict[str, Any]:
    """
    Mask PII in email body and return structured information about masked entities
    
    Args:
        email_body: The original email text
        
    Returns:
        Dictionary containing:
        - input_email_body
        - list_of_masked_entities
        - masked_email
    """
    # Initialize result structure
    result = {
        "input_email_body": email_body,
        "list_of_masked_entities": [],
        "masked_email": email_body
    }
    
    # Helper function to add masked entities
    def add_masked_entity(start: int, end: int, entity_type: str, original_text: str):
        nonlocal result
        # Check if this position is already masked
        for existing in result["list_of_masked_entities"]:
            if not (end <= existing["position"][0] or start >= existing["position"][1]):
                return  # Skip overlapping entities
        
        result["list_of_masked_entities"].append({
            "position": [start, end],
            "classification": entity_type,
            "entity": original_text
        })
    
    # Mask emails with regex
    email_matches = list(re.finditer(r'\b[\w.-]+?@\w+?\.\w+?\b', email_body))
    for match in reversed(email_matches):  # Process backwards to maintain positions
        start, end = match.span()
        original = match.group()
        result["masked_email"] = result["masked_email"][:start] + "{{EMAIL}}" + result["masked_email"][end:]
        add_masked_entity(start, end, "EMAIL", original)
    
    # Mask phone numbers with regex
    phone_pattern = re.compile(
        r'(\+?\d{1,3}[-\s]?)?(\(?\d{1,4}\)?[-\s]?)\d{3,4}[-\s]?\d{4}'
    )
    phone_matches = list(phone_pattern.finditer(email_body))
    for match in reversed(phone_matches):
        start, end = match.span()
        original = match.group()
        result["masked_email"] = result["masked_email"][:start] + "{{PHONE}}" + result["masked_email"][end:]
        add_masked_entity(start, end, "PHONE", original)
    
    # Process with spaCy for other entities (only on original unmasked portions)
    unmasked_portions = []
    last_end = 0
    for entity in sorted(result["list_of_masked_entities"], key=lambda x: x["position"][0]):
        start, end = entity["position"]
        if last_end < start:
            unmasked_portions.append((last_end, start))
        last_end = end
    if last_end < len(email_body):
        unmasked_portions.append((last_end, len(email_body)))
    
    for start, end in unmasked_portions:
        text_segment = email_body[start:end]
        doc = nlp(text_segment)
        for ent in reversed(doc.ents):
            if ent.label_ in ['PERSON', 'ORG', 'GPE', 'DATE']:
                entity_start = start + ent.start_char
                entity_end = start + ent.end_char
                original = ent.text
                mask_tag = f"{{{{{ent.label_}}}}}"
                result["masked_email"] = result["masked_email"][:entity_start] + mask_tag + result["masked_email"][entity_end:]
                add_masked_entity(entity_start, entity_end, ent.label_, original)
    
    # Sort entities by position for clean output
    result["list_of_masked_entities"].sort(key=lambda x: x["position"][0])
    
    return result

# Example usage
email_text = """Subject: Problem with Data Analytics Tools 

The data analytics tools are not functioning properly, which is hindering the optimization of investments. 
There have been instances of unexpected data loss and system crashes, which might be related to outdated software 
or hardware incompatibility issues. My contact number is +39-06-8899-1122 and email is john.doe@example.com, I,am working at Amazon."""

masked_result = mask_pii(email_text)
print(json.dumps(masked_result, indent=2))