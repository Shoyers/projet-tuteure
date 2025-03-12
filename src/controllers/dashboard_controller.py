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
            'air_quality': 'N/A',
            'distance': 'N/A',
            'luminosity': 'N/A',
            'temperature': 'N/A',
            'humidity': 'N/A',
            'pressure': 'N/A'
        }
    
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
            # Générer des valeurs aléatoires pour les capteurs
            demoData = {
                'air_quality': random.randint(400, 1200),
                'distance': round(random.uniform(0.1, 5.0), 2),
                'luminosity': random.randint(100, 1000),
                'temperature': round(random.uniform(18.0, 28.0), 1),
                'humidity': random.randint(30, 80),
                'pressure': random.randint(980, 1020)
            }
            
            # Mettre à jour les valeurs dans la vue
            self.view.updateSensorValues(demoData)
            
            # Mettre à jour les dernières valeurs
            self.latestData = demoData
            
            # Enregistrer les données dans la base de données si connecté
            if self.dbConnection and self.dbConnection.isConnected():
                self.saveDataToDb(demoData)
            
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
                    
                    # Mettre à jour les valeurs dans la vue
                    self.view.updateSensorValues(data)
                    
                    # Mettre à jour les dernières valeurs
                    self.latestData = data
                    
                    # Enregistrer les données dans la base de données si connecté
                    if self.dbConnection and self.dbConnection.isConnected():
                        self.saveDataToDb(data)
                    
                    # Afficher les données dans la console
                    self.view.logToConsole(f"Données reçues: {dataString}")
            except Exception as e:
                self.view.logToConsole(f"Erreur lors de la lecture des données: {str(e)}")
            
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
        # Exemple de format: "AQ:800,DIST:1.5,LUM:500,TEMP:22.5,HUM:60,PRESS:1010"
        data = {}
        
        try:
            # Diviser la chaîne en paires clé-valeur
            pairs = dataString.strip().split(',')
            
            for pair in pairs:
                if ':' in pair:
                    key, value = pair.split(':')
                    
                    # Convertir les clés en noms de variables
                    if key == 'AQ':
                        data['air_quality'] = int(value)
                    elif key == 'DIST':
                        data['distance'] = float(value)
                    elif key == 'LUM':
                        data['luminosity'] = int(value)
                    elif key == 'TEMP':
                        data['temperature'] = float(value)
                    elif key == 'HUM':
                        data['humidity'] = int(value)
                    elif key == 'PRESS':
                        data['pressure'] = int(value)
        except Exception as e:
            self.view.logToConsole(f"Erreur lors du parsing des données: {str(e)}")
        
        return data
    
    # Enregistre les données dans la base de données
    def saveDataToDb(self, data):
        """   
        Args:
            data: Dictionnaire contenant les valeurs des capteurs
        """
        try:
            # Créer la requête SQL
            query = """
            INSERT INTO sensor_data 
            (timestamp, air_quality, distance, luminosity, temperature, pressure, humidity) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            # Préparer les valeurs
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            values = (
                timestamp,
                data.get('air_quality'),
                data.get('distance'),
                data.get('luminosity'),
                data.get('temperature'),
                data.get('pressure'),
                data.get('humidity')
            )
            
            # Exécuter la requête
            cursor = self.dbConnection.cursor()
            cursor.execute(query, values)
            self.dbConnection.commit()
            cursor.close()
            
            self.view.logToConsole(f"Données enregistrées dans la base de données à {timestamp}")
        except Exception as e:
            self.view.logToConsole(f"Erreur lors de l'enregistrement des données: {str(e)}")
    
    # Retourne les dernières valeurs des capteurs
    def getLatestData(self):
        """   
        Returns:
            Dictionnaire contenant les dernières valeurs des capteurs
        """
        return self.latestData 