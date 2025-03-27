import mysql.connector;
from config.settings import DB_CONFIG;

# Connexion à la base de données
class DatabaseConnection:
    def __init__(self):
        self.connection = None;
        self.cursor = None;
        self._isConnected = False;
        self.errorMessage = '';
        self.dbConfig = DB_CONFIG.copy();
        
        # Tenter une connexion initiale avec les paramètres par défaut
        try:
            self.connect();
        except Exception as e:
            self.errorMessage = str(e);
            print(f"Erreur lors de la connexion initiale à la base de données: {str(e)}");
            self._isConnected = False;

    # Établit la connexion à la base de données
    def connect(self, host=None, user=None, password=None, database=None):
        try:
            # Mettre à jour la configuration si des paramètres sont fournis
            if host:
                self.dbConfig['host'] = host;
            if user:
                self.dbConfig['user'] = user;
            if password:
                self.dbConfig['password'] = password;
            if database:
                self.dbConfig['database'] = database;
                
            self.connection = mysql.connector.connect(**self.dbConfig);
            self.cursor = self.connection.cursor();
            self._isConnected = True;
            self.errorMessage = '';
            print(f"Connexion établie à la base de données {self.dbConfig.get('database')} sur {self.dbConfig.get('host')}");
            return True;
        except Exception as e:
            self._isConnected = False;
            self.errorMessage = str(e);
            print(f"Erreur de connexion à la base de données: {str(e)}");
            return False;
    
    # Ferme la connexion à la base de données
    def disconnect(self):
        if self.cursor:
            self.cursor.close();
        if self.connection:
            self.connection.close();
        self._isConnected = False;
        
    # Vérifie si la connexion à la base de données est établie
    def isConnected(self):
        if self.connection is None:
            self._isConnected = False;
            return False;
            
        try:
            # Vérifier si la connexion est toujours active en utilisant la méthode appropriée
            # MySQLConnection utilise is_connected() et non isConnected()
            if hasattr(self.connection, 'is_connected'):
                is_connected = self.connection.is_connected()
            else:
                # Utilisation de ping comme fallback
                self.connection.ping(reconnect=False, attempts=1, delay=0);
                is_connected = True
                
            self._isConnected = is_connected
            return is_connected
        except Exception as e:
            print(f"Erreur lors de la vérification de la connexion: {str(e)}")
            self._isConnected = False;
            return False;
    
    # Retourne le nom de la base de données connectée
    def getDatabaseName(self):
        if self.isConnected():
            return self.dbConfig.get('database', 'Unknown');
        return None;
    
    # Insère les données des capteurs dans la base de données
    # NOTE: Cette méthode a été déplacée vers QueryManager
    # Veuillez utiliser QueryManager.insertSensorData à la place 