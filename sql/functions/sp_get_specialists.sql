CREATE OR REPLACE FUNCTION sp_get_specialists(symptoms TEXT[])
RETURNS TABLE(name TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT s.name
    FROM specialists s
    JOIN specialist_symptom ss ON s.id = ss.specialist_id
    JOIN symptoms sy ON sy.id = ss.symptom_id
    WHERE sy.name = ANY(symptoms);
END;
$$ LANGUAGE plpgsql;
