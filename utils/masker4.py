import pandas as pd
import re
import spacy
from tqdm import tqdm

# Load spaCy model
nlp = spacy.load("en_core_web_lg")

def mask_email_content(email: str) -> str:
    """
    Mask PII in email content with simplified tags
    Returns only the masked text without entity tracking
    """
    masked_text = email
    
    # Processing order matters - most specific patterns first
    patterns = [
        (r'\b(\d{4}[ -]?\d{4}[ -]?\d{4})\b', '[aadhar_num]'),          # Aadhar numbers
        (r'\b((?:\d[ -]*?){15,18}\d)\b', '[credit_debit_no]'),         # Card numbers
        (r'(?:CVV|CVC|Security Code)[: ]*(\d{3,4})\b', '[cvv_no]'),    # CVV codes
        (r'\b((0[1-9]|1[0-2])[/-](\d{2}|\d{4}))\b', '[expiry_no]'),    # Expiry dates
        (r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b', '[dob]'),             # Dates DD/MM/YYYY
        (r'\b(\d{4}[/-]\d{1,2}[/-]\d{1,2})\b', '[dob]'),               # Dates YYYY/MM/DD
        (r'(\+?\d{1,3}[-.\s]?)?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}', '[phone_number]'),  # Phones
        (r'(\b[\w.-]+@[\w.-]+\.\w+\b)', '[email]'),                    # Emails
    ]
    
    # Apply all regex patterns
    for pattern, replacement in reversed(patterns):
        masked_text = re.sub(pattern, replacement, masked_text)
    
    # Handle names with spaCy (process after regex)
    doc = nlp(masked_text)
    for ent in reversed(doc.ents):
        if ent.label_ == "PERSON":
            masked_text = masked_text[:ent.start_char] + "[full_name]" + masked_text[ent.end_char:]
    
    return masked_text

def process_csv(input_path: str, output_path: str):
    """
    Process CSV file and create new one with masked emails
    """
    # Read input CSV
    df = pd.read_csv(input_path)
    
    # Verify required columns
    if 'email' not in df.columns or 'type' not in df.columns:
        raise ValueError("Input CSV must contain 'email' and 'type' columns")
    
    # Process emails with progress bar
    tqdm.pandas(desc="Masking emails")
    df['masked_email'] = df['email'].progress_apply(mask_email_content)
    
    # Create output dataframe with just masked emails and types
    output_df = df[['masked_email', 'type']]
    
    # Save to new CSV
    output_df.to_csv(output_path, index=False)
    print(f"\nSuccessfully created masked file at: {output_path}")
    print(f"Processed {len(df)} emails")

# Example usage
if __name__ == "__main__":
    input_csv = "/Users/vighneshms/Downloads/Email_classifier/models/combined_output3.csv"  # Replace with your input file
    output_csv = "/Users/vighneshms/Downloads/Email_classifier/models/masked_emails_with_types.csv"  # Output file
    
    process_csv(input_csv, output_csv)