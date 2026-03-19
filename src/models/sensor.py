# Modèle pour les capteurs
class Sensor:
    def __init__(self):
        self.air_quality = None
        self.distance = None
        self.luminosity = None
        self.uvIndex = None
        self.irValue = None
        self.temperature = None
        self.pressure = None
        self.humidity = None
        self.gas = None
        self.latitude = None
        self.longitude = None
        self.altitude = None

    def updateFromStr(self, dataStr):
        """
        Met à jour les valeurs des capteurs à partir d'une chaîne de données.
        Utilise le parser centralisé pour supporter tous les formats.
        """
        from src.utils.sensor_parser import parse_sensor_string
        
        if not dataStr:
            print("Chaîne de données vide")
            return False
        
        print(f"Mise à jour depuis: {dataStr}")
        old_values = self.toDict()
        
        # Parser la chaîne
        parsed = parse_sensor_string(dataStr)
        
        if not parsed:
            print("Aucune donnée parsée")
            return False
        
        # Mettre à jour les attributs
        updated = False
        for key, value in parsed.items():
            if value is not None:
                if key == 'uv_index':
                    self.uvIndex = value
                    updated = True
                elif key == 'ir_value':
                    self.irValue = value
                    updated = True
                elif hasattr(self, key):
                    setattr(self, key, value)
                    updated = True
        
        if updated:
            changes = []
            for key, new_value in self.toDict().items():
                if old_values[key] != new_value:
                    changes.append(f"{key}: {old_values[key]} -> {new_value}")
            print(f"Changements: {', '.join(changes)}")
        
        return updated

    def toDict(self):
        """Retourne un dictionnaire avec les valeurs des capteurs."""
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
            'altitude': self.altitude
        } 