CREATE TABLE weather_stations (
  id SERIAL PRIMARY KEY,
  station VARCHAR(12) NOT NULL,
  name VARCHAR(50) NOT NULL,
  latitude VARCHAR(20) NOT NULL,
  longitude VARCHAR(20) NOT NULL,
  elevation VARCHAR(20) NOT NULL
);

SELECT * from weather_stations;

ALTER TABLE weather_stations
ALTER COLUMN elevation TYPE VARCHAR(20);