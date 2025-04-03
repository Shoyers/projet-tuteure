# Modèle pour les capteurs
class Sensor:
    def __init__(self):
        # Initialisation avec des valeurs par défaut
        # Utiliser None pour certaines valeurs pour différencier les non-mesurées des zéros réels
        self.air_quality = None; # Qualité de l'air en PPM
        self.distance = None;    # Distance en mètres
        self.luminosity = None;  # Luminosité visible en lux
        self.uvIndex = None;     # Indice UV du capteur SI1145
        self.irValue = None;     # Valeur infrarouge du capteur SI1145
        self.temperature = 20.0; # Température ambiante standard
        self.pressure = 1013;    # Pression atmosphérique standard (hPa)
        self.humidity = 50;      # Humidité relative standard

    # Met à jour les valeurs des capteurs à partir d'une chaîne de données
    def updateFromStr(self, dataStr):
        print(f"Mise à jour des valeurs depuis la chaîne: {dataStr}")
        """
        Args:
            dataStr: Chaîne de données contenant les valeurs des capteurs
            
        Formats supportés:
        - Format standard: "AQ:800,DIST:2.5,LUM:800,TEMP:24.5,PRESS:1010,HUM:65"
        - Format Arduino: "Temperature = 24.97 *C", "Pression = 1012.39 hPa", etc.
        - Format SI1145: "SI1145 - Visible: 262", "SI1145 - UV: 0.35", "SI1145 - IR: 348"
        - Format MQ135: "MQ135 - Air Quality: 8.94 ppm", "MQ135 - Valeur lue: 348"
        - Format BME680: "BME680 - Temperature: 25.65 *C", "BME680 - Pression: 1010.01 hPa", "BME680 - Humidité: 31.57 %"
        - Format HC-SR04: "HC_SR04 - Distance: 34 cm"
        """
        if not dataStr:
            print("Chaîne de données vide, impossible de mettre à jour les valeurs");
            return False;
            
        # Enregistrer les valeurs précédentes pour détecter les changements
        oldValues = self.toDict();
        updated = False;  # Drapeau pour vérifier si au moins une valeur a été mise à jour
        
        try:
            print(f"Analyse des données: {dataStr}");
            
            # Format Arduino ou formats spécifiques
            if "=" in dataStr or "SI1145" in dataStr or "MQ135" in dataStr or "BME680" in dataStr or "HC_SR04" in dataStr:
                try:
                    import re
                    # Traiter les différents formats spécifiques d'Arduino
                    if "Temperature" in dataStr:
                        # Format "Temperature = 24.97 *C" ou "BME680 - Temperature: 25.65 *C"
                        match = re.search(r'Temperature\s*[:=]\s*([\d.]+)', dataStr)
                        if match:
                            self.temperature = float(match.group(1))
                            print(f"Température mise à jour: {self.temperature}")
                            updated = True
                    elif "Pression" in dataStr:
                        # Format "Pression = 1012.39 hPa" ou "BME680 - Pression: 1010.01 hPa"
                        match = re.search(r'Pression\s*[:=]\s*([\d.]+)', dataStr)
                        if match:
                            self.pressure = int(float(match.group(1)))
                            print(f"Pression mise à jour: {self.pressure}")
                            updated = True
                    elif "Humidité" in dataStr or "Humidite" in dataStr or "HumiditÃ©" in dataStr:
                        # Format "Humidité = 65 %" ou "BME680 - Humidité: 31.57 %"
                        match = re.search(r'Humidit[éeÃ©]\s*[:=]\s*([\d.]+)', dataStr)
                        if match:
                            self.humidity = int(float(match.group(1)))
                            print(f"Humidité mise à jour: {self.humidity}")
                            updated = True
                    
                    # Capteur BME680
                    if "BME680" in dataStr:
                        if "Temperature" in dataStr:
                            match = re.search(r'BME680.*Temperature\s*[:=]\s*([\d.]+)', dataStr)
                            if match:
                                self.temperature = float(match.group(1))
                                print(f"Température BME680 mise à jour: {self.temperature}")
                                updated = True
                        elif "Pression" in dataStr:
                            match = re.search(r'BME680.*Pression\s*[:=]\s*([\d.]+)', dataStr)
                            if match:
                                self.pressure = int(float(match.group(1)))
                                print(f"Pression BME680 mise à jour: {self.pressure}")
                                updated = True
                        elif "Humidité" in dataStr or "Humidite" in dataStr:
                            match = re.search(r'BME680.*Humidit[ée]\s*[:=]\s*([\d.]+)', dataStr)
                            if match:
                                self.humidity = int(float(match.group(1)))
                                print(f"Humidité BME680 mise à jour: {self.humidity}")
                                updated = True
                    
                    # Capteur de distance HC-SR04
                    if "HC_SR04" in dataStr and "Distance" in dataStr:
                        # Format "HC_SR04 - Distance: 34 cm"
                        match = re.search(r'HC_SR04.*Distance\s*[:=]\s*([\d.]+)', dataStr)
                        if match:
                            # Convertir de cm à m
                            distance_cm = float(match.group(1))
                            self.distance = distance_cm / 100.0  # conversion en mètres
                            print(f"Distance HC-SR04 mise à jour: {self.distance} m (depuis {distance_cm} cm)")
                            updated = True
                    # Fallback pour le format générique de distance
                    elif "Distance" in dataStr and "HC_SR04" not in dataStr:
                        # Format "Distance = 34 cm" ou similaire
                        match = re.search(r'Distance\s*[:=]\s*([\d.]+)', dataStr)
                        if match:
                            self.distance = float(match.group(1))
                            print(f"Distance mise à jour: {self.distance}")
                            updated = True
                    
                    # Capteur SI1145 - Traiter les trois valeurs: UV, IR et Visible
                    if "SI1145" in dataStr:
                        if "Visible" in dataStr:
                            # Format "SI1145 - Visible: 262"
                            match = re.search(r'SI1145.*Visible[:\s]+(\d+)', dataStr)
                            if match:
                                self.luminosity = int(match.group(1))
                                print(f"Luminosité mise à jour depuis SI1145-Visible: {self.luminosity}")
                                updated = True
                            else:
                                print(f"Format SI1145-Visible non reconnu: {dataStr}")
                        elif "UV" in dataStr:
                            # Format "SI1145 - UV: 0.35"
                            match = re.search(r'SI1145.*UV[:\s]+([\d.]+)', dataStr)
                            if match:
                                self.uvIndex = float(match.group(1))
                                print(f"Indice UV mis à jour: {self.uvIndex}")
                                updated = True
                            else:
                                print(f"Format SI1145-UV non reconnu: {dataStr}")
                        elif "IR" in dataStr:
                            # Format "SI1145 - IR: 348"
                            match = re.search(r'SI1145.*IR[:\s]+(\d+)', dataStr)
                            if match:
                                self.irValue = int(match.group(1))
                                print(f"Valeur IR mise à jour: {self.irValue}")
                                updated = True
                            else:
                                print(f"Format SI1145-IR non reconnu: {dataStr}")
                    elif "Luminosité" in dataStr or "Luminosite" in dataStr or "LUM" in dataStr:
                        # Formats traditionnels pour luminosité
                        match = re.search(r'(Luminosit[éeÃ©]|LUM)\s*[:=]\s*([\d.]+)', dataStr)
                        if match:
                            self.luminosity = int(float(match.group(2)))
                            print(f"Luminosité mise à jour: {self.luminosity}")
                            updated = True
                    
                    # Capteur de qualité d'air MQ135
                    if "MQ135" in dataStr:
                        if "Valeur lue" in dataStr:
                            # Format "MQ135 - Valeur lue: 348"
                            match = re.search(r'MQ135.*Valeur lue[:\s]+(\d+)', dataStr)
                            if match:
                                mq135_value = int(match.group(1))
                                # Pour une valeur brute du MQ135, on peut estimer AQ
                                # Ces équations sont approximatives et devraient être calibrées
                                # Conversion simplifiée pour démonstration
                                self.air_quality = mq135_value  # Conversion approximative
                                print(f"Air Quality estimé depuis MQ135: {self.air_quality} ppm")
                                updated = True
                            else:
                                print(f"Format MQ135-Valeur lue non reconnu: {dataStr}")
                            
                except Exception as e:
                    print(f"Erreur lors du parsing format spécifique: {str(e)}")
                    import traceback
                    traceback.print_exc()
            
            # Format standard: "AQ:8.34,DIST:2.5,..."
            if not updated:
                import re
                # Recherche des valeurs avec des expressions régulières
                air_qualityMatch = re.search(r'AQ:([\d.]+)', dataStr)
                distanceMatch = re.search(r'DIST:([\d.]+)', dataStr)
                luminosityMatch = re.search(r'LUM:(\d+)', dataStr)
                uvMatch = re.search(r'UV:([\d.]+)', dataStr)
                irMatch = re.search(r'IR:(\d+)', dataStr)
                temperatureMatch = re.search(r'TEMP:([\d.]+)', dataStr)
                pressureMatch = re.search(r'PRESS:(\d+)', dataStr)
                humidityMatch = re.search(r'HUM:(\d+)', dataStr)
                
                # Mise à jour des valeurs si trouvées
                if air_qualityMatch:
                    self.air_quality = float(air_qualityMatch.group(1))
                    updated = True
                    print(f"Air Quality mis à jour: {self.air_quality}")
                if distanceMatch:
                    self.distance = float(distanceMatch.group(1))
                    updated = True
                    print(f"Distance mise à jour: {self.distance}")
                if luminosityMatch:
                    self.luminosity = int(luminosityMatch.group(1))
                    updated = True
                    print(f"Luminosité mise à jour: {self.luminosity}")
                if uvMatch:
                    self.uvIndex = float(uvMatch.group(1))
                    updated = True
                    print(f"Indice UV mis à jour: {self.uvIndex}")
                if irMatch:
                    self.irValue = int(irMatch.group(1))
                    updated = True
                    print(f"Valeur IR mise à jour: {self.irValue}")
                if temperatureMatch:
                    self.temperature = float(temperatureMatch.group(1))
                    updated = True
                    print(f"Température mise à jour: {self.temperature}")
                if pressureMatch:
                    self.pressure = int(pressureMatch.group(1))
                    updated = True
                    print(f"Pression mise à jour: {self.pressure}")
                if humidityMatch:
                    self.humidity = int(humidityMatch.group(1))
                    updated = True
                    print(f"Humidité mise à jour: {self.humidity}")
            
            # Comparer avec les anciennes valeurs pour voir ce qui a changé
            if updated:
                changes = []
                for key, newValue in self.toDict().items():
                    if oldValues[key] != newValue:
                        changes.append(f"{key}: {oldValues[key]} -> {newValue}")
                print(f"Changements détectés: {', '.join(changes)}")
                return True
            else:
                print("Aucune valeur n'a été mise à jour")
                return False
        except Exception as e:
            print(f'Erreur lors de l\'analyse des données: {str(e)}')
            import traceback
            traceback.print_exc()
            return False

    # Convertit les données en dictionnaire
    def toDict(self):
        """
        Returns:
            Un dictionnaire contenant les valeurs des capteurs
        """
        return {
            'air_quality': self.air_quality,
            'distance': self.distance,
            'luminosity': self.luminosity,
            'uvIndex': self.uvIndex,
            'irValue': self.irValue,
            'temperature': self.temperature,
            'pressure': self.pressure,
            'humidity': self.humidity
        } 