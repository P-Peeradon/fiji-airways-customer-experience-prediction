# Fiji Airways Customer Experience Data Science Project Plan

This document outlines the structured plan to analyze customer experience across **four domains** for the Fiji Airways Marketing Team.

## 1. Five Questions per Domain

### Domain 1: Flight Destination
1. Which flight destinations consistently yield the highest and lowest overall customer satisfaction (CSAT) scores?
2. How do operational factors, such as flight delays and scheduling, impact customer sentiment for specific routes (e.g., Nadi to Sydney vs. Nadi to LAX)?
3. Are there distinct seasonal variations in customer experience ratings for our most popular destinations?
4. Which destinations generate the highest rate of operational complaints (e.g., baggage handling, gate experiences)?
5. How does the perceived "value for money" differ between short-haul regional flights (Pacific Islands) and long-haul international flights?

### Domain 2: On-Board Service
1. What is the prevailing sentiment regarding cabin crew helpfulness, friendliness, and professionalism based on passenger text feedback?
2. How do passengers rate the quality, variety, and cultural authenticity of in-flight meals and beverages?
3. What are the primary drivers of complaints regarding physical comfort, such as seating, legroom, and cabin cleanliness?
4. How does satisfaction with In-Flight Entertainment (IFE) differ between travel classes (Economy vs. Business)?
5. To what extent does the quality of on-board service correlate with the likelihood of a passenger recommending Fiji Airways (NPS)?

### Domain 3: Loyalty Program (Tabua Club / Oneworld)
1. Do Tabua Club and Oneworld elite members report significantly higher overall satisfaction compared to non-members?
2. Which specific loyalty perks (e.g., Premier Lounge access, priority boarding, extra baggage) are most frequently mentioned as value-adds by members?
3. What experiential factors contribute most to a member downgrading their tier status or churning entirely from the loyalty program?
4. How effectively are service failures or complaints resolved for elite members compared to standard passengers?
5. How does active participation in the loyalty program impact the frequency of repeat bookings and lifetime passenger value?

### Domain 4: Ground Service (Nadi & Suva Airports)
1. How do passengers rate the efficiency and friendliness of the check-in and baggage drop processes at Nadi (NAN) and Suva (SUV)?
2. What is the measurable impact of security and immigration wait times on a passenger's overall pre-flight customer satisfaction?
3. How do passengers perceive the quality, cleanliness, and availability of amenities in the boarding gate areas prior to departure?
4. Is there a significant difference in ground service satisfaction when comparing the primary international hub (Nadi) against the secondary hub (Suva)?
5. How effectively does the ground staff manage communication and passenger comfort during unforeseen flight delays or boarding disruptions?

---

## 2. Data Sources & External Pipeline

Since we are operating externally, we will use a **hybrid data generation approach**:

1. **Synthetic Operational & CRM Data**: We will write Python scripts to generate realistic datasets simulating internal systems (flight logs, passenger profiles, Tabua Club memberships).
2. **External Scraped Data**: We will augment our synthetic data by scraping real passenger reviews and feedback from **SkyTrax** and **Reddit** (`r/Flights`, `r/Fiji`, etc.). 

### External Data Processing (NLP & Privacy)
- **Data Masking (Privacy)**: Before any external text is analyzed or saved to the final dataset, we will implement rigorous Regex rules to mask Personally Identifiable Information (PII). This includes redacting passenger names, booking reference numbers (PNRs), phone numbers, and email addresses.
- **Multilingual Support (6:3:1 Ratio)**: To preserve the regional language of Fiji and practice advanced NLP/Regex, our text data will be distributed across three languages in a strict **60% English, 30% Fijian, and 10% Hindi** ratio. This 6:3:1 ratio will be applied consistently across both the scraped external data pool and the internally generated synthetic data. We will use language detection algorithms to route the text to the appropriate NLP processing pipeline.

---

## 3. Output Data Format

