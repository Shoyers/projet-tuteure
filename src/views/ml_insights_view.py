import customtkinter as ctk
from config.settings import COLOR_PALETTE

class MLInsightsView:
    """Vue pour afficher les insights du Machine Learning (reason et confidence)"""
    
    def __init__(self, parent, museoFonts, onRefresh=None):
        """
        Initialise la vue des insights ML
        
        Args:
            parent: Widget parent
            museoFonts: Dictionnaire des polices Museo
            onRefresh: Callback pour rafraîchir les données
        """
        self.parent = parent
        self.museoFonts = museoFonts
        self.onRefresh = onRefresh
        
        # Créer l'interface
        self.createUi()
    
    def createUi(self):
        """Crée l'interface utilisateur"""
        # Frame principal
        self.mainFrame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.mainFrame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.mainFrame.grid_columnconfigure(0, weight=1)
        
        # En-tête
        self.createHeader()
        
        # Statistiques
        self.createStatsSection()
        
        # Tableau des données ML
        self.createTableSection()
    
    def createHeader(self):
        """Crée l'en-tête de la page"""
        headerFrame = ctk.CTkFrame(self.mainFrame, fg_color="transparent")
        headerFrame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        headerFrame.grid_columnconfigure(0, weight=1)
        
        # Titre
        titleLabel = ctk.CTkLabel(
            headerFrame,
            text="Analyse IA - Détection des Problèmes",
            font=ctk.CTkFont(
                family=self.museoFonts.get('bold', None),
                size=28,
                weight="bold"
            ),
            text_color=COLOR_PALETTE['primary']
        )
        titleLabel.grid(row=0, column=0, sticky="w")
        
        # Description
        descLabel = ctk.CTkLabel(
            headerFrame,
            text="Visualisation des analyses par intelligence artificielle pour détecter les anomalies des capteurs",
            font=ctk.CTkFont(
                family=self.museoFonts.get('regular', None),
                size=14
            ),
            text_color=COLOR_PALETTE['text_dark']
        )
        descLabel.grid(row=1, column=0, sticky="w", pady=(5, 0))
        
        # Bouton de rafraîchissement
        refreshBtn = ctk.CTkButton(
            headerFrame,
            text="Rafraîchir",
            command=self.onRefresh if self.onRefresh else lambda: None,
            font=ctk.CTkFont(
                family=self.museoFonts.get('regular', None),
                size=14
            ),
            fg_color=COLOR_PALETTE['primary'],
            hover_color=COLOR_PALETTE['accent'],
            corner_radius=8,
            width=120,
            height=40
        )
        refreshBtn.grid(row=0, column=1, rowspan=2, padx=10)
    
    def createStatsSection(self):
        """Crée la section des statistiques"""
        statsFrame = ctk.CTkFrame(self.mainFrame, fg_color="transparent")
        statsFrame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        statsFrame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Variables pour les statistiques
        self.totalRecordsVar = ctk.StringVar(value="0")
        self.highConfidenceVar = ctk.StringVar(value="0")
        self.mediumConfidenceVar = ctk.StringVar(value="0")
        self.lowConfidenceVar = ctk.StringVar(value="0")
        
        # Carte Total
        self.createStatCard(
            statsFrame, 
            "Total d'enregistrements", 
            self.totalRecordsVar, 
            COLOR_PALETTE['primary'],
            0
        )
        
        # Carte Haute confiance
        self.createStatCard(
            statsFrame, 
            "Haute confiance (≥80%)", 
            self.highConfidenceVar, 
            "#10b981",  # Vert
            1
        )
        
        # Carte Moyenne confiance
        self.createStatCard(
            statsFrame, 
            "Moyenne confiance (50-80%)", 
            self.mediumConfidenceVar, 
            "#f59e0b",  # Orange
            2
        )
        
        # Carte Basse confiance
        self.createStatCard(
            statsFrame, 
            "Basse confiance (<50%)", 
            self.lowConfidenceVar, 
            "#ef4444",  # Rouge
            3
        )
    
    def createStatCard(self, parent, title, variable, color, column):
        """Crée une carte de statistique"""
        card = ctk.CTkFrame(
            parent,
            fg_color=color,
            corner_radius=12
        )
        card.grid(row=0, column=column, sticky="ew", padx=10)
        
        # Titre
        titleLabel = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(
                family=self.museoFonts.get('regular', None),
                size=12
            ),
            text_color="white"
        )
        titleLabel.pack(pady=(15, 5), padx=15)
        
        # Valeur
        valueLabel = ctk.CTkLabel(
            card,
            textvariable=variable,
            font=ctk.CTkFont(
                family=self.museoFonts.get('bold', None),
                size=32,
                weight="bold"
            ),
            text_color="white"
        )
        valueLabel.pack(pady=(0, 15), padx=15)
    
    def createTableSection(self):
        """Crée la section d'affichage des données ML avec des cards"""
        cardsContainer = ctk.CTkFrame(
            self.mainFrame,
            fg_color="transparent"
        )
        cardsContainer.grid(row=2, column=0, sticky="nsew", pady=(0, 20))
        cardsContainer.grid_columnconfigure(0, weight=1)
        cardsContainer.grid_rowconfigure(0, weight=1)
        self.mainFrame.grid_rowconfigure(2, weight=1)
        
        # Zone de scroll pour les cards (scrollbar très discret)
        self.scrollFrame = ctk.CTkScrollableFrame(
            cardsContainer,
            fg_color="transparent",
            scrollbar_button_color=COLOR_PALETTE['bg_light'],  # Couleur discrète
            scrollbar_button_hover_color=COLOR_PALETTE['border'],  # Couleur hover discrète
            scrollbar_fg_color=COLOR_PALETTE['bg_light']  # Track discret
        )
        self.scrollFrame.grid(row=0, column=0, sticky="nsew")
        self.scrollFrame.grid_columnconfigure(0, weight=1)
        
        # Indicateur de chargement
        self.loadingLabel = ctk.CTkLabel(
            self.scrollFrame,
            text="⏳ Chargement en cours...",
            font=ctk.CTkFont(
                family=self.museoFonts.get('regular', None),
                size=16
            ),
            text_color=COLOR_PALETTE['primary']
        )
        
        # Message par défaut
        self.noDataLabel = ctk.CTkLabel(
            self.scrollFrame,
            text="Aucune donnée disponible. Cliquez sur 'Rafraîchir' pour charger les données.",
            font=ctk.CTkFont(
                family=self.museoFonts.get('regular', None),
                size=14
            ),
            text_color=COLOR_PALETTE['text_dark']
        )
        self.noDataLabel.grid(row=0, column=0, pady=50)
    
    def updateStats(self, total, high, medium, low):
        """Met à jour les statistiques"""
        self.totalRecordsVar.set(str(total))
        self.highConfidenceVar.set(str(high))
        self.mediumConfidenceVar.set(str(medium))
        self.lowConfidenceVar.set(str(low))
    
    def showLoading(self):
        """Affiche l'indicateur de chargement"""
        # Masquer les autres éléments
        self.noDataLabel.grid_forget()
        
        # Effacer les anciennes cards
        for widget in self.scrollFrame.winfo_children():
            if widget != self.loadingLabel and widget != self.noDataLabel:
                widget.destroy()
        
        # Afficher le loading
        self.loadingLabel.grid(row=0, column=0, pady=50)
    
    def hideLoading(self):
        """Masque l'indicateur de chargement"""
        self.loadingLabel.grid_forget()
    
    def displayData(self, data):
        """Affiche les données ML dans des cards larges"""
        # Masquer le loading
        self.hideLoading()
        
        # Effacer les anciennes données
        for widget in self.scrollFrame.winfo_children():
            if widget != self.loadingLabel and widget != self.noDataLabel:
                widget.destroy()
        
        if not data:
            self.noDataLabel = ctk.CTkLabel(
                self.scrollFrame,
                text="Aucune donnée ML trouvée dans la base de données.",
                font=ctk.CTkFont(
                    family=self.museoFonts.get('regular', None),
                    size=14
                ),
                text_color=COLOR_PALETTE['text_dark']
            )
            self.noDataLabel.grid(row=0, column=0, pady=50)
            return
        
        # Afficher chaque enregistrement dans une card
        for idx, row in enumerate(data):
            # Déterminer la couleur en fonction de la confiance
            confidence = row.get('confidence', 0) or 0
            if confidence >= 80:
                confidence_color = "#10b981"  # Vert
                border_color = "#10b981"
            elif confidence >= 50:
                confidence_color = "#f59e0b"  # Orange
                border_color = "#f59e0b"
            else:
                confidence_color = "#ef4444"  # Rouge
                border_color = "#ef4444"
            
            # Card pour chaque enregistrement
            card = ctk.CTkFrame(
                self.scrollFrame,
                fg_color=COLOR_PALETTE['bg_white'],
                corner_radius=12,
                border_width=2,
                border_color=border_color
            )
            card.grid(row=idx, column=0, sticky="ew", pady=10, padx=20)
            card.grid_columnconfigure(1, weight=1)
            
            # Ligne 1: ID et Confiance (en haut à gauche et droite)
            idFrame = ctk.CTkFrame(card, fg_color="transparent")
            idFrame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(15, 5))
            idFrame.grid_columnconfigure(1, weight=1)
            
            # ID
            idLabel = ctk.CTkLabel(
                idFrame,
                text=f"ID: {row.get('id', 'N/A')}",
                font=ctk.CTkFont(
                    family=self.museoFonts.get('bold', None),
                    size=13,
                    weight="bold"
                ),
                text_color=COLOR_PALETTE['text_muted']
            )
            idLabel.grid(row=0, column=0, sticky="w")
            
            # Confiance (badge)
            confidence_text = f"{confidence:.1f}%" if confidence else 'N/A'
            confidenceBadge = ctk.CTkFrame(
                idFrame,
                fg_color=confidence_color,
                corner_radius=20
            )
            confidenceBadge.grid(row=0, column=2, sticky="e")
            
            confidenceLabel = ctk.CTkLabel(
                confidenceBadge,
                text=confidence_text,
                font=ctk.CTkFont(
                    family=self.museoFonts.get('bold', None),
                    size=14,
                    weight="bold"
                ),
                text_color="white"
            )
            confidenceLabel.pack(padx=15, pady=5)
            
            # Ligne 2: Timestamp
            timestamp = row.get('timestamp', 'N/A')
            if timestamp and timestamp != 'N/A':
                timestamp = str(timestamp)[:19]
            timestampLabel = ctk.CTkLabel(
                card,
                text=f"📅 {timestamp}",
                font=ctk.CTkFont(
                    family=self.museoFonts.get('regular', None),
                    size=12
                ),
                text_color=COLOR_PALETTE['text_muted']
            )
            timestampLabel.grid(row=1, column=0, columnspan=2, sticky="w", padx=20, pady=(0, 10))
            
            # Ligne 3: Données capteurs (Température et Gas)
            dataFrame = ctk.CTkFrame(card, fg_color=COLOR_PALETTE['bg_light'], corner_radius=8)
            dataFrame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 10))
            dataFrame.grid_columnconfigure((0, 1), weight=1)
            
            # Température
            temp = row.get('temperature', 'N/A')
            temp_text = f"{temp}°C" if temp and temp != 'N/A' else 'N/A'
            tempLabel = ctk.CTkLabel(
                dataFrame,
                text=f"🌡️ Température: {temp_text}",
                font=ctk.CTkFont(
                    family=self.museoFonts.get('regular', None),
                    size=13
                ),
                text_color=COLOR_PALETTE['text_dark']
            )
            tempLabel.grid(row=0, column=0, sticky="w", padx=15, pady=10)
            
            # Gas/AQI
            gas = row.get('gas', 'N/A')
            gas_text = f"{gas:.1f}" if gas and gas != 'N/A' else 'N/A'
            gasLabel = ctk.CTkLabel(
                dataFrame,
                text=f"💨 Gas/AQI: {gas_text}",
                font=ctk.CTkFont(
                    family=self.museoFonts.get('regular', None),
                    size=13
                ),
                text_color=COLOR_PALETTE['text_dark']
            )
            gasLabel.grid(row=0, column=1, sticky="w", padx=15, pady=10)
            
            # Ligne 4: Raison (texte principal)
            reason = row.get('reason', 'N/A') or 'N/A'
            
            reasonFrame = ctk.CTkFrame(card, fg_color="transparent")
            reasonFrame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 15))
            
            reasonTitleLabel = ctk.CTkLabel(
                reasonFrame,
                text="⚠️ Raison détectée:",
                font=ctk.CTkFont(
                    family=self.museoFonts.get('bold', None),
                    size=12,
                    weight="bold"
                ),
                text_color=COLOR_PALETTE['text_dark'],
                anchor="w"
            )
            reasonTitleLabel.grid(row=0, column=0, sticky="w", pady=(0, 5))
            
            reasonLabel = ctk.CTkLabel(
                reasonFrame,
                text=reason,
                font=ctk.CTkFont(
                    family=self.museoFonts.get('regular', None),
                    size=13
                ),
                text_color=COLOR_PALETTE['text_dark'],
                anchor="w",
                justify="left",
                wraplength=900
            )
            reasonLabel.grid(row=1, column=0, sticky="w")
    
    def showError(self, message):
        """Affiche un message d'erreur"""
        for widget in self.scrollFrame.winfo_children():
            widget.destroy()
        
        errorLabel = ctk.CTkLabel(
            self.scrollFrame,
            text=f"Erreur : {message}",
            font=ctk.CTkFont(
                family=self.museoFonts.get('regular', None),
                size=14
            ),
            text_color="#ef4444"
        )
        errorLabel.grid(row=0, column=0, columnspan=6, pady=50)
