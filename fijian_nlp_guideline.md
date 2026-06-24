# Fijian Language NLP Guideline

Fijian (iTaukei) is an Austronesian language. Because it is considered a "low-resource" language—meaning standard NLP libraries like SpaCy or NLTK do not have pre-trained models for it—we must build a custom, rules-based sentiment pipeline. 

This artifact outlines the fundamental grammatical and lexical rules of Fijian compared to English, and establishes the technical blueprint for processing Fijian text in our Data Science project.

---

## 1. Orthography and the Writing System

Fijian uses the standard Latin alphabet, but several consonants have unique phonetic assignments that differ wildly from English. 

*   **b** is pronounced like `mb` (*bula* = mboo-la)
*   **c** is pronounced like `th` (*cagi* = tha-ngi)
*   **d** is pronounced like `nd` (*Nadi* = Nahn-di)
*   **g** is pronounced like `ng` in "singer" (*sega* = seng-ah)
*   **q** is pronounced like `ng` in "finger" (*yaqona* = yang-go-nah)

### NLP Implication: Text Normalization
Because tourists and non-native speakers (such as Australian or US passengers) often spell Fijian words phonetically in reviews (e.g., writing "Nandi" instead of "Nadi" or "Mamanutha" instead of "Mamanuca"), our NLP pipeline must include a **Normalization Dictionary** that uses Regex to map phonetic misspellings back to standard Fijian orthography before tokenization.

---

## 2. Basic Grammar: Fijian vs. English

### Word Order
*   **English**: Subject-Verb-Object (SVO). *Example: "The food is good."*
*   **Fijian**: Verb-Object-Subject (VOS) or Verb-Subject-Object (VSO). The verb or adjective typically leads the sentence.
    *   *Example: "E vinaka na kakana."* (Literally: "Is good the food").

### Pronouns and Number
*   **English**: Singular (I, you) and Plural (we, they).
*   **Fijian**: Highly complex. It distinguishes between Singular, Dual (two people), Paucal (a few people), and Plural (many). It also separates *inclusive* "we" (you and me) from *exclusive* "we" (me and someone else, but not you).

### NLP Implication: Stopword Generation
Because Fijian grammar relies heavily on tiny marker particles (to denote tense, possession, and articles) rather than English-style sentence structures, our custom **Stopword List** must aggressively filter these out so the algorithm can focus on the sentiment-bearing adjectives.
*   *Common particles to filter*: `na` (the), `e` (is/subject marker), `sa` (aspect marker), `i`, `o`, `kei` (and).

---

## 3. Lexical System for Sentiment Analysis

Since we cannot rely on a neural network to "understand" the context of Fijian sentences automatically, we will construct a **Sentiment Lexicon**—a dictionary that assigns mathematical polarity scores to specific Fijian words.

### Positive Lexicon Targets (+1.0)
*   `vinaka` (good, well, thank you)
*   `totoka` (beautiful, excellent - often used for destinations or lounges)
*   `marau` (happy, glad)
*   `loloma` (love, kindness - highly relevant for rating Cabin Crew friendliness)
*   `kaukauwa` (strong/reliable)

### Negative Lexicon Targets (-1.0)
*   `ca` (bad)
*   `berabera` (slow/delayed - highly relevant for Ground Service and flight delays)
*   `duka` (dirty - relevant for seating/cabin cleanliness)
*   `leqa` (problem/trouble)

---

## 4. The Critical Rule: Handling Negation

In English NLP, catching the word "not" before an adjective is crucial (e.g., "not good" = negative). 

In Fijian, negation is handled by the words `sega` (no/not) or the phrase `sega ni`.
*   *vinaka* = Good (+1)
*   *sega ni vinaka* = Not good (-1)

### NLP Implication: Bi-gram Tokenization
If we only use single-word tokenization (uni-grams), the algorithm will see "sega", "ni", and "vinaka", and might accidentally score the sentence as positive because it sees "vinaka". 
Therefore, our Fijian text processing pipeline MUST utilize **Bi-gram and Tri-gram tokenization** to actively scan for the `sega ni [word]` pattern. When this pattern is detected, the pipeline will multiply the polarity of the target word by `-1`.

---

## 5. Core NLP Preprocessing: Stopwords, Stemming, and Lemmatization

When preprocessing Fijian text for algorithmic analysis, standard English NLP concepts behave uniquely due to the language's morphological structure.

### Stopwords
Stopwords are highly frequent words that carry little independent semantic meaning (like "the", "is", "at" in English).
*   **Fijian Context**: Fijian relies heavily on particles to indicate tense, possession, and subjects.
*   **Action**: We must aggressively filter out words like *na* (the), *e* (predicate marker), *sa* (aspect marker), *i*, *o*, and *kei* (and). If we do not filter these, frequency-based models (like TF-IDF) will be overwhelmed by grammatical noise rather than sentiment-bearing adjectives.

### Stemming
Stemming is the process of chopping off word endings to reduce a word to its base form (e.g., "running" to "run").
*   **Fijian Context**: Fijian is an agglutinative language, meaning it builds words by adding prefixes and suffixes to root words. For example, *vaka* (a causative prefix) + *marau* (happy) = *vakamarau* (to make happy). 
*   **Action**: Simple suffix-stripping (like the Porter Stemmer in English) fails completely in Fijian because it relies heavily on prefixes and circumfixes. Developing a rules-based affix-stripper specifically for the *vaka-* prefix and nominalizing suffixes is necessary if strict stemming is required.

### Lemmatization
Lemmatization maps a word back to its dictionary root (lemma) using vocabulary and morphological analysis (e.g., "better" to "good").
*   **Fijian Context**: Lemmatization is significantly more effective than stemming for Fijian because it can handle **reduplication** (a common feature where words are repeated for emphasis or pluralization, e.g., *lako* = go, *lakolako* = journey).
*   **Action**: Since popular libraries like SpaCy and NLTK lack Fijian lemmatizers, our custom pipeline relies on mapping reduplicated words and prefixed variants back to their root lexicon targets (e.g., mapping *vakamarautaka* back to the sentiment root *marau*).

---
## Summary of the Fijian NLP Pipeline Execution
1.  **Normalization Layer**: Convert phonetic tourist spellings to proper iTaukei spelling.
2.  **Stopword Filter**: Strip grammatical particles (`na`, `e`, `sa`).
3.  **N-Gram Generation**: Split the sentence into chunks of 1, 2, and 3 words to preserve context.
4.  **Negation Check**: Scan for `sega ni` to flip mathematical polarities.
5.  **Lexicon Scoring**: Sum the values of the remaining words using the Custom Sentiment Dictionary to output a final score for the Marketing Team's CSAT metrics.
