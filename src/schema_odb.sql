-- Operational Database (ODB) Schema - 3NF
CREATE DATABASE IF NOT EXISTS FijiAirways_ODB;
USE FijiAirways_ODB;

CREATE TABLE Passengers (
    passenger_id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(150),
    join_date DATE,
    age_group VARCHAR(20),
    gender VARCHAR(20),
    nationality VARCHAR(50),
    language_preference VARCHAR(10),
    travel_persona VARCHAR(50)
);

CREATE TABLE LoyaltyMembers (
    loyalty_id VARCHAR(50) PRIMARY KEY,
    passenger_id VARCHAR(50),
    tier_level VARCHAR(50),
    points_balance INT,
    status VARCHAR(20),
    FOREIGN KEY (passenger_id) REFERENCES Passengers(passenger_id)
);

CREATE TABLE Flights (
    flight_id VARCHAR(50) PRIMARY KEY,
    flight_number VARCHAR(20),
    origin VARCHAR(10),
    destination VARCHAR(10),
    aircraft_type VARCHAR(50),
    flight_date DATE,
    delay_minutes INT
);

CREATE TABLE InternalFeedback (
    feedback_id VARCHAR(50) PRIMARY KEY,
    passenger_id VARCHAR(50),
    flight_id VARCHAR(50),
    rating_overall INT,
    nps_score INT,
    rating_crew INT,
    rating_food INT,
    rating_seat INT,
    rating_ground INT,
    submission_date DATE,
    FOREIGN KEY (passenger_id) REFERENCES Passengers(passenger_id),
    FOREIGN KEY (flight_id) REFERENCES Flights(flight_id)
);
