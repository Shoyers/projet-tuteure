CREATE DATABASE serv-projet;

-- Table unique pour stocker toutes les données des capteurs
CREATE TABLE `serv-projet`.sensor_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Données des capteurs
    air_quality INT NULL,            -- Qualité de l'air (valeur agrégée) en PPM
    distance DECIMAL(5,2) NULL,      -- Distance (HC-SR04) en mètres
    luminosity INT NULL,             -- Luminosité visible (SI1145) en lux
    uv_index DECIMAL(4,2) NULL,      -- Indice UV (SI1145)
    ir_value INT NULL,               -- Valeur infrarouge (SI1145)
    temperature DECIMAL(4,1) NULL,   -- Température (BME680) en °C
    pressure INT NULL,               -- Pression (BME680) en hPa
    humidity INT NULL,               -- Humidité (BME680) en %
    -- Données brutes (optionnel)
    raw_data TEXT NULL               -- Données brutes reçues du XBee
);

-- Index pour accélérer les requêtes par date
CREATE INDEX idx_sensor_data_timestamp ON sensor_data (timestamp);

-- Exemples d'insertion de données
-- INSERT INTO sensor_data (air_quality,  distance, luminosity, uv_index, ir_value, temperature, pressure, humidity, raw_data)
-- VALUES (800, 8.34, 16.75, 2.5, 800, 0.34, 348, 24.5, 1010, 65, 'AQ:800,DIST:2.5,LUM:800,UV:0.34,IR:348,TEMP:24.5,PRESS:1010,HUM:65');

-- Exemples de requêtes utiles

-- 1. Obtenir les 10 dernières mesures
-- SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 10;

-- 2. Obtenir la moyenne des valeurs sur la dernière heure
-- SELECT 
--     AVG(air_quality) as avg_air_quality,
--     AVG(distance) as avg_distance,
--     AVG(luminosity) as avg_luminosity,
--     AVG(uv_index) as avg_uv,
--     AVG(ir_value) as avg_ir,
--     AVG(temperature) as avg_temperature,
--     AVG(pressure) as avg_pressure,
--     AVG(humidity) as avg_humidity
-- FROM sensor_data
-- WHERE timestamp > DATE_SUB(NOW(), INTERVAL 1 HOUR);

-- 3. Obtenir les valeurs min, max et moyennes par jour
-- SELECT 
--     DATE(timestamp) as date,
--     MIN(temperature) as min_temp,
--     MAX(temperature) as max_temp,
--     AVG(temperature) as avg_temp,
--     AVG(uv_index) as avg_uv,
--     AVG(humidity) as avg_humidity
-- FROM sensor_data
-- GROUP BY DATE(timestamp)
-- ORDER BY date DESC; 