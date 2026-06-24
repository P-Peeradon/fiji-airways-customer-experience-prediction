# Fiji Airways Customer Experience Analytics

## Project Overview
This Data Science project acts as an advanced, end-to-end analytical pipeline designed for the Fiji Airways Corporate Marketing Team. The core objective is to analyze customer experience and sentiment across four operational domains (Flight Destination, On-Board Service, Loyalty Program, and Ground Service) to identify the airline's **"Purple Cow"**—the remarkable service differentiator that drives passenger loyalty.

To ensure strict data privacy and security compliance, this project leverages a **Hybrid Synthetic Methodology**. Internal operational data (passenger demographics, flight schedules, CRM) is synthetically generated to mimic real-world distributions, while text-based NLP processing is modeled against realistic multilingual passenger reviews.

## What Has Been Completed (Up to Phase 4)

### 1. Requirements & Architecture Design
*   Defined 20 specific, actionable business questions mapped to the four operational domains.
*   Designed a **3NF Operational Database (ODB)** schema to simulate transactional systems.
*   Designed a **Dimensional Star Schema Data Warehouse (DW)** optimized for Business Intelligence dashboards (Tableau/PowerBI).

### 2. Synthetic Data Generation
*   Generated robust operational datasets (`passengers.csv`, `flights.csv`, `loyalty_members.csv`, `internal_feedback.csv`).
*   Enforced specific demographic binning (e.g., Age Groups 16-22, 23-30) and isolated Key Markets (Australia, Fiji, New Zealand, USA, Singapore, Japan, Hong Kong) from the "Rest of Pacific".
*   Programmed deterministic feedback triggers (e.g., A350 fleet inflates seat ratings; delays over 60 minutes decrease ground service ratings).

### 3. Multilingual NLP Pipeline & Privacy Filtering
*   Built a synthetic external data scraper mocking reviews from SkyTrax and Reddit, strictly adhering to a **6:3:1 language ratio** (English : Fijian : Hindi).
*   **Cybersecurity Compliance:** Engineered an automated NLP Privacy Filter using Regex and SpaCy NER to detect and redact sensitive Personally Identifiable Information (PII) including PNRs, emails, names, and phone numbers *before* text ingestion.
*   Implemented a multilingual Sentiment Analyzer applying VADER for English and custom lexicon routing for Fijian and Hindi.

### 4. Sociological & Cultural Data Tuning
*   Documented extensive guidelines on Fijian NLP constraints, adapting algorithmic preprocessing for Fijian word structures (e.g., VOS grammar, reduplication in lemmatization, and prefix-heavy stemming failures).
*   Accounted for sociological impacts on data science, such as "Fiji Time" and indirect communication patterns compared to high-efficiency hubs like Singapore.

### 5. ETL Pipeline & Data Warehousing
*   Executed an automated Python ETL script (`src/etl_pipeline.py`) that successfully extracts the raw operational data, transforms it, and loads it into polished Dimensional and Fact tables (`dim_passenger`, `dim_flight`, `dim_loyalty`, `fact_feedback`) in the `data/processed/warehouse/` directory.

### 6. Git Workflow Automation
*   Configured local repository security with a robust `.git/hooks/pre-commit` hook that blocks direct commits to the `main` branch and enforces that all feature branches must pull `origin main` before saving code.

## Academic Alignment
This project serves as a practical capstone, synthesizing learning outcomes from two core University of Melbourne Master's units:
*   **ISYS90049 (Digital Business Analysis):** Exhibited through stakeholder requirements elicitation, socio-technical process modeling, and strategic information systems design.
*   **ISYS90056 (Cybersecurity Management):** Exhibited through strict data governance, synthetic data risk mitigation, and proactive GDPR/PII compliance filtering.