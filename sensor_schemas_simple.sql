CREATE DATABASE IF NOT EXISTS `serv-projet`;

CREATE TABLE `serv-projet`.sensor_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Données des capteurs
    co2 INT NULL,                    -- MQ135 (approx CO2 / qualité air)
    distance DECIMAL(5,2) NULL,      -- HC-SR04 (mètres ou cm selon ton choix)
    luminosity INT NULL,             -- SI1145 visible
    uv_index DECIMAL(4,2) NULL,      -- SI1145 UV
    ir_value INT NULL,               -- SI1145 IR
    temperature DECIMAL(4,1) NULL,   -- BME680 °C
    pressure INT NULL,               -- BME680 hPa
    humidity INT NULL,               -- BME680 %
    gas DOUBLE NULL,                 -- BME680 gas resistance

    -- Données GPS (plus précis que ta version initiale)
    latitude DECIMAL(10,8) NULL,
    longitude DECIMAL(11,8) NULL,
    altitude DECIMAL(7,2) NULL,

    -- ML / analyse
    confidence DECIMAL(3,2) NULL,    -- ex: 0.85
    reason TEXT NULL,                -- explication (ex: "fumée détectée")

    -- Données brutes
    raw_data TEXT NULL
);

-- Index pour perf (très important pour timeseries)
CREATE INDEX idx_sensor_data_timestamp 
ON `serv-projet`.sensor_data (timestamp);