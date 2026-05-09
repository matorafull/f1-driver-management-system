CREATE OR REPLACE FUNCTION check_contract_overlap()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM contracts
        WHERE driver_id = NEW.driver_id
          AND id != NEW.id
          AND (
            (NEW.start_date, COALESCE(NEW.end_date, '9999-12-31')) OVERLAPS
            (start_date, COALESCE(end_date, '9999-12-31'))
          )
    ) THEN
        RAISE EXCEPTION 'Пилот с ID % уже имеет активный контракт на этот период времени.', NEW.driver_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_constructor_standings(season_year_input INT)
RETURNS TABLE(team_name VARCHAR, total_points DECIMAL) AS $$
BEGIN
    RETURN QUERY
    SELECT
        t.name,
        SUM(rr.points_earned) as total_points
    FROM teams t
    JOIN race_results rr ON t.id = rr.team_id
    JOIN races r ON rr.race_id = r.id
    WHERE r.season_year = season_year_input
    GROUP BY t.name
    ORDER BY total_points DESC;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_check_contract_overlap
BEFORE INSERT OR UPDATE ON contracts
FOR EACH ROW EXECUTE FUNCTION check_contract_overlap();