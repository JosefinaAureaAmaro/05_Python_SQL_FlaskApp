CREATE TABLE weather_stations (
  id SERIAL PRIMARY KEY,
  station VARCHAR(12) NOT NULL,
  name VARCHAR(50) NOT NULL,
  latitude INT NOT NULL,
  longitude INT NOT NULL,
  elevation INT NOT NULL
);

SELECT * from weather_stations;