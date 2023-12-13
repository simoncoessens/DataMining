-- Creation of the database main table
CREATE TABLE vehicle_data (
    mapped_veh_id INT,
    timestamps_UTC TIMESTAMP,
    lat FLOAT,
    lon FLOAT,
    RS_E_InAirTemp_PC1 FLOAT,
    RS_E_InAirTemp_PC2 FLOAT,
    RS_E_OilPress_PC1 FLOAT,
    RS_E_OilPress_PC2 FLOAT,
    RS_E_RPM_PC1 FLOAT,
    RS_E_RPM_PC2 FLOAT,
    RS_E_WatTemp_PC1 FLOAT,
    RS_E_WatTemp_PC2 FLOAT,
    RS_T_OilTemp_PC1 FLOAT,
    RS_T_OilTemp_PC2 FLOAT
);

-- I imported the csv file in Datagrip with a built in function


-- Test if the database works
SELECT COUNT(*) FROM vehicle_data;

SELECT * FROM vehicle_data LIMIT 10;

SELECT * FROM vehicle_data WHERE mapped_veh_id = 181;


-- Index creation
CREATE INDEX idx_timestamps_utc ON vehicle_data(timestamps_UTC);

CREATE INDEX idx_mapped_veh_id ON vehicle_data(mapped_veh_id);

-- POSTGIS extension 
CREATE EXTENSION POSTGIS;

ALTER TABLE vehicle_data
ADD COLUMN pg_point GEOGRAPHY(Point);

UPDATE vehicle_data
SET pg_point = ST_MakePoint(lon, lat)::geography;

