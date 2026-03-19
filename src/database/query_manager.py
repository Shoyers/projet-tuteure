from datetime import datetime, timedelta
from src.models.sensor_data import SensorData

class QueryManager:
    def __init__(self, dbConnection):
        """Initialise le gestionnaire de requêtes."""
        self.dbConnection = dbConnection
        if dbConnection is not None and hasattr(dbConnection, 'connection'):
            self.connection = dbConnection.connection
        else:
            self.connection = dbConnection
    
    def insertSensorData(self, data):
        """Insère des données de capteurs dans la base de données."""
        from src.utils.sensor_parser import normalize_sensor_dict
        
        try:
            if not data or not isinstance(data, dict):
                print("Données invalides pour l'insertion")
                return False
            
            # Normaliser les données avec le parser centralisé
            normalized = normalize_sensor_dict(data)
            
            # Mapper vers les colonnes SQL (co2 au lieu de air_quality)
            sql_data = {}
            if normalized.get('air_quality') is not None:
                sql_data['co2'] = normalized['air_quality']
            if normalized.get('distance') is not None:
                sql_data['distance'] = normalized['distance']
            if normalized.get('luminosity') is not None:
                sql_data['luminosity'] = normalized['luminosity']
            if normalized.get('uv_index') is not None:
                sql_data['uv_index'] = normalized['uv_index']
            if normalized.get('ir_value') is not None:
                sql_data['ir_value'] = normalized['ir_value']
            if normalized.get('temperature') is not None:
                sql_data['temperature'] = normalized['temperature']
            if normalized.get('pressure') is not None:
                sql_data['pressure'] = normalized['pressure']
            if normalized.get('humidity') is not None:
                sql_data['humidity'] = normalized['humidity']
            if normalized.get('gas') is not None:
                sql_data['gas'] = normalized['gas']
            if normalized.get('latitude') is not None:
                sql_data['latitude'] = normalized['latitude']
            if normalized.get('longitude') is not None:
                sql_data['longitude'] = normalized['longitude']
            if normalized.get('altitude') is not None:
                sql_data['altitude'] = normalized['altitude']
            if normalized.get('timestamp') is not None:
                sql_data['timestamp'] = normalized['timestamp']
            if normalized.get('raw_data') is not None:
                sql_data['raw_data'] = normalized['raw_data']
            
            if not sql_data:
                print("Aucune donnée valide à insérer")
                return False
            
            # Construire la requête
            columns = list(sql_data.keys())
            placeholders = ["%s"] * len(columns)
            values = [sql_data[col] for col in columns]
            
            query = f"INSERT INTO sensor_data ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
            
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
            SELECT timestamp, co2, distance, luminosity, uv_index, ir_value, 
                   temperature, pressure, humidity, latitude, longitude, altitude
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
                    # Garder 'airQuality' pour compatibilité avec SensorData.fromDict
                    'airQuality': row[1],
                    'distance': row[2],
                    'luminosity': row[3],
                    'uvIndex': row[4],
                    'irValue': row[5],
                    'temperature': row[6],
                    'pressure': row[7],
                    'humidity': row[8],
                    'latitude': row[9],
                    'longitude': row[10],
                    'altitude': row[11]
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
            SELECT timestamp, co2, distance, luminosity, uv_index, ir_value, 
                   temperature, pressure, humidity, latitude, longitude, altitude
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
                    'humidity': row[8],
                    'latitude': row[9],
                    'longitude': row[10],
                    'altitude': row[11]
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
            if self.connection is None:
                print("Erreur lors de la récupération des données de la table: MySQL Connection not available.")
                return [], []
                
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
                SELECT id, co2, distance, luminosity, uv_index, ir_value, 
                       temperature, pressure, humidity, latitude, longitude, altitude, timestamp
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
                    # On expose toujours 'air_quality' côté Python,
                    # même si la colonne SQL s'appelle co2.
                    'air_quality': row[1],
                    'distance': row[2],
                    'luminosity': row[3],
                    'uv_index': row[4],
                    'ir_value': row[5],
                    'temperature': row[6],
                    'pressure': row[7],
                    'humidity': row[8],
                    'latitude': row[9],
                    'longitude': row[10],
                    'altitude': row[11],
                    'timestamp': row[12]
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
                    AVG(co2) as avg_co2,
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
    
    # Méthodes pour les insights ML (reason et confidence)
    def getMLInsights(self, limit=100):
        """
        Récupère les données ML avec reason et confidence
        
        Args:
            limit: Nombre maximum d'enregistrements à récupérer
            
        Returns:
            Liste de dictionnaires contenant les données ML
        """
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT 
                    id,
                    timestamp,
                    temperature,
                    gas,
                    reason,
                    confidence
                FROM sensor_data
                WHERE reason IS NOT NULL OR confidence IS NOT NULL
                ORDER BY timestamp DESC
                LIMIT %s
            """
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()
            
            results = []
            for row in rows:
                results.append({
                    'id': row[0],
                    'timestamp': row[1],
                    'temperature': row[2],
                    'gas': row[3],
                    'reason': row[4],
                    'confidence': row[5]
                })
            
            return results
            
        except Exception as e:
            print(f"Erreur lors de la récupération des insights ML: {str(e)}")
            return []
    
    def getMLInsightsByConfidence(self, min_confidence=0, max_confidence=100, limit=100):
        """
        Récupère les données ML filtrées par niveau de confiance
        
        Args:
            min_confidence: Confiance minimale (0-100)
            max_confidence: Confiance maximale (0-100)
            limit: Nombre maximum d'enregistrements
            
        Returns:
            Liste de dictionnaires contenant les données ML filtrées
        """
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT 
                    id,
                    timestamp,
                    temperature,
                    gas,
                    reason,
                    confidence
                FROM sensor_data_ml
                WHERE confidence >= %s AND confidence <= %s
                ORDER BY confidence DESC, timestamp DESC
                LIMIT %s
            """
            cursor.execute(query, (min_confidence, max_confidence, limit))
            rows = cursor.fetchall()
            
            results = []
            for row in rows:
                results.append({
                    'id': row[0],
                    'timestamp': row[1],
                    'temperature': row[2],
                    'gas': row[3],
                    'reason': row[4],
                    'confidence': row[5]
                })
            
            return results
            
        except Exception as e:
            print(f"Erreur lors du filtrage par confiance: {str(e)}")
            return []
    
    def searchMLInsightsByReason(self, keyword, limit=100):
        """
        Recherche les données ML par mot-clé dans la raison
        
        Args:
            keyword: Mot-clé à rechercher dans la colonne reason
            limit: Nombre maximum d'enregistrements
            
        Returns:
            Liste de dictionnaires contenant les résultats de recherche
        """
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT 
                    id,
                    timestamp,
                    temperature,
                    gas,
                    reason,
                    confidence
                FROM sensor_data_ml
                WHERE reason LIKE %s
                ORDER BY confidence DESC, timestamp DESC
                LIMIT %s
            """
            search_pattern = f"%{keyword}%"
            cursor.execute(query, (search_pattern, limit))
            rows = cursor.fetchall()
            
            results = []
            for row in rows:
                results.append({
                    'id': row[0],
                    'timestamp': row[1],
                    'temperature': row[2],
                    'gas': row[3],
                    'reason': row[4],
                    'confidence': row[5]
                })
            
            return results
            
        except Exception as e:
            print(f"Erreur lors de la recherche par raison: {str(e)}")
            return []
    
    def getMLStats(self):
        """
        Récupère les statistiques sur les données ML
        
        Returns:
            Dictionnaire avec les statistiques
        """
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT 
                    COUNT(*) as total,
                    COUNT(CASE WHEN confidence >= 80 THEN 1 END) as high_confidence,
                    COUNT(CASE WHEN confidence >= 50 AND confidence < 80 THEN 1 END) as medium_confidence,
                    COUNT(CASE WHEN confidence < 50 THEN 1 END) as low_confidence,
                    AVG(confidence) as avg_confidence,
                    MAX(confidence) as max_confidence,
                    MIN(confidence) as min_confidence
                FROM sensor_data_ml
                WHERE confidence IS NOT NULL
            """
            cursor.execute(query)
            row = cursor.fetchone()
            
            return {
                'total': row[0] or 0,
                'high_confidence': row[1] or 0,
                'medium_confidence': row[2] or 0,
                'low_confidence': row[3] or 0,
                'avg_confidence': row[4] or 0,
                'max_confidence': row[5] or 0,
                'min_confidence': row[6] or 0
            }
            
        except Exception as e:
            print(f"Erreur lors du calcul des statistiques ML: {str(e)}")
            return {
                'total': 0,
                'high_confidence': 0,
                'medium_confidence': 0,
                'low_confidence': 0,
                'avg_confidence': 0,
                'max_confidence': 0,
                'min_confidence': 0
            } 