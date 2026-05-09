CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    full_name VARCHAR(255),
    base_location VARCHAR(150),
    team_principal VARCHAR(100),
    engine_supplier VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE drivers (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    driver_code VARCHAR(3) UNIQUE,
    nationality VARCHAR(50),
    permanent_number INT UNIQUE,
    birth_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE contracts (
    id SERIAL PRIMARY KEY,
    driver_id INT NOT NULL,
    team_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    salary_m_usd DECIMAL(10, 2),
    contract_type VARCHAR(50) DEFAULT 'Full-time',

    CONSTRAINT fk_driver FOREIGN KEY (driver_id) REFERENCES drivers(id) ON DELETE CASCADE,
    CONSTRAINT fk_team FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
    CONSTRAINT date_check CHECK (end_date > start_date)
);

CREATE TABLE races (
    id SERIAL PRIMARY KEY,
    gp_name VARCHAR(150) NOT NULL,
    circuit_name VARCHAR(150) NOT NULL,
    country VARCHAR(100),
    race_date DATE NOT NULL,
    laps_count INT,
    season_year INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE race_results (
    id SERIAL PRIMARY KEY,
    race_id INT NOT NULL,
    driver_id INT NOT NULL,
    team_id INT NOT NULL,
    position INT,
    points_earned DECIMAL(4, 1) DEFAULT 0,
    is_fastest_lap BOOLEAN DEFAULT FALSE,
    did_not_finish BOOLEAN DEFAULT FALSE,
    status_reason VARCHAR(100),

    CONSTRAINT fk_race FOREIGN KEY (race_id) REFERENCES races(id) ON DELETE CASCADE,
    CONSTRAINT fk_driver_res FOREIGN KEY (driver_id) REFERENCES drivers(id) ON DELETE CASCADE,
    CONSTRAINT fk_team_res FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
    CONSTRAINT pos_check CHECK (position >= 1 AND position <= 30)
);

CREATE INDEX idx_driver_last_name ON drivers(last_name);
CREATE INDEX idx_race_date ON races(race_date);
CREATE INDEX idx_results_race ON race_results(race_id);