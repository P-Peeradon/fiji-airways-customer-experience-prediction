import pandas as pd
import numpy as np
from faker import Faker
import random
import uuid
import os

fake_en = Faker('en_US')
fake_hi = Faker('hi_IN')

# Mock Fijian vocabulary for generating text
fj_words = ['bula', 'vinaka', 'waqavuka', 'berabera', 'sega', 'ni', 'ca', 'totoka', 'kakana', 'kerekere', 'pasese', 'Nadi', 'Suva', 'crew', 'flight', 'loloma', 'duka']

def generate_fijian_sentence():
    return " ".join(random.choices(fj_words, k=random.randint(5, 15))).capitalize() + "."

def generate_external_reviews(num_reviews=1000):
    print("Generating Synthetic External Reviews (SkyTrax/Reddit)...")
    reviews = []
    
    platforms = ['SkyTrax', 'Reddit', 'TripAdvisor']
    
    for _ in range(num_reviews):
        platform = random.choice(platforms)
        
        # Enforce the 6:3:1 Language Ratio (English:Fijian:Hindi)
        lang = np.random.choice(['EN', 'FJ', 'HI'], p=[0.6, 0.3, 0.1])
        
        if lang == 'EN':
            comment = fake_en.paragraph(nb_sentences=random.randint(2, 5))
        elif lang == 'HI':
            comment = fake_hi.paragraph(nb_sentences=random.randint(2, 4))
        else:
            comment = generate_fijian_sentence() + " " + generate_fijian_sentence()
            
        # 40% chance to maliciously inject PII to test the NLP Privacy Filter Pipeline
        if random.random() < 0.4:
            pii_type = random.choice(['email', 'phone', 'pnr', 'name'])
            if pii_type == 'email':
                comment += f" Contact me at {fake_en.email()}."
            elif pii_type == 'phone':
                comment += f" Call me: +679-{random.randint(1000000, 9999999)}."
            elif pii_type == 'pnr':
                # Aviation PNR is 6 alphanumeric characters
                pnr = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
                comment += f" My booking reference is {pnr}."
            elif pii_type == 'name':
                comment = f"Hi, I am {fake_en.name()}. " + comment
                
        reviews.append({
            'review_id': str(uuid.uuid4()),
            'source': platform,
            'language_detected': lang, # Simulating a language-detect pass
            'raw_comment': comment,
            'review_date': fake_en.date_between(start_date='-2y', end_date='today')
        })
        
    return pd.DataFrame(reviews)

if __name__ == "__main__":
    os.makedirs(os.path.join(os.path.dirname(__file__), '../data/raw'), exist_ok=True)
    df_reviews = generate_external_reviews()
    df_reviews.to_csv(os.path.join(os.path.dirname(__file__), '../data/raw/external_reviews.csv'), index=False)
    print("Synthetic External Reviews Generation Complete. Saved to data/raw/external_reviews.csv")
