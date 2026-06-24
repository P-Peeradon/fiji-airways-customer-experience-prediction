import pandas as pd
import numpy as np
from faker import Faker
import random
import uuid
from datetime import datetime, timedelta
import os

# Initialize Faker and seed for reproducibility
fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

NUM_PASSENGERS = 5000
NUM_FLIGHTS = 1000

def generate_passengers():
    print("Generating Passengers...")
    passengers = []
    
    age_bins = ['16-22', '23-30', '31-45', '46-60', '61+']
    genders = ['M', 'F', 'Non-Binary']
    nationalities = ['Australia', 'Fiji', 'New Zealand', 'USA', 'Singapore', 'Japan', 'Hong Kong', 'Rest of Pacific', 'Other']
    nat_weights = [0.35, 0.20, 0.15, 0.10, 0.05, 0.05, 0.03, 0.05, 0.02]
    
    languages = ['EN', 'FJ', 'HI']
    lang_weights = [0.6, 0.3, 0.1]  # 6:3:1 ratio
    
    personas = ['Leisure', 'Business', 'VFR']
    
    for _ in range(NUM_PASSENGERS):
        p_id = str(uuid.uuid4())
        passengers.append({
            'passenger_id': p_id,
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'join_date': fake.date_between(start_date='-5y', end_date='today'),
            'age_group': random.choice(age_bins),
            'gender': np.random.choice(genders, p=[0.48, 0.48, 0.04]),
            'nationality': np.random.choice(nationalities, p=nat_weights),
            'language_preference': np.random.choice(languages, p=lang_weights),
            'travel_persona': np.random.choice(personas, p=[0.5, 0.2, 0.3])
        })
    return pd.DataFrame(passengers)

def generate_loyalty(passengers_df):
    print("Generating Loyalty Members...")
    loyalty = []
    tiers = ['None', 'Tabua Club / Oneworld Ruby', 'Elite (Tabua Plus / Oneworld Sapphire/Emerald)']
    tier_weights = [0.70, 0.20, 0.10]
    
    for _, row in passengers_df.iterrows():
        tier = np.random.choice(tiers, p=tier_weights)
        if tier != 'None':
            loyalty.append({
                'loyalty_id': 'TC-' + str(random.randint(100000, 999999)),
                'passenger_id': row['passenger_id'],
                'tier_level': tier,
                'points_balance': random.randint(1000, 500000),
                'status': 'Active'
            })
    return pd.DataFrame(loyalty)

def generate_flights():
    print("Generating Flights...")
    flights = []
    
    routes = [
        ('NAN', 'SYD', 'A350'), ('NAN', 'AKL', '737 MAX'), ('NAN', 'LAX', 'A350'),
        ('NAN', 'SFO', 'A350'), ('NAN', 'NRT', 'A330'), ('NAN', 'HKG', 'A330'),
        ('NAN', 'SIN', 'A330'), ('SUV', 'SYD', '737 MAX'), ('NAN', 'VLI', 'ATR-72'),
        ('NAN', 'TBU', 'ATR-72')
    ]
    
    start_date = datetime(2023, 1, 1)
    
    for i in range(NUM_FLIGHTS):
        route = random.choice(routes)
        # Random date in 2023-2024
        flight_date = start_date + timedelta(days=random.randint(0, 730))
        
        # Simulate delay using an exponential distribution (most delays are short, few are long)
        delay = int(np.random.exponential(scale=20))
        if delay < 5: delay = 0
        
        # Simulate cyclone season (Jan-March) higher delays
        if flight_date.month in [1, 2, 3] and random.random() < 0.1:
            delay += random.randint(60, 180)
            
        flights.append({
            'flight_id': f"FL-{1000+i}",
            'flight_number': f"FJ{random.randint(100, 999)}",
            'origin': route[0],
            'destination': route[1],
            'aircraft_type': route[2],
            'flight_date': flight_date.date(),
            'delay_minutes': delay
        })
    return pd.DataFrame(flights)

def generate_feedback(passengers_df, flights_df, loyalty_df):
    print("Generating Deterministic Feedback...")
    feedback = []
    
    # Let's say each flight has about 5-10 responses
    loyalty_dict = dict(zip(loyalty_df.passenger_id, loyalty_df.tier_level))
    
    for _, flight in flights_df.iterrows():
        num_responses = random.randint(5, 10)
        flight_passengers = passengers_df.sample(num_responses)
        
        delay = flight['delay_minutes']
        aircraft = flight['aircraft_type']
        
        for _, passenger in flight_passengers.iterrows():
            # Baseline Scores
            base_overall = np.random.normal(4.2, 0.8) # Generally positive baseline
            base_seat = np.random.normal(3.8, 1.0)
            base_crew = np.random.normal(4.5, 0.6) # Famous friendly crew
            base_ground = np.random.normal(3.5, 1.0)
            base_food = np.random.normal(3.8, 1.0)
            
            # Deterministic Modifiers
            if delay > 60:
                base_overall -= 1.5
                base_ground -= 1.0
            
            if aircraft == 'A350':
                base_seat += 0.8
                
            tier = loyalty_dict.get(passenger['passenger_id'], 'None')
            if 'Elite' in tier:
                base_overall += 0.5 # Better lounge access, priority, etc.
                
            # Bound and round scores between 0 and 5
            def bound_score(s): return int(max(0, min(5, round(s))))
            
            csat = bound_score(base_overall)
            
            # NPS (0-10) loosely correlated to CSAT
            nps_base = base_overall * 2
            nps = int(max(0, min(10, round(nps_base + np.random.normal(0, 1)))))
            
            feedback.append({
                'feedback_id': str(uuid.uuid4()),
                'passenger_id': passenger['passenger_id'],
                'flight_id': flight['flight_id'],
                'rating_overall': csat,
                'nps_score': nps,
                'rating_crew': bound_score(base_crew),
                'rating_food': bound_score(base_food),
                'rating_seat': bound_score(base_seat),
                'rating_ground': bound_score(base_ground),
                'submission_date': flight['flight_date'] + timedelta(days=random.randint(1, 5))
            })
            
    return pd.DataFrame(feedback)

if __name__ == "__main__":
    # Ensure raw directory exists
    os.makedirs(os.path.join(os.path.dirname(__file__), '../data/raw'), exist_ok=True)
    
    df_passengers = generate_passengers()
    df_passengers.to_csv(os.path.join(os.path.dirname(__file__), '../data/raw/passengers.csv'), index=False)
    
    df_loyalty = generate_loyalty(df_passengers)
    df_loyalty.to_csv(os.path.join(os.path.dirname(__file__), '../data/raw/loyalty_members.csv'), index=False)
    
    df_flights = generate_flights()
    df_flights.to_csv(os.path.join(os.path.dirname(__file__), '../data/raw/flights.csv'), index=False)
    
    df_feedback = generate_feedback(df_passengers, df_flights, df_loyalty)
    df_feedback.to_csv(os.path.join(os.path.dirname(__file__), '../data/raw/internal_feedback.csv'), index=False)
    
    print("Synthetic Operational Data Generation Complete. Files saved to data/raw/")
