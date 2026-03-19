import mysql.connector;
import logging;
from config.settings import DB_CONFIG;

# Configuration du logger
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('database_connection.log'),
        logging.StreamHandler()
    ]
);
logger = logging.getLogger('DatabaseConnection');

# Connexion à la base de données
class DatabaseConnection:
    def __init__(self):
        self.connection = None;
        self.cursor = None;
        self._isConnected = False;
        self.errorMessage = '';
        self.dbConfig = DB_CONFIG.copy();
        
        logger.info("=== INITIALISATION DE LA CONNEXION ===");
        logger.debug(f"Configuration: host={self.dbConfig.get('host')}, user={self.dbConfig.get('user')}, database={self.dbConfig.get('database')}");
        
        # Tenter une connexion initiale avec les paramètres par défaut
        try:
            self.connect();
        except Exception as e:
            self.errorMessage = str(e);
            logger.error(f"Erreur lors de la connexion initiale: {str(e)}", exc_info=True);
            self._isConnected = False;

    # Établit la connexion à la base de données
    def connect(self, host=None, user=None, password=None, database=None):
        logger.info("=== TENTATIVE DE CONNEXION ===");
        
        try:
            # Mettre à jour la configuration si des paramètres sont fournis
            if host:
                logger.debug(f"Mise à jour host: {self.dbConfig.get('host')} -> {host}");
                self.dbConfig['host'] = host;
            if user:
                logger.debug(f"Mise à jour user: {self.dbConfig.get('user')} -> {user}");
                self.dbConfig['user'] = user;
            if password:
                logger.debug("Mise à jour password: ***");
                self.dbConfig['password'] = password;
            if database:
                logger.debug(f"Mise à jour database: {self.dbConfig.get('database')} -> {database}");
                self.dbConfig['database'] = database;
            
            logger.info(f"Connexion vers: {self.dbConfig.get('user')}@{self.dbConfig.get('host')}:{self.dbConfig.get('port', 3306)}/{self.dbConfig.get('database')}");
            logger.debug("Tentative de connexion avec mysql.connector...");
            
            self.connection = mysql.connector.connect(**self.dbConfig);
            
            logger.debug("Objet connection créé avec succès");
            logger.debug(f"Type de connexion: {type(self.connection)}");
            
            self.cursor = self.connection.cursor();
            logger.debug("Curseur créé avec succès");
            
            self._isConnected = True;
            self.errorMessage = '';
            
            logger.info(f"✓ CONNEXION RÉUSSIE à {self.dbConfig.get('database')} sur {self.dbConfig.get('host')}");
            return True;
            
        except mysql.connector.errors.ProgrammingError as e:
            self._isConnected = False;
            self.errorMessage = str(e);
            logger.error(f"✗ Erreur de programmation MySQL: {str(e)}");
            logger.error("Vérifiez le nom de la base de données");
            return False;
            
        except mysql.connector.errors.DatabaseError as e:
            self._isConnected = False;
            self.errorMessage = str(e);
            logger.error(f"✗ Erreur de base de données: {str(e)}");
            logger.error("Vérifiez que le serveur MySQL est accessible");
            return False;
            
        except mysql.connector.errors.InterfaceError as e:
            self._isConnected = False;
            self.errorMessage = str(e);
            logger.error(f"✗ Erreur d'interface MySQL: {str(e)}");
            logger.error("Le serveur MySQL ne répond pas ou n'est pas accessible");
            return False;
            
        except Exception as e:
            self._isConnected = False;
            self.errorMessage = str(e);
            logger.error(f"✗ ERREUR DE CONNEXION: {type(e).__name__}: {str(e)}", exc_info=True);
            logger.error(f"Config utilisée: host={self.dbConfig.get('host')}, user={self.dbConfig.get('user')}, database={self.dbConfig.get('database')}");
            return False;
    
    # Ferme la connexion à la base de données
    def disconnect(self):
        logger.info("Fermeture de la connexion...");
        if self.cursor:
            self.cursor.close();
            logger.debug("Curseur fermé");
        if self.connection:
            self.connection.close();
            logger.debug("Connexion fermée");
        self._isConnected = False;
        logger.info("Déconnexion terminée");
        
    # Vérifie si la connexion à la base de données est établie
    def isConnected(self):
        if self.connection is None:
            logger.debug("Vérification connexion: connection est None");
            self._isConnected = False;
            return False;
            
        try:
            # Vérifier si la connexion est toujours active en utilisant la méthode appropriée
            # MySQLConnection utilise is_connected() et non isConnected()
            if hasattr(self.connection, 'is_connected'):
                is_connected = self.connection.is_connected();
                logger.debug(f"Vérification connexion via is_connected(): {is_connected}");
            else:
                # Utilisation de ping comme fallback
                logger.debug("Vérification connexion via ping()");
                self.connection.ping(reconnect=False, attempts=1, delay=0);
                is_connected = True;
                
            self._isConnected = is_connected;
            return is_connected;
        except Exception as e:
            logger.warning(f"Erreur lors de la vérification de la connexion: {str(e)}");
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