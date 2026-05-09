INSERT INTO teams (name, full_name, base_location, team_principal, engine_supplier) VALUES
('Red Bull', 'Oracle Red Bull Racing', 'Milton Keynes, UK', 'Christian Horner', 'Honda RBPT'),
('Mercedes', 'Mercedes-AMG PETRONAS F1 Team', 'Brackley, UK', 'Toto Wolff', 'Mercedes'),
('Ferrari', 'Scuderia Ferrari', 'Maranello, Italy', 'Frédéric Vasseur', 'Ferrari'),
('McLaren', 'McLaren Formula 1 Team', 'Woking, UK', 'Andrea Stella', 'Mercedes'),
('Aston Martin', 'Aston Martin Aramco F1 Team', 'Silverstone, UK', 'Mike Krack', 'Mercedes'),
('Alpine', 'BWT Alpine F1 Team', 'Enstone, UK', 'Oliver Oakes', 'Renault'),
('Williams', 'Williams Racing', 'Grove, UK', 'James Vowles', 'Mercedes'),
('RB', 'Visa Cash App RB F1 Team', 'Faenza, Italy', 'Laurent Mekies', 'Honda RBPT'),
('Sauber', 'Stake F1 Team Kick Sauber', 'Hinwil, Switzerland', 'Alessandro Alunni Bravi', 'Ferrari'),
('Haas', 'MoneyGram Haas F1 Team', 'Kannapolis, USA', 'Ayao Komatsu', 'Ferrari');

INSERT INTO drivers (first_name, last_name, driver_code, nationality, permanent_number, birth_date) VALUES
('Max', 'Verstappen', 'VER', 'Dutch', 1, '1997-09-30'),
('Sergio', 'Perez', 'PER', 'Mexican', 11, '1990-01-26'),
('Lewis', 'Hamilton', 'HAM', 'British', 44, '1985-01-07'),
('George', 'Russell', 'RUS', 'British', 63, '1998-02-15'),
('Charles', 'Leclerc', 'LEC', 'Monegasque', 16, '1997-10-16'),
('Carlos', 'Sainz', 'SAI', 'Spanish', 55, '1994-09-01'),
('Lando', 'Norris', 'NOR', 'British', 4, '1999-11-13'),
('Oscar', 'Piastri', 'PIA', 'Australian', 81, '2001-04-06'),
('Fernando', 'Alonso', 'ALO', 'Spanish', 14, '1981-07-29'),
('Lance', 'Stroll', 'STR', 'Canadian', 18, '1998-10-29'),
('Pierre', 'Gasly', 'GAS', 'French', 10, '1996-02-07'),
('Esteban', 'Ocon', 'OCO', 'French', 31, '1996-09-17'),
('Alexander', 'Albon', 'ALB', 'Thai', 23, '1996-03-23'),
('Logan', 'Sargeant', 'SAR', 'American', 2, '2000-12-31'),
('Daniel', 'Ricciardo', 'RIC', 'Australian', 3, '1989-07-01'),
('Yuki', 'Tsunoda', 'TSU', 'Japanese', 22, '2000-05-11'),
('Valtteri', 'Bottas', 'BOT', 'Finnish', 77, '1989-08-28'),
('Zhou', 'Guanyu', 'ZHO', 'Chinese', 24, '1999-05-30'),
('Kevin', 'Magnussen', 'MAG', 'Danish', 20, '1992-10-05'),
('Nico', 'Hulkenberg', 'HUL', 'German', 27, '1987-08-19');


INSERT INTO contracts (driver_id, team_id, start_date, end_date, salary_m_usd)
VALUES
((SELECT id FROM drivers WHERE driver_code = 'VER'), (SELECT id FROM teams WHERE name = 'Red Bull'), '2024-01-01', '2028-12-31', 55.0),
((SELECT id FROM drivers WHERE driver_code = 'HAM'), (SELECT id FROM teams WHERE name = 'Mercedes'), '2024-01-01', '2024-12-31', 45.0),
((SELECT id FROM drivers WHERE driver_code = 'LEC'), (SELECT id FROM teams WHERE name = 'Ferrari'), '2024-01-01', '2029-12-31', 34.0),
((SELECT id FROM drivers WHERE driver_code = 'NOR'), (SELECT id FROM teams WHERE name = 'McLaren'), '2024-01-01', '2026-12-31', 20.0);
