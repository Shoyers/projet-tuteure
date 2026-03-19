from datetime import datetime

class SensorData:
    def __init__(self, air_quality=None, distance=None, luminosity=None,
                 uvIndex=None, irValue=None, temperature=None, pressure=None, 
                 humidity=None, gas=None, latitude=None, longitude=None, altitude=None,
                 timestamp=None, rawData=None):
        """Initialise les données du capteur."""
        self.air_quality = air_quality
        self.distance = distance
        self.luminosity = luminosity
        self.uvIndex = uvIndex
        self.irValue = irValue
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity
        self.gas = gas
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.timestamp = timestamp or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.rawData = rawData

    @classmethod
    def fromDict(cls, data_dict):
        """Crée un objet SensorData à partir d'un dictionnaire."""
        from src.utils.sensor_parser import normalize_sensor_dict
        
        if not data_dict:
            return None
        
        # Normaliser les clés
        normalized = normalize_sensor_dict(data_dict)
        
        return cls(
            air_quality=normalized.get('air_quality'),
            distance=normalized.get('distance'),
            luminosity=normalized.get('luminosity'),
            uvIndex=normalized.get('uv_index'),
            irValue=normalized.get('ir_value'),
            temperature=normalized.get('temperature'),
            pressure=normalized.get('pressure'),
            humidity=normalized.get('humidity'),
            gas=normalized.get('gas'),
            latitude=normalized.get('latitude'),
            longitude=normalized.get('longitude'),
            altitude=normalized.get('altitude'),
            timestamp=normalized.get('timestamp'),
            rawData=normalized.get('raw_data')
        )
    
    def toDict(self):
        """Convertit l'objet SensorData en dictionnaire."""
        return {
            'air_quality': self.air_quality,
            'distance': self.distance,
            'luminosity': self.luminosity,
            'uvIndex': self.uvIndex,
            'irValue': self.irValue,
            'temperature': self.temperature,
            'pressure': self.pressure,
            'humidity': self.humidity,
            'gas': self.gas,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'altitude': self.altitude,
            'timestamp': self.timestamp,
            'rawData': self.rawData
        }
    
    def __str__(self):
        """Retourne une représentation en chaîne de l'objet SensorData."""
        return (
            f"air_quality={self.air_quality}, "
            f"distance={self.distance}, "
            f"luminosity={self.luminosity}, "
            f"uvIndex={self.uvIndex}, "
            f"irValue={self.irValue}, "
            f"temperature={self.temperature}, "
            f"pressure={self.pressure}, "
            f"humidity={self.humidity}, "
            f"gas={self.gas}, "
            f"latitude={self.latitude}, "
            f"longitude={self.longitude}, "
            f"altitude={self.altitude}, "
            f"timestamp={self.timestamp}"
        ) 