To ensure maximum compatibility with the Marketing Team's tools, the processed analytical datasets will be exported in both **`.csv`** and **`.xlsx` (Excel)** formats.

**Example Dataset Name**: `analytical_customer_experience_dataset.csv` / `.xlsx`
**Key Fields/Schema**:
- `passenger_id` (String/UUID): Unique identifier for the passenger.
- `flight_number` (String): e.g., "FJ910"
- `origin_code` / `destination_code` (String): e.g., "NAN", "SYD"
- `flight_date` (Date): Date of travel.
- `travel_class` (String): Economy, Business.
- `loyalty_tier` (String): None, Tabua Club, Oneworld Ruby/Sapphire/Emerald.
- `csat_score` (Integer 0-5): Overall satisfaction rating.
- `nps_score` (Integer 0-10): Net promoter score.
- `crew_rating`, `food_rating`, `seat_rating`, `ground_service_rating` (Integer 0-5): Sub-category ratings.
- `delay_minutes` (Integer): Actual arrival time minus scheduled arrival.
- `raw_feedback_text` (Text): The original review text from SkyTrax/Reddit.
- `masked_feedback_text` (Text): Review text with PII removed via Regex.
- `detected_language` (String): English, Fijian, or Hindi.
- `sentiment_label` (String): NLP-derived classification (Positive, Neutral, Negative).

**Reporting Strategy**: The raw data will be strictly on a 0-5 integer scale, but the final analytical reports will aggregate these scores into performance **"Bands"** to explicitly identify which specific service acts as a **"Purple Cow"** (a standout feature) that differentiates Fiji Airways.

---

## 4. Schema of MySQL ODB and Data Warehouse

### Operational Database (MySQL ODB)
- **`passengers`**: `passenger_id` (PK), `first_name`, `last_name`, `email`, `join_date`.
- **`loyalty_members`**: `loyalty_id` (PK), `passenger_id` (FK), `tier_level`, `points_balance`, `status`.
- **`flights`**: `flight_id` (PK), `flight_number`, `origin`, `destination`, `scheduled_departure`, `actual_departure`.
- **`feedback`**: `feedback_id` (PK), `passenger_id` (FK), `flight_id` (FK), `rating_overall`, `rating_crew`, `rating_food`, `rating_ground`, `raw_comments`, `masked_comments`, `language`, `submission_date`.

### Data Warehouse (Analytical)
- **Fact Table: `fact_customer_experience`**
  - Measures: `csat_score`, `nps_score`, `delay_minutes`, `crew_rating`, `food_rating`, `ground_service_rating`.
  - Foreign Keys: `passenger_key`, `flight_key`, `date_key`, `loyalty_key`, `destination_key`.
- **Dimension Tables**:
  - **`dim_passenger`**: `passenger_key`, `age_group` (Bins: 16-22, 23-30, 31-45, 46-60, 61+), `gender`, `nationality` (Key Markets: Australia, Fiji, New Zealand, USA, Singapore, Japan, Hong Kong; Rest of Pacific: Tonga, Tuvalu, Samoa, Palau, Solomon Islands, Marshall Islands, Kiribati, Papua New Guinea, Niue, Micronesia, Vanuatu, Nauru; all others binned as 'Other'), `language_preference` (EN, FJ, HI), `travel_persona` (Leisure, Business, VFR), `lifetime_value`.
  - **`dim_flight`**: `flight_key`, `flight_number`, `route`, `distance`, `aircraft_type`.
  - **`dim_destination`**: `destination_key`, `airport_code`, `city`, `country`, `region`.
  - **`dim_loyalty`**: `loyalty_key`, `program_name`, `tier_name`.
  - **`dim_date`**: `date_key`, `day`, `month`, `year`, `quarter`, `season`.

## User Review Required
> [!IMPORTANT]
> The external NLP pipeline (SkyTrax/Reddit sources, PII data masking, and multilingual support for English, Fijian, and Hindi) has been added to the plan! Let me know if everything looks correct.
