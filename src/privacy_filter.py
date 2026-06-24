import pandas as pd
import re
import spacy
import os

# Load SpaCy for Name Entity Recognition (NER)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spacy model...")
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def mask_pii(text):
    if not isinstance(text, str):
        return text
        
    # 1. Mask Emails
    text = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '[REDACTED EMAIL]', text)
    
    # 2. Mask Phone Numbers (simple international & local formats)
    text = re.sub(r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?[\d\-.\s]{7,10}', '[REDACTED PHONE]', text)
    
    # 3. Mask PNRs (6 uppercase alphanumeric characters, isolated)
    text = re.sub(r'\b[A-Z0-9]{6}\b', '[REDACTED PNR]', text)
    
    # 4. Mask Names using SpaCy NER
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            text = text.replace(ent.text, '[REDACTED NAME]')
            
    return text

if __name__ == "__main__":
    input_file = os.path.join(os.path.dirname(__file__), '../data/raw/external_reviews.csv')
    output_file = os.path.join(os.path.dirname(__file__), '../data/processed/clean_external_reviews.csv')
    
    print("Running NLP Privacy Filter Pipeline...")
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        exit(1)
        
    df = pd.read_csv(input_file)
    
    # Apply masking
    df['masked_comment'] = df['raw_comment'].apply(mask_pii)
    
    # Save processed data
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)
    print("PII Masking complete. Processed data saved to data/processed/clean_external_reviews.csv")
