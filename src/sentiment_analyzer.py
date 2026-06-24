import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
import re

analyzer = SentimentIntensityAnalyzer()

# Fijian Lexicon (from Artifact 4)
fijian_positive = ['vinaka', 'totoka', 'marau', 'loloma', 'kaukauwa', 'bulabula']
fijian_negative = ['ca', 'berabera', 'duka', 'leqa']

def analyze_fijian(text):
    text = str(text).lower()
    score = 0
    words = text.split()
    
    for i, word in enumerate(words):
        # Handle Negation (sega ni)
        is_negated = False
        if i > 1 and words[i-2] == 'sega' and words[i-1] == 'ni':
            is_negated = True
            
        word_clean = re.sub(r'[^\w\s]', '', word)
        
        if word_clean in fijian_positive:
            score += -1 if is_negated else 1
        elif word_clean in fijian_negative:
            score += 1 if is_negated else -1
            
    # Normalize score between -1 and 1
    if score > 0: return min(score * 0.33, 1.0)
    elif score < 0: return max(score * 0.33, -1.0)
    return 0.0

def analyze_hindi(text):
    # Dummy Hindi Lexicon for synthetic data demonstration
    hi_positive = ['अच्छा', 'सुंदर', 'धन्यवाद']
    hi_negative = ['खराब', 'देरी', 'समस्या']
    score = 0
    for word in hi_positive:
        if word in str(text): score += 1
    for word in hi_negative:
        if word in str(text): score -= 1
        
    if score > 0: return 0.8
    if score < 0: return -0.8
    return 0.0

def calculate_sentiment(row):
    lang = row['language_detected']
    text = str(row['masked_comment'])
    
    if lang == 'EN':
        # Use VADER for English
        return analyzer.polarity_scores(text)['compound']
    elif lang == 'FJ':
        return analyze_fijian(text)
    elif lang == 'HI':
        return analyze_hindi(text)
    return 0.0

if __name__ == "__main__":
    input_file = os.path.join(os.path.dirname(__file__), '../data/processed/clean_external_reviews.csv')
    output_file = os.path.join(os.path.dirname(__file__), '../data/processed/sentiment_scored_reviews.csv')
    
    print("Running Multilingual Sentiment Analysis...")
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Run privacy_filter.py first.")
        exit(1)
        
    df = pd.read_csv(input_file)
    df['sentiment_score'] = df.apply(calculate_sentiment, axis=1)
    
    # Map score back to CSAT 0-5 scale for analytical alignment
    # VADER is -1 to 1. So map (-1 to 1) -> (0 to 5)
    df['inferred_csat'] = ((df['sentiment_score'] + 1) / 2) * 5
    df['inferred_csat'] = df['inferred_csat'].round().astype(int)
    
    df.to_csv(output_file, index=False)
    print("Sentiment Analysis complete. Output saved to data/processed/sentiment_scored_reviews.csv")
