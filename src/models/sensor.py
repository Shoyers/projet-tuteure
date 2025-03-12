# Modèle pour les capteurs
class Sensor:
    def __init__(self):
        self.airQuality = 0;
        self.distance = 0.0;
        self.luminosity = 0;
        self.temperature = 20.0;
        self.pressure = 1000;
        self.humidity = 50;

    # Met à jour les valeurs des capteurs à partir d'une chaîne de données
    def updateFromStr(self, dataStr):
        """
        Args:
            dataStr: Chaîne de données contenant les valeurs des capteurs
            
        Format attendu: "AQ:150,DIST:2.5,LUM:800,TEMP:24.5,PRESS:1010,HUM:65"
        """
        try:
            import re;
            
            # Recherche des valeurs avec des expressions régulières
            airQualityMatch = re.search(r'AQ:(\d+)', dataStr);
            distanceMatch = re.search(r'DIST:([\d.]+)', dataStr);
            luminosityMatch = re.search(r'LUM:(\d+)', dataStr);
            temperatureMatch = re.search(r'TEMP:([\d.]+)', dataStr);
            pressureMatch = re.search(r'PRESS:(\d+)', dataStr);
            humidityMatch = re.search(r'HUM:(\d+)', dataStr);
            
            # Mise à jour des valeurs si trouvées
            if airQualityMatch:
                self.airQuality = int(airQualityMatch.group(1));
            if distanceMatch:
                self.distance = float(distanceMatch.group(1));
            if luminosityMatch:
                self.luminosity = int(luminosityMatch.group(1));
            if temperatureMatch:
                self.temperature = float(temperatureMatch.group(1));
            if pressureMatch:
                self.pressure = int(pressureMatch.group(1));
            if humidityMatch:
                self.humidity = int(humidityMatch.group(1));
                
            return True;
        except Exception as e:
            print(f'Erreur lors de l\'analyse des données: {str(e)}');
            return False;

    # Convertit les données en dictionnaire
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
            'pressure': self.pressure,
            'humidity': self.humidity
        }; 