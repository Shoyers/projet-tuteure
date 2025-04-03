from datetime import datetime

# Classe pour représenter les données des capteurs
class SensorData:
    def __init__(self, air_quality=None, distance=None, luminosity=None,
                 uvIndex=None, irValue=None, temperature=None, pressure=None, 
                 humidity=None, timestamp=None, rawData=None):
        """
        Initialise les données du capteur.
        
        Args:
            air_quality: Qualité de l'air en PPM
            distance: Distance en mètres
            luminosity: Luminosité en lux
            uvIndex: Indice UV
            irValue: Valeur de l'infrarouge
            temperature: Température en degrés Celsius
            pressure: Pression atmosphérique en hPa
            humidity: Humidité relative en %
            timestamp: Horodatage de la mesure
            rawData: Données brutes reçues
        """
        self.air_quality = air_quality
        self.distance = distance
        self.luminosity = luminosity
        self.uvIndex = uvIndex
        self.irValue = irValue
        self.temperature = temperature
        self.pressure = pressure
        self.humidity = humidity
        self.timestamp = timestamp or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.rawData = rawData

    # Convertit un dictionnaire en objet SensorData
    @classmethod
    def fromDict(cls, data_dict):
        """
        Crée un objet SensorData à partir d'un dictionnaire.
        
        Args:
            data_dict: Dictionnaire contenant les données des capteurs
            
        Returns:
            Une nouvelle instance de SensorData
        """
        if not data_dict:
            return None
        
        # Définition des mappages de clés
        key_mapping = {
            'air_quality': ['air_quality', 'airQuality', 'AQ'],
            'distance': ['distance', 'dist', 'DIST'],
            'luminosity': ['luminosity', 'lum', 'LUM'],
            'uvIndex': ['uvIndex', 'uv_index', 'UV'],
            'irValue': ['irValue', 'ir_value', 'IR'],
            'temperature': ['temperature', 'temp', 'TEMP'],
            'pressure': ['pressure', 'press', 'PRESS'],
            'humidity': ['humidity', 'hum', 'HUM'],
            'timestamp': ['timestamp', 'time', 'date'],
            'rawData': ['rawData', 'raw_data', 'raw']
        }
        
        # Fonction pour obtenir la valeur d'une clé en vérifiant différentes alternatives
        def get_value_from_dict(keys):
            for key in keys:
                if key in data_dict and data_dict[key] is not None:
                    return data_dict[key]
            return None
        
        # Extraire les valeurs
        air_quality = get_value_from_dict(key_mapping['air_quality'])
        distance = get_value_from_dict(key_mapping['distance'])
        luminosity = get_value_from_dict(key_mapping['luminosity'])
        uv_index = get_value_from_dict(key_mapping['uvIndex'])
        ir_value = get_value_from_dict(key_mapping['irValue'])
        temperature = get_value_from_dict(key_mapping['temperature'])
        pressure = get_value_from_dict(key_mapping['pressure'])
        humidity = get_value_from_dict(key_mapping['humidity'])
        timestamp = get_value_from_dict(key_mapping['timestamp'])
        raw_data = get_value_from_dict(key_mapping['rawData'])
        
        # Afficher les valeurs extraites pour le débogage
        print(f"Valeurs extraites: air_quality={air_quality}, " +
              f"distance={distance}, luminosity={luminosity}, uv_index={uv_index}, " +
              f"ir_value={ir_value}, temperature={temperature}, pressure={pressure}, humidity={humidity}")
        
        # Créer l'objet SensorData
        return cls(
            air_quality=air_quality,
            distance=distance,
            luminosity=luminosity,
            uvIndex=uv_index,
            irValue=ir_value,
            temperature=temperature,
            pressure=pressure,
            humidity=humidity,
            timestamp=timestamp,
            rawData=raw_data
        )
    
    # Convertit l'objet SensorData en dictionnaire
    def toDict(self):
        """
        Convertit l'objet SensorData en dictionnaire.
        
        Returns:
            Un dictionnaire contenant les données des capteurs
        """
        return {
            'air_quality': self.air_quality,
            'distance': self.distance,
            'luminosity': self.luminosity,
            'uvIndex': self.uvIndex,
            'irValue': self.irValue,
            'temperature': self.temperature,
            'pressure': self.pressure,
            'humidity': self.humidity,
            'timestamp': self.timestamp,
            'rawData': self.rawData
        }
    
    # Représentation en chaîne de l'objet SensorData
    def __str__(self):
        """
        Retourne une représentation en chaîne de l'objet SensorData.
        
        Returns:
            Une chaîne représentant l'objet SensorData
        """
        return (
            f"air_quality={self.air_quality}, "
            f"distance={self.distance}, "
            f"luminosity={self.luminosity}, "
            f"uvIndex={self.uvIndex}, "
            f"irValue={self.irValue}, "
            f"temperature={self.temperature}, "
            f"pressure={self.pressure}, "
            f"humidity={self.humidity}, "
            f"timestamp={self.timestamp}"
        ) 