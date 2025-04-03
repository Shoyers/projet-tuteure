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
        # Si dbConnection est une instance de DatabaseConnection, on utilise sa propriété connection
        if dbConnection is not None and hasattr(dbConnection, 'connection'):
            self.connection = dbConnection.connection
        else:
            self.connection = dbConnection
    
    # Insère les données des capteurs dans la base de données
    def insertSensorData(self, data):
        """
        Insère des données de capteurs dans la base de données.
        
        Args:
            data: Un dictionnaire contenant les données à insérer.
                 Les clés devraient correspondre aux noms des colonnes de la table sensor_data.
        
        Returns:
            True si l'insertion a réussi, False sinon.
        """
        try:
            # Vérifier qu'un dictionnaire valide est fourni
            if not data or not isinstance(data, dict):
                print("Données invalides pour l'insertion")
                return False
            
            # Normaliser les clés et traiter les valeurs spéciales
            normalized_data = {}
            
            # Mapper les différents formats de clés possibles
            key_mapping = {
                'air_quality': ['air_quality', 'airQuality', 'AQ'],
                'distance': ['distance', 'dist', 'DIST'],
                'luminosity': ['luminosity', 'lum', 'LUM'],
                'uv_index': ['uv_index', 'uvIndex', 'UV'],
                'ir_value': ['ir_value', 'irValue', 'IR'],
                'temperature': ['temperature', 'temp', 'TEMP'],
                'pressure': ['pressure', 'press', 'PRESS'],
                'humidity': ['humidity', 'hum', 'HUM'],
                'timestamp': ['timestamp', 'time', 'date'],
                'raw_data': ['raw_data', 'rawData']
            }
            
            # Normaliser les données
            for db_key, possible_keys in key_mapping.items():
                for key in possible_keys:
                    if key in data and data[key] is not None:
                        # Convertir 'N/A' en None
                        if data[key] == 'N/A':
                            normalized_data[db_key] = None
                        else:
                            normalized_data[db_key] = data[key]
                        break
            
            # Construire la requête d'insertion
            columns = []
            placeholders = []
            values = []
            
            # Ajouter chaque clé et valeur s'ils sont présents et pas None
            for key, value in normalized_data.items():
                if value is not None:
                    columns.append(key)
                    placeholders.append("%s")
                    values.append(value)
            
            # S'il n'y a pas de colonnes, ne pas créer d'insertion
            if not columns:
                print("Aucune donnée valide à insérer")
                return False
            
            # Construire la requête
            query = f"INSERT INTO sensor_data ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
            
            # Exécuter la requête
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            
            print(f"Données capteurs insérées avec succès, colonnes: {columns}")
            return True
            
        except Exception as e:
            print(f"Erreur lors de l'insertion des données capteurs: {str(e)}")
            import traceback
            traceback.print_exc()
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
            SELECT timestamp, air_quality, distance, luminosity, uv_index, ir_value, temperature, pressure, humidity
            FROM sensor_data
            ORDER BY timestamp DESC
            LIMIT %s
            """
            
            cursor = self.connection.cursor()
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
                    'uvIndex': row[4],
                    'irValue': row[5],
                    'temperature': row[6],
                    'pressure': row[7],
                    'humidity': row[8]
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
            SELECT timestamp, air_quality, distance, luminosity, uv_index, ir_value, temperature, pressure, humidity
            FROM sensor_data
            WHERE timestamp >= %s
            ORDER BY timestamp DESC
            """
            
            cursor = self.connection.cursor()
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
                    'uvIndex': row[4],
                    'irValue': row[5],
                    'temperature': row[6],
                    'pressure': row[7],
                    'humidity': row[8]
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
            if self.connection is None:
                print("Erreur: Connexion à la base de données non établie")
                return []
                
            query = "SHOW TABLES"
            
            cursor = self.connection.cursor()
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
            
            cursor = self.connection.cursor()
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
            cursor = self.connection.cursor()
            
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
                self.connection.commit()
                affectedRows = cursor.rowcount
                cursor.close()
                return [], [(f"{affectedRows} lignes affectées",)]
        except Exception as e:
            print(f"Erreur lors de l'exécution de la requête: {str(e)}")
            return [], [(f"Erreur: {str(e)}",)]

    # Méthode pour convertir une instance SensorData en format pour BDD
    def _sensorDataToDbFormat(self, sensorData):
        """
        Convertit une instance SensorData en format pour insertion dans la base de données.
        
        Args:
            sensorData: L'instance SensorData à convertir
            
        Returns:
            Un tuple contenant les valeurs à insérer dans la base de données
        """
        return (
            sensorData.air_quality if sensorData.air_quality and sensorData.air_quality > 0 else None,
            sensorData.distance if sensorData.distance and sensorData.distance > 0 else None,
            sensorData.luminosity if sensorData.luminosity and sensorData.luminosity > 0 else None,
            sensorData.uvIndex if sensorData.uvIndex and sensorData.uvIndex > 0 else None,
            sensorData.irValue if sensorData.irValue and sensorData.irValue > 0 else None,
            sensorData.temperature if sensorData.temperature else None,
            sensorData.pressure if sensorData.pressure and sensorData.pressure > 0 else None,
            sensorData.humidity if sensorData.humidity and sensorData.humidity > 0 else None,
            sensorData.timestamp,
            sensorData.rawData
        )

    # Méthode pour récupérer les n dernières mesures
    def getLastMeasurements(self, limit=10):
        """
        Récupère les dernières mesures des capteurs.
        
        Args:
            limit: Le nombre maximum de mesures à récupérer (par défaut 10)
            
        Returns:
            Une liste de dictionnaires contenant les mesures, ou None en cas d'erreur
        """
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT id, air_quality, distance, luminosity, uv_index, ir_value, 
                       temperature, pressure, humidity, timestamp
                FROM sensor_data
                ORDER BY timestamp DESC
                LIMIT %s
            """
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()
            
            if not rows:
                return []
                
            results = []
            for row in rows:
                results.append({
                    'id': row[0],
                    'air_quality': row[1],
                    'distance': row[2],
                    'luminosity': row[3],
                    'uv_index': row[4],
                    'ir_value': row[5],
                    'temperature': row[6],
                    'pressure': row[7],
                    'humidity': row[8],
                    'timestamp': row[9]
                })
            
            return results
            
        except Exception as e:
            print(f"Erreur lors de la récupération des dernières mesures: {str(e)}")
            return None
    
    # Méthode pour calculer la moyenne des valeurs sur une période
    def getAverages(self, hours=1):
        """
        Calcule la moyenne des valeurs des capteurs sur la période spécifiée.
        
        Args:
            hours: Le nombre d'heures à considérer pour la moyenne (par défaut 1)
            
        Returns:
            Un dictionnaire contenant les moyennes calculées, ou None en cas d'erreur
        """
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT 
                    AVG(air_quality) as avg_air_quality,
                    AVG(distance) as avg_distance,
                    AVG(luminosity) as avg_luminosity,
                    AVG(uv_index) as avg_uv,
                    AVG(ir_value) as avg_ir,
                    AVG(temperature) as avg_temperature,
                    AVG(pressure) as avg_pressure,
                    AVG(humidity) as avg_humidity,
                    COUNT(*) as count
                FROM sensor_data
                WHERE timestamp > DATE_SUB(NOW(), INTERVAL %s HOUR)
            """
            cursor.execute(query, (hours,))
            row = cursor.fetchone()
            
            if not row or row[9] == 0:  # Vérifier si count est 0
                return None
                
            return {
                'air_quality': row[0],
                'distance': row[1],
                'luminosity': row[2],
                'uv_index': row[3],
                'ir_value': row[4],
                'temperature': row[5],
                'pressure': row[6],
                'humidity': row[7],
                'count': row[9]
            }
            
        except Exception as e:
            print(f"Erreur lors du calcul des moyennes: {str(e)}")
            return None 