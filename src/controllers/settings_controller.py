import serial.tools.list_ports

# Contrôleur pour la gestion des paramètres de l'application
class SettingsController:
    # Initialise le contrôleur des paramètres
    def __init__(self, view, dbConnection, sensorService):
        """
        Args:
            view: La vue des paramètres
            dbConnection: La connexion à la base de données
            sensorService: Le service de capteurs
        """
        self.view = view
        self.dbConnection = dbConnection
        self.sensorService = sensorService
        
        # Initialiser l'état des connexions
        self.updateConnectionStatus()
        
        # Rafraîchir la liste des ports
        self.refreshPorts()
    
    # Met à jour le statut des connexions
    def updateConnectionStatus(self):
        # Mettre à jour le statut de la connexion série
        self.view.updateSerialStatus(
            self.sensorService.isConnected(),
            self.sensorService.getPort() if self.sensorService.isConnected() else None
        )
        
        # Mettre à jour le statut de la connexion à la base de données
        self.view.updateDbStatus(
            self.dbConnection.isConnected(),
            self.dbConnection.getDatabaseName() if self.dbConnection.isConnected() else None
        )
    
    # Rafraîchit la liste des ports série disponibles
    def refreshPorts(self):
        ports = self.getAvailablePorts()
        self.view.updatePortsList(ports)
    
    # Récupère la liste des ports série disponibles
    def getAvailablePorts(self):
        """      
        Returns:
            Une liste des ports disponibles
        """
        ports = []
        try:
            # Utiliser pyserial pour lister les ports
            ports = [port.device for port in serial.tools.list_ports.comports()]
        except Exception as e:
            print(f"Erreur lors de la récupération des ports: {str(e)}")
        
        return ports
    
    # Se connecte ou se déconnecte du port série sélectionné
    def connectToPort(self):
        if self.sensorService.isConnected():
            # Déconnexion
            self.sensorService.disconnect()
            self.view.updateSerialStatus(False)
        else:
            # Connexion
            port = self.view.selectedPort.get()
            if port:
                success = self.sensorService.connect(port)
                self.view.updateSerialStatus(success, port if success else None)
            else:
                print("Aucun port sélectionné")
    
    # Se connecte à la base de données avec les paramètres fournis
    def connectToDb(self):
        if self.dbConnection.isConnected():
            print("Déjà connecté à la base de données")
            return
        
        # Récupérer la configuration de la base de données
        dbConfig = self.view.getDbConfig()
        
        # Se connecter à la base de données
        success = self.dbConnection.connect(
            host=dbConfig['host'],
            user=dbConfig['user'],
            password=dbConfig['password'],
            database=dbConfig['database']
        )
        
        # Mettre à jour l'affichage
        self.view.updateDbStatus(success, dbConfig['database'] if success else None)
    
    # Se déconnecte de la base de données
    def disconnectFromDb(self):
        if not self.dbConnection.isConnected():
            print("Pas de connexion à la base de données")
            return
        
        # Se déconnecter de la base de données
        self.dbConnection.disconnect()
        
        # Mettre à jour l'affichage
        self.view.updateDbStatus(False) 