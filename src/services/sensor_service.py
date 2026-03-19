import threading;
import random;
import serial;
from src.models.sensor import Sensor;
from src.database.connection import DatabaseConnection;
from src.database.query_manager import QueryManager;

# Service pour la gestion des capteurs
class SensorService:
    def __init__(self):
        self.sensor = Sensor();
        self.db = DatabaseConnection();
        self.queryManager = None;
        if self.db.isConnected():
            self.queryManager = QueryManager(self.db);
        self.running = False;
        self.demoMode = False;
        self.dataThread = None;
        self.onDataUpdate = None;  # Callback pour la mise à jour de l'interface
        self.serialPort = None;
        self.portName = None;

    # Vérifie si le service est connecté à un port série
    def isConnected(self):
        """
        Returns:
            True si le service est connecté à un port série, False sinon
        """
        return self.serialPort is not None and not self.demoMode;
    
    # Vérifie si le service est disponible (connecté ou en mode démo)
    def isAvailable(self):
        """
        Returns:
            True si le service est disponible (connecté ou en mode démo), False sinon
        """
        return self.isConnected() or self.demoMode;

    # Se connecte à un port série
    def connect(self, portName, baudrate=9600):
        try:
            self.serialPort = serial.Serial(portName, baudrate);
            self.portName = portName;
            # Attendre que le port soit prêt
            import time
            time.sleep(2)  # Donner du temps à Arduino/Xbee pour s'initialiser
            # Vider le buffer d'entrée
            if self.serialPort:
                self.serialPort.reset_input_buffer()
            return True;
        except Exception as e:
            print(f"Erreur lors de la connexion au port {portName}: {str(e)}");
            self.serialPort = None;
            self.portName = None;
            return False;
    
    # Se déconnecte du port série
    def disconnect(self):
        if self.serialPort:
            try:
                self.stop();
                self.serialPort.close();
                self.serialPort = None;
                self.portName = None;
                return True;
            except Exception as e:
                print(f"Erreur lors de la déconnexion: {str(e)}");
                return False;
        return True;
    
    # Retourne le nom du port série connecté
    def getPort(self):
        return self.portName;
    
    # Démarre la lecture des données des capteurs
    def start(self, serialPort=None):
        if serialPort:
            self.serialPort = serialPort;
            self.demoMode = False;
        else:
            self.demoMode = True;

        self.running = True;
        self.dataThread = threading.Thread(target=self._readDataThread);
        self.dataThread.daemon = True;
        self.dataThread.start();
 
    # Arrête la lecture des données
    def stop(self):
        self.running = False;
        if self.dataThread:
            self.dataThread.join();

    # Thread de lecture des données
    def _readDataThread(self):
        while self.running:
            try:
                if self.demoMode:
                    self._generateDemoData();
                else:
                    self._readSerialData();

                # Mise à jour de l'interface via le callback
                if self.onDataUpdate:
                    self.onDataUpdate(self.sensor.toDict());

                # Sauvegarde dans la base de données
                if self.db.isConnected():
                    if self.queryManager is None:
                        self.queryManager = QueryManager(self.db);
                    
                    # Créer un dictionnaire avec le timestamp actuel
                    from datetime import datetime
                    data = self.sensor.toDict();
                    data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S');
                    
                    # Insérer les données
                    self.queryManager.insertSensorData(data);

            except Exception as e:
                print(f'Erreur lors de la lecture des données: {str(e)}');

    # Lit les données depuis le port série
    def _readSerialData(self):
        try:
            if self.serialPort:
                # Vérifier si des données sont disponibles
                try:
                    available_bytes = self.serialPort.in_waiting
                except AttributeError:
                    available_bytes = self.serialPort.inWaiting()
                
                if available_bytes > 0:
                    print(f"Données disponibles sur le port série: {available_bytes} octets")
                    # Lire toutes les données disponibles
                    lines_read = 0
                    max_lines = 20  # Augmenté pour capturer plus de lignes par cycle
                    
                    collected_data = []  # Pour collecter toutes les lignes de données valides
                    
                    while available_bytes > 0 and lines_read < max_lines:
                        # Lire une ligne complète
                        dataReceived = self.serialPort.readline()
                        if not dataReceived:
                            break
                            
                        decodedData = dataReceived.decode('utf-8', errors='replace').strip()
                        lines_read += 1
                        
                        if not decodedData:
                            continue
                            
                        print(f"Données reçues du port série: '{decodedData}'")
                        
                        # Ignorer les lignes qui contiennent seulement des tirets (séparateurs)
                        if decodedData.strip('-') == '':
                            continue
                            
                        # Ignorer les lignes spéciales comme "Fin des lectures" ou "Réactualisation dans X secondes"
                        if "Fin des lectures" in decodedData or "Réactualisation" in decodedData or "👾" in decodedData:
                            print(f"Ligne de contrôle ignorée: {decodedData}")
                            continue
                            
                        # Nettoyer les données en supprimant le préfixe "Message envoyé :" si présent
                        if "Message envoyé" in decodedData or "Message envoy" in decodedData:
                            cleanedData = decodedData
                            for prefix in ["Message envoyé :", "Message envoyÃ© :", "Message envoy :"]:
                                cleanedData = cleanedData.replace(prefix, "").strip()
                            print(f"Données nettoyées: '{cleanedData}'")
                            decodedData = cleanedData
                        
                        # Ajouter à notre collection de données si non vide
                        if decodedData and not decodedData.isspace():
                            collected_data.append(decodedData)
                        
                        # Vérifier s'il y a encore des données disponibles
                        try:
                            available_bytes = self.serialPort.in_waiting
                        except AttributeError:
                            available_bytes = self.serialPort.inWaiting()
                    
                    print(f"Nombre total de lignes traitées: {lines_read}")
                    
                    # Traiter les données collectées
                    if collected_data:
                        # Priorité aux messages spécifiques SI1145-Visible, MQ135-Air Quality, HC-SR04-Distance et BME680
                        visible_data = None
                        air_quality_data = None
                        distance_data = None
                        mq135_raw_data = None
                        bme680_temp_data = None
                        bme680_press_data = None
                        bme680_hum_data = None
                        gps_lat_data = None
                        gps_lon_data = None
                        gps_alt_data = None
                        
                        # Identifier d'abord les messages importants
                        for data_line in collected_data:
                            # Données luminosité SI1145
                            if "SI1145" in data_line and "Visible" in data_line:
                                visible_data = data_line
                                print(f"Données SI1145-Visible détectées: {visible_data}")
                            
                            # Données Air Quality MQ135
                            if "MQ135" in data_line and "Air Quality" in data_line:
                                air_quality_data = data_line
                                print(f"Données MQ135-Air Quality détectées: {air_quality_data}")
                            
                            # Données MQ135 brutes
                            if "MQ135" in data_line and "Valeur" in data_line:
                                mq135_raw_data = data_line
                                print(f"Données MQ135 brutes détectées: {mq135_raw_data}")
                            
                            # Données distance HC-SR04
                            if "HC_SR04" in data_line and "Distance" in data_line:
                                distance_data = data_line
                                print(f"Données HC-SR04 Distance détectées: {distance_data}")
                            
                            # Données BME680
                            if "BME680" in data_line:
                                if "Temperature" in data_line:
                                    bme680_temp_data = data_line
                                    print(f"Données BME680-Temperature détectées: {bme680_temp_data}")
                                elif "Pression" in data_line:
                                    bme680_press_data = data_line
                                    print(f"Données BME680-Pression détectées: {bme680_press_data}")
                                elif "Humidité" in data_line or "Humidite" in data_line:
                                    bme680_hum_data = data_line
                                    print(f"Données BME680-Humidité détectées: {bme680_hum_data}")
                            
                            # Données GPS
                            if "GPS" in data_line:
                                if "Latitude" in data_line:
                                    gps_lat_data = data_line
                                    print(f"Données GPS-Latitude détectées: {gps_lat_data}")
                                elif "Longitude" in data_line:
                                    gps_lon_data = data_line
                                    print(f"Données GPS-Longitude détectées: {gps_lon_data}")
                                elif "Altitude" in data_line:
                                    gps_alt_data = data_line
                                    print(f"Données GPS-Altitude détectées: {gps_alt_data}")
                                elif "Recherche de position" in data_line:
                                    print("GPS en cours de recherche de position...")
                        
                        # Traiter en priorité les données importantes
                        # SI1145 - Visible
                        if visible_data:
                            updateSuccess = self.sensor.updateFromStr(visible_data)
                            if updateSuccess:
                                print(f"Luminosité mise à jour avec succès: {self.sensor.luminosity}")
                            else:
                                print(f"Échec de mise à jour de la luminosité avec: {visible_data}")
                        
                        # MQ135 - Air Quality spécifique
                        if air_quality_data:
                            updateSuccess = self.sensor.updateFromStr(air_quality_data)
                            if updateSuccess:
                                print(f"Air Quality mis à jour avec succès: {self.sensor.air_quality}")
                            else:
                                print(f"Échec de mise à jour de l'Air Quality avec: {air_quality_data}")
                        
                        # MQ135 - Valeur brute (fallback pour Air Quality)
                        if mq135_raw_data and not air_quality_data:
                            updateSuccess = self.sensor.updateFromStr(mq135_raw_data)
                            if updateSuccess:
                                print(f"Air Quality estimés depuis MQ135 brut: Air Quality={self.sensor.air_quality}")
                            else:
                                print(f"Échec de mise à jour Air Quality depuis valeur brute avec: {mq135_raw_data}")
                        
                        # HC-SR04 - Distance
                        if distance_data:
                            updateSuccess = self.sensor.updateFromStr(distance_data)
                            if updateSuccess:
                                print(f"Distance mise à jour avec succès: {self.sensor.distance}")
                            else:
                                print(f"Échec de mise à jour de la distance avec: {distance_data}")
                        
                        # BME680 - Température
                        if bme680_temp_data:
                            updateSuccess = self.sensor.updateFromStr(bme680_temp_data)
                            if updateSuccess:
                                print(f"Température BME680 mise à jour avec succès: {self.sensor.temperature}")
                            else:
                                print(f"Échec de mise à jour de la température avec: {bme680_temp_data}")
                                
                        # BME680 - Pression
                        if bme680_press_data:
                            updateSuccess = self.sensor.updateFromStr(bme680_press_data)
                            if updateSuccess:
                                print(f"Pression BME680 mise à jour avec succès: {self.sensor.pressure}")
                            else:
                                print(f"Échec de mise à jour de la pression avec: {bme680_press_data}")
                                
                        # BME680 - Humidité
                        if bme680_hum_data:
                            updateSuccess = self.sensor.updateFromStr(bme680_hum_data)
                            if updateSuccess:
                                print(f"Humidité BME680 mise à jour avec succès: {self.sensor.humidity}")
                            else:
                                print(f"Échec de mise à jour de l'humidité avec: {bme680_hum_data}")
                        
                        # GPS - Latitude
                        if gps_lat_data:
                            updateSuccess = self.sensor.updateFromStr(gps_lat_data)
                            if updateSuccess:
                                print(f"Latitude GPS mise à jour avec succès: {self.sensor.latitude}")
                            else:
                                print(f"Échec de mise à jour de la latitude avec: {gps_lat_data}")
                        
                        # GPS - Longitude
                        if gps_lon_data:
                            updateSuccess = self.sensor.updateFromStr(gps_lon_data)
                            if updateSuccess:
                                print(f"Longitude GPS mise à jour avec succès: {self.sensor.longitude}")
                            else:
                                print(f"Échec de mise à jour de la longitude avec: {gps_lon_data}")
                        
                        # GPS - Altitude
                        if gps_alt_data:
                            updateSuccess = self.sensor.updateFromStr(gps_alt_data)
                            if updateSuccess:
                                print(f"Altitude GPS mise à jour avec succès: {self.sensor.altitude}")
                            else:
                                print(f"Échec de mise à jour de l'altitude avec: {gps_alt_data}")
                        
                        # Traiter ensuite les autres données
                        for data_line in collected_data:
                            # Ne pas retraiter les données spécifiques
                            if (data_line != visible_data and data_line != air_quality_data and
                                data_line != bme680_temp_data and data_line != bme680_press_data and
                                data_line != bme680_hum_data and data_line != distance_data and
                                data_line != mq135_raw_data and data_line != gps_lat_data and
                                data_line != gps_lon_data and data_line != gps_alt_data):
                                updateSuccess = self.sensor.updateFromStr(data_line)
                                if updateSuccess:
                                    print(f"Autres données capteurs mises à jour: {self.sensor.toDict()}")
                else:
                    # Attendre un court instant et réessayer
                    import time
                    time.sleep(0.1)  # Attendre 100ms
            else:
                print("Port série non disponible")
        except Exception as e:
            print(f"Erreur lors de la lecture des données série: {str(e)}")
            import traceback
            traceback.print_exc()

    # Génère des données de démonstration
    def _generateDemoData(self):
        # Des valeurs réalistes pour la démo
        # D'abord générer AQ
        self.sensor.air_quality = random.uniform(400, 1200);  # Air Quality en ppm
        
        self.sensor.distance = random.uniform(0.5, 5.0);
        self.sensor.luminosity = random.randint(200, 2000);  # Échelle Visible
        self.sensor.temperature = random.uniform(15, 35);
        self.sensor.pressure = random.randint(980, 1020);
        self.sensor.humidity = random.randint(20, 80);
        
        # Afficher les valeurs générées pour le débogage
        print(f"Demo data généré: Air Quality={self.sensor.air_quality} ppm")
        print(f"luminosity={self.sensor.luminosity}, temperature={self.sensor.temperature}, " +
              f"humidity={self.sensor.humidity}, pressure={self.sensor.pressure}")

    # Force la lecture même si aucune donnée n'est disponible
    def forceReadSerial(self, timeout=1.0):
        if not self.serialPort:
            print("Port série non disponible pour la lecture forcée")
            return False
            
        try:
            # Sauvegarder le timeout actuel
            old_timeout = self.serialPort.timeout
            
            # Définir un nouveau timeout
            self.serialPort.timeout = timeout
            
            # Lire les données
            dataReceived = self.serialPort.readline()
            if dataReceived:
                decodedData = dataReceived.decode('utf-8', errors='replace').strip()
                print(f"Données reçues en lecture forcée: {decodedData}")
                
                # Ignorer les lignes spéciales comme "Fin des lectures" ou "Réactualisation dans X secondes"
                if "Fin des lectures" in decodedData or "Réactualisation" in decodedData or "👾" in decodedData:
                    print(f"Ligne de contrôle ignorée en lecture forcée: {decodedData}")
                    # Restaurer le timeout d'origine
                    self.serialPort.timeout = old_timeout
                    return False
                
                # Nettoyer les données en supprimant le préfixe "Message envoyé :" si présent
                if "Message envoyé" in decodedData or "Message envoy" in decodedData:
                    cleanedData = decodedData
                    for prefix in ["Message envoyé :", "Message envoyÃ© :", "Message envoy :"]:
                        cleanedData = cleanedData.replace(prefix, "").strip()
                    print(f"Données nettoyées: {cleanedData}")
                    decodedData = cleanedData
                
                # Mettre à jour les valeurs du capteur
                if decodedData and not decodedData.isspace():
                    updateSuccess = self.sensor.updateFromStr(decodedData)
                    if updateSuccess:
                        print(f"Valeurs du capteur mises à jour: {self.sensor.toDict()}")
                        # Restaurer le timeout d'origine
                        self.serialPort.timeout = old_timeout
                        return True
            else:
                print("Aucune donnée reçue lors de la lecture forcée")
                
            # Restaurer le timeout d'origine
            self.serialPort.timeout = old_timeout
            return False
            
        except Exception as e:
            print(f"Erreur lors de la lecture forcée: {str(e)}")
            return False

    # Envoie une commande pour demander des données
    def requestData(self, command='DATA'):
        """
        Envoie une commande au port série pour demander des données.
        Certains dispositifs (Arduino/XBee) attendent une commande pour envoyer des données.
        
        Args:
            command: La commande à envoyer (par défaut 'DATA')
            
        Returns:
            True si la commande a été envoyée, False sinon
        """
        if not self.serialPort:
            print("Port série non disponible pour l'envoi de commande")
            return False
            
        try:
            # Assurer que la commande se termine par un retour à la ligne
            if not command.endswith('\n'):
                command += '\n'
                
            # Envoyer la commande encodée en bytes
            self.serialPort.write(command.encode('utf-8'))
            self.serialPort.flush()  # S'assurer que les données sont envoyées
            print(f"Commande '{command.strip()}' envoyée sur le port série")
            
            # Attendre un court instant pour que l'appareil traite la commande
            import time
            time.sleep(0.5)
            
            return True
        except Exception as e:
            print(f"Erreur lors de l'envoi de la commande: {str(e)}")
            return False

    # Lit les données des capteurs et retourne une chaîne formatée
    def readData(self):
        if self.demoMode:
            # Générer des données de démo
            self._generateDemoData();
            # Inclure les mesures de AQ
            data = f"AQ:{self.sensor.air_quality:.2f},DIST:{self.sensor.distance:.2f},LUM:{self.sensor.luminosity},TEMP:{self.sensor.temperature:.1f},HUM:{self.sensor.humidity},PRESS:{self.sensor.pressure}";
            print(f"Données générées en mode démo: {data}")
            return data
        elif self.serialPort:
            try:
                # Enregistrer l'état initial des capteurs
                initial_state = self.sensor.toDict().copy()
                
                # Demander des données et lire les réponses
                self.requestData()
                self._readSerialData()
                
                # Vérifier si des données ont été mises à jour
                current_state = self.sensor.toDict()
                changed = False
                
                for key, value in current_state.items():
                    if initial_state[key] != value:
                        changed = True
                        print(f"Valeur changée: {key} = {value} (avant: {initial_state[key]})")
                
                # Si aucune valeur n'a changé, essayer une lecture forcée
                if not changed:
                    print("Aucune valeur n'a été mise à jour, tentative de lecture forcée")
                    if not self.forceReadSerial():
                        print("Lecture forcée échouée")
                        # Vérifier si nous avons au moins certaines valeurs non-nulles
                        if all(v is None for v in current_state.values()):
                            return None
                
                # Construire une chaîne complète formatée avec toutes les valeurs connues
                # C'est important pour le contrôleur qui utilisera ces données pour l'interface
                formatted_values = []
                
                # Ajouter chaque valeur disponible (non nulle)
                if self.sensor.air_quality is not None:
                    formatted_values.append(f"AQ:{self.sensor.air_quality:.2f}")
                
                if self.sensor.distance is not None:
                    formatted_values.append(f"DIST:{self.sensor.distance:.2f}")
                    
                if self.sensor.luminosity is not None:
                    formatted_values.append(f"LUM:{self.sensor.luminosity}")
                    
                if self.sensor.uvIndex is not None:
                    formatted_values.append(f"UV:{self.sensor.uvIndex:.2f}")
                    
                if self.sensor.irValue is not None:
                    formatted_values.append(f"IR:{self.sensor.irValue}")
                    
                if self.sensor.temperature is not None:
                    formatted_values.append(f"TEMP:{self.sensor.temperature:.1f}")
                    
                if self.sensor.humidity is not None:
                    formatted_values.append(f"HUM:{self.sensor.humidity}")
                    
                if self.sensor.pressure is not None:
                    formatted_values.append(f"PRESS:{self.sensor.pressure}")
                
                if self.sensor.gas is not None:
                    formatted_values.append(f"GAS:{self.sensor.gas:.2f}")
                
                if self.sensor.latitude is not None:
                    formatted_values.append(f"LAT:{self.sensor.latitude:.6f}")
                
                if self.sensor.longitude is not None:
                    formatted_values.append(f"LON:{self.sensor.longitude:.6f}")
                
                if self.sensor.altitude is not None:
                    formatted_values.append(f"ALT:{self.sensor.altitude:.2f}")
                
                # Joindre toutes les valeurs formatées
                formattedData = ",".join(formatted_values)
                
                if not formattedData:
                    print("Aucune donnée formatée disponible")
                    return None
                    
                print(f"Données formatées retournées: {formattedData}")
                return formattedData
            except Exception as e:
                print(f"Erreur lors de la lecture des données: {str(e)}")
                import traceback
                traceback.print_exc()
                return None
        return None 