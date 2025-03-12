import threading
import time

# Contrôleur pour la gestion des tables de la base de données
class TableController:
    # Initialise le contrôleur des tables
    def __init__(self, view, queryManager):
        """
        Args:
            view: La vue des tables
            query_manager: Le gestionnaire de requêtes SQL
        """
        self.view = view
        self.queryManager = queryManager
        
        # Variables pour le rafraîchissement automatique
        self.refreshActive = False
        self.refreshInterval = 5000  # 5 secondes par défaut
        self.refreshJob = None
        self.stopRefresh = threading.Event()
    
    # Rafraîchit la liste des tables
    def refreshTablesList(self):
        tables = self.queryManager.getTablesList()
        self.view.updateTablesList(tables)

    # Charge les données d'une table
    def loadTableData(self, tableName):
        """   
        Args:
            tableName: Nom de la table à charger
        """
        columns, rows = self.query_manager.get_table_data(tableName)
        self.view.updateTableData(tableName, columns, rows)
    
    # Démarre le rafraîchissement automatique
    def startAutoRefresh(self, interval=5000):
        """   
        Args:
            interval: Intervalle de rafraîchissement en millisecondes
        """
        if self.refreshActive:
            return
        
        self.refreshActive = True
        self.refreshInterval = interval
        self.stopRefresh.clear()
        
        # Mettre à jour l'affichage du statut
        self.view.updateAutoRefreshStatus(True, interval / 1000)
        
        # Démarrer le thread de rafraîchissement
        self.refreshThread = threading.Thread(target=self._refreshLoop)
        self.refreshThread.daemon = True
        self.refreshThread.start()
    
    # Arrête le rafraîchissement automatique
    def stopAutoRefresh(self):
        if not self.refreshActive:
            return
        
        self.refreshActive = False
        self.stopRefresh.set()
        
        # Mettre à jour l'affichage du statut
        self.view.updateAutoRefreshStatus(False)
    
    # Boucle de rafraîchissement automatique des données
    def _refreshLoop(self):
        while not self.stopRefresh.is_set() and self.refreshActive:
            # Vérifier si une table est sélectionnée
            if self.view.currentTableName:
                # Charger les données de la table
                self.loadTableData(self.view.currentTableName)
            
            # Attendre l'intervalle de rafraîchissement
            time.sleep(self.refreshInterval / 1000)
    
    # Exécute une requête SQL personnalisée
    def executeCustomQuery(self, query, params=None):
        """
        Args:
            query: Requête SQL
            params: Paramètres de la requête
        Returns:
            Un tuple (colonnes, lignes)
        """
        return self.queryManager.executeCustomQuery(query, params)