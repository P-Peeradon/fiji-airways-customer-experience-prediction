# Multilingual NLP & Data Cleaning Pipeline

This document outlines the third core component of the project: the text processing pipeline. It details how raw, unstructured text (from both synthetic sources and scraped reviews) is cleaned using Regex and processed via Natural Language Processing (NLP) *before* it is ingested into the MySQL Operational Database (ODB).

---

## 1. Data Cleaning and Privacy Masking (Regex)
To ensure passenger privacy and data compliance, all text must pass through a strict Regex filtering layer before being stored as `masked_comments` in the database.

**Core Regex Masking Rules:**
*   **Booking References (PNR)**: Fiji Airways PNRs are typically 6-character alphanumeric strings.
    *   *Regex*: `\b[A-Z0-9]{6}\b`
    *   *Action*: Replace with `[PNR_REDACTED]`
*   **Email Addresses**:
    *   *Regex*: `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`
    *   *Action*: Replace with `[EMAIL_REDACTED]`
*   **Phone Numbers**: Capturing international and local Fiji formats.
    *   *Regex*: `(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}`
    *   *Action*: Replace with `[PHONE_REDACTED]`
*   **Passenger Names**: Using a combination of title-matching Regex (e.g., `(?:Mr\.|Mrs\.|Ms\.|Dr\.)\s[A-Z][a-z]+`) and Named Entity Recognition (NER) to substitute with `[NAME_REDACTED]`.

---

## 2. Language Detection & Routing
Before applying sentiment analysis, the text passes through a language classifier (e.g., `langdetect` or Facebook's `fasttext`). The classifier identifies the text, ensuring it aligns with our target **6:3:1 ratio**, and routes it to the correct NLP processing node.

---

## 3. The Multilingual NLP Strategy

### A. English Node (60% of Data)
*   **Preprocessing**: Standard tokenization, lemmatization, and stop-word removal using `spaCy` or `NLTK`.
*   **Sentiment Analysis**: We will utilize **VADER** (Valence Aware Dictionary and sEntiment Reasoner) which is highly tuned for social media and review texts, or a pre-trained transformer model (like DistilBERT) to output a definitive `Positive`, `Neutral`, or `Negative` sentiment label.

### B. Fijian Node (30% of Data)
*   **Challenge**: Fijian (iTaukei) is a low-resource language in traditional NLP libraries.
*   **Preprocessing**: We will build a custom tokenizer that respects Fijian orthography and curate a custom dictionary of common Fijian stopwords (e.g., *na, e, i, o, kei*).
*   **Sentiment Analysis**: We will implement a **Lexicon-based approach**. We will construct a custom dictionary mapping Fijian words to polarity scores.
    *   *Positive terms*: e.g., *vinaka* (good/thank you), *totoka* (beautiful), *marau* (happy).
    *   *Negative terms*: e.g., *ca* (bad), *berabera* (slow/delayed).

### C. Hindi / Fiji Hindi Node (10% of Data)
*   **Challenge**: Reviews may be written in standard Hindi (Devanagari script) or Fiji Hindi / Fiji Baat (often written in Romanized/Latin script).
*   **Preprocessing**: Utilizing the `iNLTK` (Natural Language Toolkit for Indic Languages) for Devanagari, and custom tokenizers for Romanized script.
*   **Sentiment Analysis**: 
    *   For standard Hindi, we will use a pre-trained multilingual transformer model (e.g., **XLM-RoBERTa**) capable of cross-lingual zero-shot transfer. 
    *   For Fiji Hindi slang, we will supplement the model with a custom dictionary to catch local nuances.

---

## 4. Ingestion into the Operational Database (ODB)
Once the pipeline has processed the raw review, it packages the structured results into a payload containing:
1.  `raw_comments` (The original scraped/synthetic text)
2.  `masked_comments` (The Regex-cleaned, privacy-safe text)
3.  `language` (The detected language flag: `en`, `fj`, or `hi`)
4.  `sentiment_label` (The final output of the NLP nodes)

This payload is then safely `INSERT`ed into the `feedback` table of the MySQL ODB, ready to answer our marketing questions!
