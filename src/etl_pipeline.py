import pandas as pd
import os

def run_etl():
    print("Running ETL Pipeline...")
    base_dir = os.path.dirname(__file__)
    
    # Load raw ODB tables
    passengers = pd.read_csv(os.path.join(base_dir, '../data/raw/passengers.csv'))
    flights = pd.read_csv(os.path.join(base_dir, '../data/raw/flights.csv'))
    loyalty = pd.read_csv(os.path.join(base_dir, '../data/raw/loyalty_members.csv'))
    feedback = pd.read_csv(os.path.join(base_dir, '../data/raw/internal_feedback.csv'))
    
    # Create Dimensions
    dim_passenger = passengers[['passenger_id', 'age_group', 'gender', 'nationality', 'language_preference', 'travel_persona']].copy()
    dim_flight = flights[['flight_id', 'flight_number', 'origin', 'destination', 'aircraft_type', 'delay_minutes']].copy()
    dim_flight['route'] = dim_flight['origin'] + '-' + dim_flight['destination']
    
    dim_loyalty = loyalty[['loyalty_id', 'passenger_id', 'tier_level', 'status']].copy()
    
    # Create Fact Table
    # Merge feedback with flight to get delay_minutes
    fact_table = feedback.merge(dim_flight[['flight_id', 'delay_minutes']], on='flight_id', how='left')
    
    # Calculate the "Purple Cow" (e.g., if crew_rating > 4 AND overall > 4)
    fact_table['is_purple_cow'] = ((fact_table['rating_crew'] >= 4) & (fact_table['rating_overall'] >= 4)).astype(int)
    
    # Save dimensions and facts to processed directory for BI consumption
    out_dir = os.path.join(base_dir, '../data/processed/warehouse')
    os.makedirs(out_dir, exist_ok=True)
    
    dim_passenger.to_csv(os.path.join(out_dir, 'dim_passenger.csv'), index=False)
    dim_flight.to_csv(os.path.join(out_dir, 'dim_flight.csv'), index=False)
    dim_loyalty.to_csv(os.path.join(out_dir, 'dim_loyalty.csv'), index=False)
    fact_table.to_csv(os.path.join(out_dir, 'fact_feedback.csv'), index=False)
    
    print("ETL Complete. Dimensional Warehouse CSVs ready in data/processed/warehouse/")

if __name__ == "__main__":
    run_etl()
