# Academic Alignment: University of Melbourne Core Units

This Fiji Airways Customer Experience Data Science Project is designed not just as a technical exercise, but as a comprehensive application of graduate-level Information Systems theory. 

This seventh artifact explicitly maps the project's methodologies and architectural decisions to the learning outcomes of two core master's units taught at the University of Melbourne: **ISYS90049 Digital Business Analysis** and **ISYS90056 Cybersecurity Management**.

---

## 1. Alignment with ISYS90049: Digital Business Analysis

ISYS90049 focuses on the methods and techniques used to identify business needs, model processes, analyze requirements, and design information systems that actively support business strategy.

**How this project demonstrates ISYS90049 Outcomes:**

*   **Requirements Elicitation & Domain Modeling:** Rather than immediately writing code, the project began with a rigorous requirements phase (Artifact 1). We clearly defined the stakeholder (the Corporate Marketing Team) and elicited 20 specific, actionable business questions across 4 distinct operational domains (Flight, On-Board, Loyalty, Ground Service).
*   **Systems Design & Architecture:** We architected a complete data pipeline, designing both a normalized Operational Database (3NF) to simulate transactional flow, and a Dimensional Data Warehouse (Star Schema) optimized for business intelligence and dashboarding.
*   **Strategic Business Alignment:** The system is explicitly designed to identify Fiji Airways' "Purple Cow" (competitive differentiator). By highly granulating the `dim_passenger` table (Age Bins, Key Markets vs. Rest of Pacific), the data structure directly empowers the Marketing Team to make strategic, segment-specific decisions.
*   **Socio-Technical Systems Analysis:** Artifacts 4, 5, and 6 (The Fijian NLP, Cultural, and Vocabulary Guidelines) demonstrate a deep understanding that Information Systems are socio-technical. The data models and NLP algorithms were specifically tuned to the cultural realities of the stakeholders (e.g., accounting for "Fiji Time" and indirect communication styles), rather than applying a rigid, one-size-fits-all technical solution.

---

## 2. Alignment with ISYS90056: Cybersecurity Management

ISYS90056 focuses on the managerial aspects of cybersecurity, including information governance, risk assessment, data privacy, and compliance within modern business contexts.

**How this project demonstrates ISYS90056 Outcomes:**

*   **Data Privacy & Compliance (PII Handling):** The most critical cybersecurity implementation in this project is the NLP Privacy Pipeline (Artifact 3). By proactively building Regex-driven data masking to redact Personally Identifiable Information (PII)—including Passenger Names, Booking References (PNRs), Emails, and Phone Numbers—*before* the external text enters the database, the system demonstrates strict compliance with global data protection principles (e.g., GDPR).
*   **Risk Mitigation via Data Generation:** The methodological decision (Artifact 2) to synthesize the Operational and CRM data rather than attempting to source real, proprietary customer data is a fundamental risk management strategy. It entirely neutralizes the risk of a data breach or legal violation while still enabling robust system testing.
*   **Data Governance & Pipeline Security:** The architecture strictly isolates the untrusted, unstructured "wild" data scraped from external sources (Reddit, SkyTrax) from the clean, structured Data Warehouse. This enforces a secure boundary, ensuring that raw external inputs are sanitized, classified by language, and stripped of sensitive data before they are allowed to influence the core business analytics.
