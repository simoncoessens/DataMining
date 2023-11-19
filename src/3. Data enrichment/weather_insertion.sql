-- Include PostGIS
CREATE EXTENSION postgis;

-- Add geom for general table
ALTER TABLE vehicle_data ADD COLUMN geom geometry(Point, 4326);
UPDATE vehicle_data SET geom = ST_SetSRID(ST_MakePoint(lon, lat), 4326)
WHERE mapped_veh_id is not null;

-- Create a table for the weather data
CREATE TABLE weather_data (
    id NUMERIC,
    lat NUMERIC,
    lon NUMERIC,
    timestamps_weather Text,
    temperature NUMERIC,
    humidity INTEGER,
    rain NUMERIC,
    geom geometry(POINT, 4326)
);

-- Import weather_pull_data.csv (generated with weather_pull.py) using built-in function

-- Include geom values
UPDATE weather_data SET geom = ST_SetSRID(ST_MakePoint(lon, lat), 4326)
WHERE id is not null;

-- Update values from vehicle_data table with the following join
CREATE TABLE vehicle_data_weather AS
SELECT
    a.mapped_veh_id,
    a.timestamps_UTC,
    a.lat,
    a.lon,
    a.RS_E_InAirTemp_PC1,
    a.RS_E_InAirTemp_PC2,
    a.RS_E_OilPress_PC1,
    a.RS_E_OilPress_PC2,
    a.RS_E_RPM_PC1,
    a.RS_E_RPM_PC2,
    a.RS_E_WatTemp_PC1,
    a.RS_E_WatTemp_PC2,
    a.RS_T_OilTemp_PC1,
    a.RS_T_OilTemp_PC2,
    w.temperature,
    w.humidity,
    w.rain
FROM
    vehicle_data a
LEFT JOIN LATERAL (
    SELECT
        temperature,
        humidity,
        rain
    FROM
        weather_data w
    WHERE
        ST_Distance(ST_GeomFromText('POINT(' || a.lon || ' ' || a.lat || ')', 4326), w.geom) =
            (SELECT MIN(ST_Distance(ST_GeomFromText('POINT(' || a.lon || ' ' || a.lat || ')', 4326), w.geom))
             FROM weather_data w
             WHERE EXTRACT(HOUR FROM a.timestamps_UTC::TIMESTAMP) = EXTRACT(HOUR FROM w.timestamps_weather::TIMESTAMP))
    LIMIT 1
) w ON true;