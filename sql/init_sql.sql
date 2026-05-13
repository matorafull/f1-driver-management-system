-- Очистка старых данных
DROP VIEW IF EXISTS view_team_standings;
DROP TABLE IF EXISTS race_penalties CASCADE;
DROP TABLE IF EXISTS race_results CASCADE;
DROP TABLE IF EXISTS races CASCADE;
DROP TABLE IF EXISTS cars CASCADE;
DROP TABLE IF EXISTS drivers CASCADE;
DROP TABLE IF EXISTS teams CASCADE;
DROP TABLE IF EXISTS circuits CASCADE;

-- 1. Справочники
CREATE TABLE circuits (
    circuit_id   SERIAL PRIMARY KEY,
    circuit_name VARCHAR(100) NOT NULL,
    country      VARCHAR(50),
    length_km    NUMERIC(5, 3)
);

CREATE TABLE teams (
    team_id      SERIAL PRIMARY KEY,
    team_name    VARCHAR(100) NOT NULL UNIQUE,
    base_city    VARCHAR(100),
    budget_cap   NUMERIC(15, 2)
);

-- 2. Объекты команд
CREATE TABLE drivers (
    driver_id     SERIAL PRIMARY KEY,
    full_name     VARCHAR(100) NOT NULL,
    team_id       INT REFERENCES teams (team_id),
    country       VARCHAR(50),
    driver_number INT UNIQUE,
    salary        NUMERIC(12, 2)
);

CREATE TABLE cars (
    car_id       SERIAL PRIMARY KEY,
    model_name   VARCHAR(50) NOT NULL,
    team_id      INT REFERENCES teams (team_id),
    engine_power INT,
    weight_kg    INT
);

-- 3. События
CREATE TABLE races (
    race_id        SERIAL PRIMARY KEY,
    race_name      VARCHAR(100),
    circuit_id     INT REFERENCES circuits (circuit_id),
    race_date      DATE DEFAULT CURRENT_DATE,
    laps_total     INT
);

-- 4. Результаты
CREATE TABLE race_results (
    result_id    SERIAL PRIMARY KEY,
    race_id      INT REFERENCES races (race_id) ON DELETE CASCADE,
    driver_id    INT REFERENCES drivers (driver_id),
    car_id       INT REFERENCES cars (car_id),
    position     INT,
    points_earned INT DEFAULT 0
);

-- 5. ЗАПОЛНЕНИЕ ДАННЫМИ

INSERT INTO circuits (circuit_name, country, length_km)
VALUES ('Suzuka Circuit', 'Japan', 5.807);

INSERT INTO teams (team_name, base_city, budget_cap)
VALUES ('Red Bull Racing', 'Milton Keynes', 135000000),
       ('Ferrari', 'Maranello', 135000000);

INSERT INTO drivers (full_name, team_id, driver_number, salary)
VALUES ('Max Verstappen', 1, 1, 55000000),
       ('Charles Leclerc', 2, 16, 36000000);

INSERT INTO cars (model_name, team_id, engine_power, weight_kg)
VALUES ('RB20', 1, 1050, 798),
       ('SF-24', 2, 1040, 798);

INSERT INTO races (race_name, circuit_id, laps_total)
VALUES ('Japanese Grand Prix', 1, 53);

INSERT INTO race_results (race_id, driver_id, car_id, position, points_earned)
VALUES (1, 1, 1, 1, 25),
       (1, 2, 2, 2, 18);

-- 6. Аналитическая вьюха (Исправленная для dashboard.html)
CREATE OR REPLACE VIEW view_team_standings AS
SELECT
    t.team_id,
    t.team_name,
    t.budget_cap,
    COALESCE(SUM(rr.points_earned), 0) as total_points,
    COUNT(CASE WHEN rr.position <= 3 THEN 1 END) as total_podiums,
    CASE
        WHEN SUM(rr.points_earned) > 0
        THEN ROUND(t.budget_cap / SUM(rr.points_earned), 2)
        ELSE 0
    END as cost_per_point
FROM teams t
LEFT JOIN drivers d ON t.team_id = d.team_id
LEFT JOIN race_results rr ON d.driver_id = rr.driver_id
GROUP BY t.team_id, t.team_name, t.budget_cap
ORDER BY total_points DESC;