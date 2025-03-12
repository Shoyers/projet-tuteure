from datetime import datetime

# Modèle pour les données des capteurs
class SensorData:
    # Initialise un objet SensorData
    def __init__(self, airQuality=None, distance=None, luminosity=None, 
                 temperature=None, humidity=None, pressure=None, timestamp=None):
        """
        Args:
            air_quality: Qualité de l'air en PPM
            distance: Distance en mètres
            luminosity: Luminosité en lux
            temperature: Température en °C
            humidity: Humidité en %
            pressure: Pression en hPa
            timestamp: Horodatage de la mesure
        """
        self.airQuality = airQuality
        self.distance = distance
        self.luminosity = luminosity
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.timestamp = timestamp or datetime.now()
    
    @classmethod
    def fromDict(cls, dataDict):
        """
        Crée un objet SensorData à partir d'un dictionnaire.
        
        Args:
            data_dict: Dictionnaire contenant les valeurs des capteurs
            
        Returns:
            Un objet SensorData
        """
        return cls(
            airQuality=dataDict.get('airQuality'),
            distance=dataDict.get('distance'),
            luminosity=dataDict.get('luminosity'),
            temperature=dataDict.get('temperature'),
            humidity=dataDict.get('humidity'),
            pressure=dataDict.get('pressure'),
            timestamp=dataDict.get('timestamp', datetime.now())
        )
    
    # Convertit l'objet SensorData en dictionnaire
    def toDict(self):
        """
        Returns:
            Un dictionnaire contenant les valeurs des capteurs
        """
        return {
            'airQuality': self.airQuality,
            'distance': self.distance,
            'luminosity': self.luminosity,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'timestamp': self.timestamp
        }
    
    # Convertit l'objet SensorData en tuple pour l'insertion en base de données
    def toDbTuple(self):
        """
        Returns:
            Un tuple contenant les valeurs des capteurs
        """
        timestampStr = self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        return (
            timestampStr,
            self.airQuality,
            self.distance,
            self.luminosity,
            self.temperature,
            self.pressure,
            self.humidity
        )
    
    # Retourne une représentation en chaîne de caractères de l'objet SensorData
    def __str__(self):
        """
        Returns:
            Une chaîne de caractères représentant l'objet SensorData
        """
        timestampStr = self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        return (
            f"SensorData(timestamp={timestampStr}, "
            f"airQuality={self.airQuality}, "
            f"distance={self.distance}, "
            f"luminosity={self.luminosity}, "
            f"temperature={self.temperature}, "
            f"humidity={self.humidity}, "
            f"pressure={self.pressure})"
        ) 