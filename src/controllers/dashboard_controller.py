import threading
import random
import time
from datetime import datetime

# Controller pour le tableau de bord
class DashboardController:

    # Initialisation du contrôleur
    def __init__(self, view, sensorService, dbConnection):
        """
        Args:
            view: La vue du tableau de bord
            sensorService: Le service de capteurs
            dbConnection: La connexion à la base de données
        """
        self.view = view
        self.sensorService = sensorService
        self.dbConnection = dbConnection
        
        # Variables pour le thread de lecture
        self.readingThread = None
        self.stopThread = threading.Event()
        self.running = False
        
        # Variables pour le mode démo
        self.demoActive = False
        self.demoThread = None
        
        # Dernières valeurs des capteurs
        self.latestData = {
            'co2': 'N/A',
            'nh3': 'N/A',
            'distance': 'N/A',
            'luminosity': 'N/A',
            'uv_index': 'N/A',
            'ir_value': 'N/A',
            'temperature': 'N/A',
            'humidity': 'N/A',
            'pressure': 'N/A'
        }
        
        # Créer un gestionnaire de requêtes si la connexion est établie
        if hasattr(dbConnection, 'isConnected') and dbConnection.isConnected():
            from src.database.query_manager import QueryManager
            self.queryManager = QueryManager(dbConnection)
        else:
            self.queryManager = None
    
    # Démarre la lecture des données des capteurs
    def startDataReading(self):
        if self.running:
            return
            
        self.running = True
        self.stopThread.clear()
        
        # Créer et démarrer le thread de lecture
        self.readingThread = threading.Thread(target=self.readDataThread)
        self.readingThread.daemon = True
        self.readingThread.start()
        
        self.view.logToConsole("Lecture des données démarrée")

    # Arrête la lecture des données des capteurs
    def stopDataReading(self):
        if not self.running:
            return
            
        self.running = False
        self.stopThread.set()
        
        # Attendre que le thread se termine
        if self.readingThread:
            self.readingThread.join(timeout=1.0)
            self.readingThread = None
        
        self.view.logToConsole("Lecture des données arrêtée")
    
    # Active ou désactive le mode démo
    def toggleDemoMode(self):
        self.demoActive = not self.demoActive
        
        if self.demoActive:
            # Arrêter la lecture normale si elle est en cours
            self.stopDataReading()
            
            # Démarrer le thread de démo
            self.demoThread = threading.Thread(target=self.updateValuesDemo)
            self.demoThread.daemon = True
            self.demoThread.start()
            
            self.view.logToConsole("Mode démo activé")
        else:
            # Arrêter le thread de démo
            self.stopThread.set()
            if self.demoThread:
                self.demoThread.join(timeout=1.0)
                self.demoThread = None
            self.stopThread.clear()
            
            self.view.logToConsole("Mode démo désactivé")
    
    # Met à jour les valeurs des capteurs en mode démo
    def updateValuesDemo(self):
        while not self.stopThread.is_set() and self.demoActive:
            try:
                # Générer des valeurs aléatoires pour les capteurs
                demoData = {
                    'co2': round(random.uniform(400, 1200), 2),
                    'nh3': round(random.uniform(5, 25), 2),
                    'distance': round(random.uniform(0.5, 5.0), 2),
                    'luminosity': random.randint(200, 2000),
                    'uv_index': round(random.uniform(0.1, 10.0), 2),
                    'ir_value': random.randint(200, 800),
                    'temperature': round(random.uniform(15, 35), 1),
                    'humidity': random.randint(20, 80),
                    'pressure': random.randint(980, 1020)
                }
                
                self.view.logToConsole(f"Données de démo générées: {demoData}")
                
                # Mettre à jour les valeurs dans la vue
                self.view.updateSensorValues(demoData)
                
                # Mettre à jour les dernières valeurs
                self.latestData = demoData
                
                # Enregistrer les données dans la base de données si connecté
                if hasattr(self.dbConnection, 'isConnected') and self.dbConnection.isConnected():
                    try:
                        self.view.logToConsole(f"Tentative d'envoi des données de démo pour enregistrement...")
                        
                        # Préparer les données pour l'insertion
                        data_with_timestamp = demoData.copy()
                        data_with_timestamp['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        
                        # S'assurer que le gestionnaire de requêtes existe
                        if self.queryManager is None:
                            from src.database.query_manager import QueryManager
                            self.queryManager = QueryManager(self.dbConnection)
                        
                        # Insérer les données
                        success = self.queryManager.insertSensorData(data_with_timestamp)
                        
                        if success:
                            self.view.logToConsole(f"Données enregistrées dans la base de données à {data_with_timestamp['timestamp']}")
                            self.view.logToConsole(f"Données de démo envoyées pour enregistrement avec succès")
                        else:
                            self.view.logToConsole("Erreur lors de l'enregistrement des données de démo")
                    except Exception as e:
                        self.view.logToConsole(f"Erreur lors de l'envoi des données de démo: {str(e)}")
                else:
                    self.view.logToConsole("Base de données non connectée - Impossible d'enregistrer les données de démo")
            except Exception as e:
                self.view.logToConsole(f"Erreur lors de la génération/traitement des données de démo: {str(e)}")
            
            # Attendre avant la prochaine mise à jour
            time.sleep(2)
    
    def readDataThread(self):
        """
        Thread de lecture des données des capteurs.
        """
        while not self.stopThread.is_set() and self.running:
            try:
                # Lire les données des capteurs
                dataString = self.sensorService.readData()
                
                if dataString:
                    # Parser les données
                    data = self.parseSensorData(dataString)
                    
                    # Ne mettre à jour que si on a obtenu des données
                    if data:
                        # Mettre à jour les valeurs dans la vue
                        self.view.updateSensorValues(data)
                        
                        # Mettre à jour les dernières valeurs
                        self.latestData = data
                        
                        # Enregistrer les données dans la base de données si connecté
                        if hasattr(self.dbConnection, 'isConnected') and self.dbConnection.isConnected():
                            # Ajouter un timestamp aux données
                            data_with_timestamp = data.copy()
                            data_with_timestamp['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            
                            # Utiliser le gestionnaire de requêtes pour insérer les données
                            if self.queryManager is None:
                                from src.database.query_manager import QueryManager
                                self.queryManager = QueryManager(self.dbConnection)
                                
                            self.queryManager.insertSensorData(data_with_timestamp)
                            self.view.logToConsole(f"Données enregistrées dans la base de données à {data_with_timestamp['timestamp']}")
                            self.view.logToConsole(f"Données du capteur envoyées pour enregistrement")
                        
                        # Afficher les données dans la console
                        self.view.logToConsole(f"Données traitées: {data}")
                    else:
                        self.view.logToConsole("Aucune donnée n'a pu être extraite du message reçu")
                else:
                    # Cas où aucune donnée n'a été reçue
                    # On peut utiliser directement les données du service de capteur
                    if hasattr(self.sensorService, 'sensor'):
                        sensor_data = self.sensorService.sensor.toDict()
                        # Partir des dernières valeurs connues
                        data = self.latestData.copy()
                        
                        # Mettre à jour avec les nouvelles valeurs non nulles
                        has_updated = False
                        
                        # Mise à jour des valeurs
                        if sensor_data.get('co2') is not None:
                            data['co2'] = sensor_data.get('co2')
                            has_updated = True
                        if sensor_data.get('nh3') is not None:
                            data['nh3'] = sensor_data.get('nh3')
                            has_updated = True
                        if sensor_data.get('distance') is not None:
                            data['distance'] = sensor_data.get('distance')
                            has_updated = True
                        if sensor_data.get('luminosity') is not None:
                            data['luminosity'] = sensor_data.get('luminosity')
                            has_updated = True
                        if sensor_data.get('uvIndex') is not None:
                            data['uv_index'] = sensor_data.get('uvIndex')
                            has_updated = True
                        if sensor_data.get('irValue') is not None:
                            data['ir_value'] = sensor_data.get('irValue')
                            has_updated = True
                        if sensor_data.get('temperature') is not None:
                            data['temperature'] = sensor_data.get('temperature')
                            has_updated = True
                        if sensor_data.get('humidity') is not None:
                            data['humidity'] = sensor_data.get('humidity')
                            has_updated = True
                        if sensor_data.get('pressure') is not None:
                            data['pressure'] = sensor_data.get('pressure')
                            has_updated = True
                        
                        # Vérifier si on a des nouvelles valeurs
                        if has_updated:
                            # Mettre à jour les valeurs dans la vue
                            self.view.updateSensorValues(data)
                            
                            # Mettre à jour les dernières valeurs
                            self.latestData = data
                            
                            # Enregistrer les données dans la base de données
                            if hasattr(self.dbConnection, 'isConnected') and self.dbConnection.isConnected():
                                # Préparer les données pour l'insertion
                                data_with_timestamp = data.copy()
                                data_with_timestamp['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                
                                # S'assurer que le gestionnaire de requêtes existe
                                if self.queryManager is None:
                                    from src.database.query_manager import QueryManager
                                    self.queryManager = QueryManager(self.dbConnection)
                                
                                self.queryManager.insertSensorData(data_with_timestamp)
                                self.view.logToConsole(f"Données enregistrées dans la base de données à {data_with_timestamp['timestamp']}")
                                self.view.logToConsole(f"Données du capteur envoyées pour enregistrement (direct)")
                            
                            self.view.logToConsole(f"Données obtenues directement du capteur: {data}")
            except Exception as e:
                self.view.logToConsole(f"Erreur lors de la lecture des données: {str(e)}")
                import traceback
                traceback.print_exc()
            
            # Attendre avant la prochaine lecture
            time.sleep(1)
    
    # Parse les données reçues des capteurs
    def parseSensorData(self, dataString):
        """
        Parse les données reçues des capteurs.
        
        Args:
            dataString: Chaîne de caractères contenant les données
            
        Returns:
            Dictionnaire contenant les valeurs des capteurs
        """
        # Format possible: "CO2:8.94,NH3:17.29,DIST:1.5,LUM:500,TEMP:22.5,HUM:60,PRESS:1010"
        data = {}
        
        try:
            self.view.logToConsole(f"Parsing des données: {dataString}")
            
            # Si la chaîne est au format standard avec ':'
            if ':' in dataString:
                # Diviser la chaîne en paires clé-valeur
                pairs = dataString.strip().split(',')
                
                for pair in pairs:
                    if ':' in pair:
                        key, value = pair.split(':')
                        
                        # Convertir les clés en noms de variables
                        if key == 'CO2':
                            data['co2'] = float(value) if value and value.strip() else None
                        elif key == 'NH3':
                            data['nh3'] = float(value) if value and value.strip() else None
                        elif key == 'DIST':
                            data['distance'] = float(value) if value and value.strip() else None
                        elif key == 'LUM':
                            data['luminosity'] = int(value) if value and value.strip() else None
                        elif key == 'UV':
                            data['uv_index'] = float(value) if value and value.strip() else None
                        elif key == 'IR':
                            data['ir_value'] = int(value) if value and value.strip() else None
                        elif key == 'TEMP':
                            data['temperature'] = float(value) if value and value.strip() else None
                        elif key == 'HUM':
                            data['humidity'] = int(value) if value and value.strip() else None
                        elif key == 'PRESS':
                            data['pressure'] = int(value) if value and value.strip() else None
                
                # Si on a de nouvelles données, les fusionner avec les données existantes
                # Au lieu de remplacer complètement les anciennes valeurs
                if data:
                    # Copie profonde pour éviter de modifier les données existantes directement
                    merged_data = self.latestData.copy()
                    # Mettre à jour uniquement les clés présentes dans les nouvelles données
                    for key, value in data.items():
                        if value is not None:
                            merged_data[key] = value
                    # Utiliser les données fusionnées pour l'affichage et l'enregistrement
                    data = merged_data
                    
            # Format provenant directement de l'objet Sensor
            elif hasattr(self.sensorService, 'sensor'):
                sensor = self.sensorService.sensor
                sensor_dict = sensor.toDict()
                
                # Copie profonde des données existantes
                data = self.latestData.copy()
                
                # Convertir les noms de variables et mettre à jour uniquement les valeurs non nulles
                if 'co2' in sensor_dict and sensor_dict['co2'] is not None:
                    data['co2'] = sensor_dict['co2']
                if 'nh3' in sensor_dict and sensor_dict['nh3'] is not None:
                    data['nh3'] = sensor_dict['nh3']
                if 'distance' in sensor_dict and sensor_dict['distance'] is not None:
                    data['distance'] = sensor_dict['distance']
                if 'luminosity' in sensor_dict and sensor_dict['luminosity'] is not None:
                    data['luminosity'] = sensor_dict['luminosity']
                if 'uvIndex' in sensor_dict and sensor_dict['uvIndex'] is not None:
                    data['uv_index'] = sensor_dict['uvIndex']
                if 'irValue' in sensor_dict and sensor_dict['irValue'] is not None:
                    data['ir_value'] = sensor_dict['irValue']
                if 'temperature' in sensor_dict and sensor_dict['temperature'] is not None:
                    data['temperature'] = sensor_dict['temperature']
                if 'humidity' in sensor_dict and sensor_dict['humidity'] is not None:
                    data['humidity'] = sensor_dict['humidity']
                if 'pressure' in sensor_dict and sensor_dict['pressure'] is not None:
                    data['pressure'] = sensor_dict['pressure']
                
                self.view.logToConsole(f"Données extraites de l'objet sensor et fusionnées avec les précédentes: {data}")
            
            # Vérifier si des données ont été extraites, sinon utiliser directement l'objet sensor
            if not data and hasattr(self.sensorService, 'sensor'):
                sensor = self.sensorService.sensor
                # Créer un dictionnaire à partir des données existantes
                data = self.latestData.copy()
                
                # Ne pas ajouter une valeur si elle est None ou 0 (pourrait indiquer que le capteur n'a pas encore été mis à jour)
                if sensor.co2 is not None and sensor.co2 > 0:
                    data['co2'] = sensor.co2
                if sensor.nh3 is not None and sensor.nh3 > 0:
                    data['nh3'] = sensor.nh3
                if sensor.distance is not None and sensor.distance > 0:
                    data['distance'] = sensor.distance
                if sensor.luminosity is not None and sensor.luminosity > 0:
                    data['luminosity'] = sensor.luminosity
                if sensor.uvIndex is not None:
                    data['uv_index'] = sensor.uvIndex
                if sensor.irValue is not None and sensor.irValue > 0:
                    data['ir_value'] = sensor.irValue
                if sensor.temperature is not None:
                    data['temperature'] = sensor.temperature
                if sensor.humidity is not None and sensor.humidity > 0:
                    data['humidity'] = sensor.humidity
                if sensor.pressure is not None and sensor.pressure > 0:
                    data['pressure'] = sensor.pressure
                self.view.logToConsole(f"Données directement extraites de l'objet sensor et fusionnées: {data}")
                
            # Vérifier qu'il y a des données valides
            if data:
                # Vérifier si les valeurs sont des chaînes et les convertir
                for key in data:
                    if isinstance(data[key], str):
                        try:
                            if '.' in data[key]:
                                data[key] = float(data[key])
                            else:
                                data[key] = int(data[key])
                        except ValueError:
                            pass  # Laisser comme chaîne si la conversion échoue
                self.view.logToConsole(f"Données parsées avec succès: {data}")
            else:
                self.view.logToConsole("Aucune donnée n'a pu être extraite")
                
        except Exception as e:
            self.view.logToConsole(f"Erreur lors du parsing des données: {str(e)}")
            import traceback
            traceback.print_exc()
        
        return data
    
    # Retourne les dernières valeurs des capteurs
    def getLatestData(self):
        """   
        Returns:
            Dictionnaire contenant les dernières valeurs des capteurs
        """
        return self.latestData 