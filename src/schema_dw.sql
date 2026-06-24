-- Analytical Data Warehouse - Star Schema
CREATE DATABASE IF NOT EXISTS FijiAirways_DW;
USE FijiAirways_DW;

-- Dimensions
CREATE TABLE dim_passenger (
    passenger_key INT AUTO_INCREMENT PRIMARY KEY,
    passenger_id VARCHAR(50),
    age_group VARCHAR(20),
    gender VARCHAR(20),
    nationality VARCHAR(50),
    language_preference VARCHAR(10),
    travel_persona VARCHAR(50)
);

CREATE TABLE dim_flight (
    flight_key INT AUTO_INCREMENT PRIMARY KEY,
    flight_id VARCHAR(50),
    flight_number VARCHAR(20),
    route VARCHAR(20),
    aircraft_type VARCHAR(50)
);

CREATE TABLE dim_loyalty (
    loyalty_key INT AUTO_INCREMENT PRIMARY KEY,
    loyalty_id VARCHAR(50),
    tier_level VARCHAR(50),
    status VARCHAR(20)
);

CREATE TABLE dim_date (
    date_key INT PRIMARY KEY, -- format YYYYMMDD
    full_date DATE,
    year INT,
    month INT,
    day INT,
    quarter INT
);

-- Fact Table
CREATE TABLE fact_feedback (
    fact_id INT AUTO_INCREMENT PRIMARY KEY,
    passenger_key INT,
    flight_key INT,
    date_key INT,
    loyalty_key INT,
    csat_score INT,
    nps_score INT,
    delay_minutes INT,
    crew_rating INT,
    food_rating INT,
    seat_rating INT,
    ground_service_rating INT,
    sentiment_score DECIMAL(5,2),
    is_purple_cow BOOLEAN,
    FOREIGN KEY (passenger_key) REFERENCES dim_passenger(passenger_key),
    FOREIGN KEY (flight_key) REFERENCES dim_flight(flight_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (loyalty_key) REFERENCES dim_loyalty(loyalty_key)
);
