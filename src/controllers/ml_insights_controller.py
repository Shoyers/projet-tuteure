class MLInsightsController:
    """Contrôleur pour gérer les insights du Machine Learning"""
    
    def __init__(self, view, queryManager):
        """
        Initialise le contrôleur
        
        Args:
            view: Vue MLInsightsView
            queryManager: Gestionnaire de requêtes
        """
        self.view = view
        self.queryManager = queryManager
    
    def loadMLData(self, limit=100):
        """
        Charge les données ML depuis la base de données
        
        Args:
            limit: Nombre maximum d'enregistrements à charger
        """
        try:
            # Afficher le loading
            self.view.showLoading()
            
            # Récupérer les données ML
            data = self.queryManager.getMLInsights(limit=limit)
            
            if not data:
                self.view.displayData([])
                self.view.updateStats(0, 0, 0, 0)
                return
            
            # Calculer les statistiques
            total = len(data)
            high = sum(1 for row in data if (row.get('confidence') or 0) >= 80)
            medium = sum(1 for row in data if 50 <= (row.get('confidence') or 0) < 80)
            low = sum(1 for row in data if (row.get('confidence') or 0) < 50)
            
            # Mettre à jour la vue
            self.view.updateStats(total, high, medium, low)
            self.view.displayData(data)
            
            print(f"✓ {total} enregistrements ML chargés")
            
        except Exception as e:
            error_message = str(e)
            print(f"❌ Erreur lors du chargement des données ML: {error_message}")
            self.view.hideLoading()
            self.view.showError(error_message)
    
    def filterByConfidence(self, min_confidence=0, max_confidence=100):
        """
        Filtre les données par niveau de confiance
        
        Args:
            min_confidence: Confiance minimale (0-100)
            max_confidence: Confiance maximale (0-100)
        """
        try:
            data = self.queryManager.getMLInsightsByConfidence(
                min_confidence=min_confidence,
                max_confidence=max_confidence,
                limit=100
            )
            
            if not data:
                self.view.displayData([])
                return
            
            # Calculer les statistiques pour les données filtrées
            total = len(data)
            high = sum(1 for row in data if (row.get('confidence') or 0) >= 80)
            medium = sum(1 for row in data if 50 <= (row.get('confidence') or 0) < 80)
            low = sum(1 for row in data if (row.get('confidence') or 0) < 50)
            
            self.view.updateStats(total, high, medium, low)
            self.view.displayData(data)
            
            print(f"✓ Filtré: {total} enregistrements (confiance {min_confidence}-{max_confidence}%)")
            
        except Exception as e:
            error_message = str(e)
            print(f"❌ Erreur lors du filtrage: {error_message}")
            self.view.showError(error_message)
    
    def searchByReason(self, keyword):
        """
        Recherche les données par mot-clé dans la raison
        
        Args:
            keyword: Mot-clé à rechercher
        """
        try:
            data = self.queryManager.searchMLInsightsByReason(
                keyword=keyword,
                limit=100
            )
            
            if not data:
                self.view.displayData([])
                return
            
            # Calculer les statistiques
            total = len(data)
            high = sum(1 for row in data if (row.get('confidence') or 0) >= 80)
            medium = sum(1 for row in data if 50 <= (row.get('confidence') or 0) < 80)
            low = sum(1 for row in data if (row.get('confidence') or 0) < 50)
            
            self.view.updateStats(total, high, medium, low)
            self.view.displayData(data)
            
            print(f"✓ Recherche '{keyword}': {total} résultats")
            
        except Exception as e:
            error_message = str(e)
            print(f"❌ Erreur lors de la recherche: {error_message}")
            self.view.showError(error_message)
