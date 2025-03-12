import threading;
import random;
import serial;
from src.models.sensor import Sensor;
from src.database.connection import DatabaseConnection;

# Service pour la gestion des capteurs
class SensorService:
    def __init__(self):
        self.sensor = Sensor();
        self.db = DatabaseConnection();
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
                    self.db.insertSensorData(self.sensor.toDict());

            except Exception as e:
                print(f'Erreur lors de la lecture des données: {str(e)}');

    # Lit les données depuis le port série
    def _readSerialData(self):
        if self.serialPort and self.serialPort.inWaiting() > 0:
            dataReceived = self.serialPort.readline();
            decodedData = dataReceived.decode('utf-8').strip();
            self.sensor.updateFromStr(decodedData);

    # Génère des données de démonstration
    def _generateDemoData(self):
        self.sensor.airQuality = random.randint(50, 300);
        self.sensor.distance = random.uniform(0.5, 5.0);
        self.sensor.luminosity = random.randint(100, 1000);
        self.sensor.temperature = random.uniform(15, 35);
        self.sensor.pressure = random.randint(950, 1050);
        self.sensor.humidity = random.randint(20, 80);
        
    # Lit les données des capteurs et retourne une chaîne formatée
    def readData(self):
        if self.demoMode:
            self._generateDemoData();
            return f"AQ:{self.sensor.airQuality},DIST:{self.sensor.distance:.2f},LUM:{self.sensor.luminosity},TEMP:{self.sensor.temperature:.1f},HUM:{self.sensor.humidity},PRESS:{self.sensor.pressure}";
        elif self.serialPort:
            try:
                self._readSerialData();
                return f"AQ:{self.sensor.airQuality},DIST:{self.sensor.distance:.2f},LUM:{self.sensor.luminosity},TEMP:{self.sensor.temperature:.1f},HUM:{self.sensor.humidity},PRESS:{self.sensor.pressure}";
            except Exception as e:
                print(f"Erreur lors de la lecture des données: {str(e)}");
                return None;
        return None; 