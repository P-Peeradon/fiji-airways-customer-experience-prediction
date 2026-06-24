# Synthetic Data Generation: Process and Rationale

To accurately answer the marketing team's questions without access to internal systems, we must construct a highly realistic synthetic dataset. This document outlines the process of generating this data using Python and the rationale behind how it accurately reflects Fiji Airways' operations during the 2023-2024 timeframe.

---

## 1. The Generation Process

We will use a combination of Python libraries (such as `pandas`, `numpy`, and `Faker`) to procedurally generate interconnected datasets (`passengers`, `loyalty_members`, `flights`, and `feedback`).

### Step 1: Defining Real-World Operational Parameters
Before generating random numbers, we define strict rules based on Fiji Airways' actual 2023-2024 public network:
- **Hubs**: Nadi International (NAN) and Nausori/Suva (SUV).
- **Destinations**: 
  - *Short/Medium-haul*: Sydney (SYD), Brisbane (BNE), Auckland (AKL).
  - *Long-haul*: Los Angeles (LAX), San Francisco (SFO), Hong Kong (HKG), Tokyo Narita (NRT).
  - *Regional*: Port Vila (VLI), Nukuʻalofa (TBU).
- **Fleet Alignment**: Map specific aircraft to realistic routes (e.g., Airbus A350s for LAX/SYD, Boeing 737 MAX for AKL/BNE, ATR-72 for regional).

### Step 2: Generating Flight Schedules and Events
- **Timetables**: Generate a 2-year timeline (Jan 2023 - Dec 2024). Frequencies will mirror reality (e.g., daily flights to LAX, multiple daily flights to SYD).
- **Injecting Seasonality & Weather**: 
  - *Peak Tourist Season* (June–August, December): Higher passenger load factors (85-95%).
  - *Cyclone Season* (January–March): We will programmatically increase the probability of severe weather delays and cancellations during these months.
- **Delay Simulation**: Use probability distributions (e.g., Poisson or log-normal) to simulate realistic delay minutes. 80% of flights will be on time (<15 min delay), while the "long tail" represents severe delays.

### Step 3: Simulating the Passenger and CRM Data
- **Demographics**: Use `Faker` to generate realistic names, emails, and ages.
- **Loyalty Assignment**: Assign membership tiers based on industry standard distributions:
  - 70% Non-members
  - 20% Base Tabua Club / Entry Oneworld
  - 10% Elite (Tabua Club Plus / Oneworld Sapphire/Emerald)
- **Booking Behavior**: Elite members will be algorithmically forced to have a higher frequency of flights (e.g., 4-10 flights/year) compared to non-members (1-2 flights/year).

### Step 4: Deterministic Feedback Generation
Feedback cannot be purely random; it must be *causally linked* to the flight data to allow for meaningful data science later.
- **The Delay Penalty**: If a generated flight has a delay > 60 minutes, the algorithm will automatically reduce the `csat_score` and `nps_score` for passengers on that flight.
- **The Fleet Bonus**: Passengers assigned to the modern Airbus A350 fleet will have slightly higher baseline ratings for `seat_rating` and `IFE_rating` compared to older aircraft.
- **The Class Divide**: Business class passengers will have a tighter, higher distribution of food/crew ratings compared to Economy passengers.

---

## 2. Rationale: Why this simulates 2023-2024 Fiji Airways

Creating data using this rule-based approach ensures the dataset is not just "random noise" but a statistically sound digital twin of the airline's recent operations. 

Here is why it effectively mirrors the 2023-2024 period:

### A. Post-Pandemic Travel Surge & Capacity
2023-2024 represents a massive resurgence in tourism to Fiji. By setting baseline load factors high (especially from Australian and US markets), the dataset will accurately reflect the stress on operations (baggage handling, gate crowding) that occurs during peak recovery years. 

### B. Fleet Modernization & Seating Comfort (The A350 Effect)
While Fleet Management is fundamentally separate from Customer Management, the type of aircraft has a direct and measurable correlation to Customer Satisfaction, specifically regarding aircraft seating and amenities. During 2023-2024, Fiji Airways heavily utilized their new Airbus A350-900 XWBs, which feature modern interiors, enhanced seating comfort, and superior In-Flight Entertainment (IFE). By explicitly coding a positive bias into the `seat_rating` and `IFE_rating` for A350 routes, our data will organically show this correlation when we analyze On-Board Service, exactly as the Marketing Team would observe in real surveys.

### C. Oneworld Alliance Integration
In 2024, Fiji Airways announced its transition to a full Oneworld member. The 2023-2024 data needs to reflect growing Oneworld elite passenger traffic. By structuring the `loyalty_tier` to include Oneworld status and giving these passengers higher expectations (e.g., higher sensitivity to priority boarding failures), we can simulate the changing demographic of the airline's premium cabin.

### D. Skytrax Awards Validation
Fiji Airways won "Best Airline in Australia and the Pacific" at the 2023 and 2024 Skytrax awards. Therefore, our baseline parameters for crew friendliness and overall CSAT must be skewed positively (e.g., a mean score of 4.2 out of 5) rather than a neutral 3.0. The data science challenge will be finding the *exceptions* (the specific routes or delay events) that dip below this high baseline.

---

## 3. Data Scoping Strategy: Real vs. Synthetic Boundaries

To ensure the project remains highly credible and grounded for the Marketing Team, we must strictly define the boundaries of our hybrid data approach. **Real data must be used wherever it is publicly verifiable and applicable.**

### Where REAL Data is Mandatory (To Ground the Project)
1. **Unstructured Passenger Feedback**: Synthetic text generators (like LLMs) fail to capture genuine human nuance, emotional variance, and regional slang. Therefore, the entire text corpus for our NLP pipeline *must* be real data scraped from SkyTrax, Reddit, and forums.
2. **The Route Network & Timetables**: We will not invent fake routes. The baseline for the `flights` table will be grounded using real Fiji Airways public schedules (e.g., mapping actual flight numbers like FJ910 to Sydney).
3. **Fleet Composition**: The aircraft assignments in our data will perfectly mirror Fiji Airways' real public fleet (Airbus A350s, A330s, Boeing 737 MAX, and ATR-72s).
4. **Macro-Events (Weather/Disruptions)**: We will anchor our generated flight delays to real-world historical events. For example, if a real cyclone affected Nadi in early 2023, our generated data will algorithmically spike with flight delays and ground service complaints on those exact dates.

### Where SYNTHETIC Data is Necessary
1. **Passenger Identity (PII) & CRM Profiles**: Due to strict data privacy laws (like GDPR), real customer names, emails, and Tabua Club point balances are completely inaccessible. These *must* be safely synthesized using libraries like `Faker`.
2. **Internal CSAT/NPS Integers**: While we have real text reviews, internal 0-5 post-flight surveys are proprietary. We will synthesize these integer scores, but we will mathematically anchor them to the sentiment scores derived from the real external text.
3. **Micro-Operational Metrics**: The exact minutes of delay for every single flight, or internal gate allocations at Suva, are private. We will synthesize these using statistical probability distributions (e.g., Poisson distributions) tied to global aviation industry averages.
