from datetime import datetime, timedelta
from src.models.sensor_data import SensorData

# Gestionnaire de requêtes SQL pour la base de données
class QueryManager:
    # Initialise le gestionnaire de requêtes
    def __init__(self, dbConnection):
        """        
        Args:
            dbConnection: La connexion à la base de données
        """
        self.dbConnection = dbConnection
    
    # Insère les données des capteurs dans la base de données
    def insertSensorData(self, sensorData):
        """
        Args:
            sensorData: Un objet SensorData ou un dictionnaire contenant les valeurs des capteurs
            
        Returns:
            True si l'insertion a réussi, False sinon
        """
        try:
            # Convertir en SensorData si c'est un dictionnaire
            if isinstance(sensorData, dict):
                sensorData = SensorData.fromDict(sensorData)
            
            # Créer la requête SQL
            query = """
            INSERT INTO sensor_data 
            (timestamp, air_quality, distance, luminosity, temperature, pressure, humidity) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            # Exécuter la requête
            cursor = self.dbConnection.cursor()
            cursor.execute(query, sensorData.toDbTuple())
            self.dbConnection.commit()
            cursor.close()
            
            return True
        except Exception as e:
            print(f"Erreur lors de l'insertion des données: {str(e)}")
            return False
        
    # Récupère les dernières données de capteurs
    def getLatestData(self, limit=1):
        """  
        Args:
            limit: Nombre de lignes à récupérer
            
        Returns:
            Une liste d'objets SensorData
        """
        try:
            query = """
            SELECT timestamp, air_quality, distance, luminosity, temperature, pressure, humidity
            FROM sensor_data
            ORDER BY timestamp DESC
            LIMIT %s
            """
            
            cursor = self.dbConnection.cursor()
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()
            cursor.close()
            
            # Convertir les résultats en objets SensorData
            result = []
            for row in rows:
                data = {
                    'timestamp': row[0],
                    'airQuality': row[1],
                    'distance': row[2],
                    'luminosity': row[3],
                    'temperature': row[4],
                    'pressure': row[5],
                    'humidity': row[6]
                }
                result.append(SensorData.fromDict(data))
            
            return result
        except Exception as e:
            print(f"Erreur lors de la récupération des données: {str(e)}")
            return []
    
    # Récupère les données de capteurs pour une période donnée
    def getDataByTimeframe(self, timeframe='day'):
        """
        Args:
            timeframe: Période ('hour', 'day', 'week', 'month')
            
        Returns:
            Une liste d'objets SensorData
        """
        try:
            # Déterminer la date de début en fonction de la période
            now = datetime.now()
            if timeframe == 'hour':
                startDate = now - timedelta(hours=1)
            elif timeframe == 'day':
                startDate = now - timedelta(days=1)
            elif timeframe == 'week':
                startDate = now - timedelta(weeks=1)
            elif timeframe == 'month':
                startDate = now - timedelta(days=30)
            else:
                startDate = now - timedelta(days=1)  # Par défaut: 1 jour
            
            # Formater la date pour la requête SQL
            startDateStr = startDate.strftime('%Y-%m-%d %H:%M:%S')
            
            query = """
            SELECT timestamp, air_quality, distance, luminosity, temperature, pressure, humidity
            FROM sensor_data
            WHERE timestamp >= %s
            ORDER BY timestamp DESC
            """
            
            cursor = self.dbConnection.cursor()
            cursor.execute(query, (startDateStr,))
            rows = cursor.fetchall()
            cursor.close()
            
            # Convertir les résultats en objets SensorData
            result = []
            for row in rows:
                data = {
                    'timestamp': row[0],
                    'airQuality': row[1],
                    'distance': row[2],
                    'luminosity': row[3],
                    'temperature': row[4],
                    'pressure': row[5],
                    'humidity': row[6]
                }
                result.append(SensorData.fromDict(data))
            
            return result
        except Exception as e:
            print(f"Erreur lors de la récupération des données: {str(e)}")
            return []
    
    # Récupère la liste des tables de la base de données
    def getTablesList(self):
        """
        Returns:
            Une liste des noms de tables
        """
        try:
            if self.dbConnection is None:
                print("Erreur: Connexion à la base de données non établie")
                return []
                
            query = "SHOW TABLES"
            
            cursor = self.dbConnection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            
            # Extraire les noms de tables
            tables = [row[0] for row in rows]
            
            return tables
        except Exception as e:
            print(f"Erreur lors de la récupération des tables: {str(e)}")
            return []
    
    # Récupère les données d'une table
    def getTableData(self, tableName, limit=100):
        """
        Args:
            tableName: Nom de la table
            limit: Nombre maximum de lignes à récupérer
            
        Returns:
            Un tuple (colonnes, lignes)
        """
        try:
            # Récupérer les informations sur les colonnes
            queryColumns = f"SHOW COLUMNS FROM {tableName}"
            
            cursor = self.dbConnection.cursor()
            cursor.execute(queryColumns)
            columnsInfo = cursor.fetchall()
            
            # Extraire les noms de colonnes
            columns = [col[0] for col in columnsInfo]
            
            # Récupérer les données
            queryData = f"SELECT * FROM {tableName} ORDER BY id DESC LIMIT {limit}"
            
            cursor.execute(queryData)
            rows = cursor.fetchall()
            cursor.close()
            
            return columns, rows
        except Exception as e:
            print(f"Erreur lors de la récupération des données de la table: {str(e)}")
            return [], []
    
    def executeCustomQuery(self, query, params=None):
        """
        Args:
            query: Requête SQL
            params: Paramètres de la requête
            
        Returns:
            Un tuple (colonnes, lignes)
        """
        try:
            cursor = self.dbConnection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Si c'est une requête SELECT, récupérer les résultats
            if query.strip().upper().startswith('SELECT'):
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
                cursor.close()
                return columns, rows
            else:
                # Pour les autres types de requêtes (INSERT, UPDATE, DELETE)
                self.dbConnection.commit()
                affectedRows = cursor.rowcount
                cursor.close()
                return [], [(f"{affectedRows} lignes affectées",)]
        except Exception as e:
            print(f"Erreur lors de l'exécution de la requête: {str(e)}")
            return [], [(f"Erreur: {str(e)}",)] 