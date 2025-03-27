import customtkinter as ctk
from config.settings import COLOR_PALETTE

# Vue pour les paramètres de l'application.
class SettingsView:
    # Initialise la vue des paramètres.
    def __init__(self, parent, museoFonts, onConnectPort, onRefreshPorts, onConnectDb, onDisconnectDb):
        """
        Args:
            parent: Le widget parent
            museo_fonts: Dictionnaire des polices Museo
            on_connect_port: Fonction à appeler pour se connecter à un port série
            on_refresh_ports: Fonction à appeler pour rafraîchir la liste des ports
            on_connect_db: Fonction à appeler pour se connecter à la base de données
            on_disconnect_db: Fonction à appeler pour se déconnecter de la base de données
        """
        self.parent = parent
        self.museoFonts = museoFonts
        self.onConnectPort = onConnectPort
        self.onRefreshPorts = onRefreshPorts
        self.onConnectDb = onConnectDb
        self.onDisconnectDb = onDisconnectDb
        
        # Variables pour les paramètres
        self.selectedPort = ctk.StringVar(value="")
        self.connectionStatus = ctk.StringVar(value="Non connecté")
        self.dbHost = ctk.StringVar(value="localhost")
        self.dbUser = ctk.StringVar(value="root")
        self.dbPassword = ctk.StringVar(value="root")
        self.dbName = ctk.StringVar(value="serv-projet")
        self.dbStatus = ctk.StringVar(value="Non connecté")
        
        # Créer le contenu de la vue
        self.createSettingsContent()
    
    # Crée le contenu de la vue des paramètres.
    def createSettingsContent(self):
        # Section principale
        mainSection = ctk.CTkFrame(self.parent, fg_color="transparent")
        mainSection.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        mainSection.columnconfigure(0, weight=1)
        mainSection.rowconfigure(0, weight=0)
        mainSection.rowconfigure(1, weight=0)
        mainSection.rowconfigure(2, weight=1)
        
        # Section connexion série
        self.createSerialSection(mainSection)
        
        # Section connexion base de données
        self.createDatabaseSection(mainSection)

    
    # Crée la section de connexion série.
    def createSerialSection(self, parent):
        """
        Args:
            parent: Le widget parent
        """
        # Cadre pour la connexion série
        serialFrame = ctk.CTkFrame(parent, fg_color=COLOR_PALETTE['bg_card'], corner_radius=8, border_width=1, border_color=COLOR_PALETTE['border'])
        serialFrame.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 20))
        serialFrame.columnconfigure(0, weight=1)
        
        # Titre de la section
        serialTitle = ctk.CTkLabel(serialFrame, text="Connexion série", 
                                  font=ctk.CTkFont(family=self.museoFonts.get('bold', None), size=16),
                                  text_color=COLOR_PALETTE['text_dark'])
        serialTitle.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))
        
        # Cadre pour les contrôles
        serialControls = ctk.CTkFrame(serialFrame, fg_color="transparent")
        serialControls.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        serialControls.columnconfigure(0, weight=0)
        serialControls.columnconfigure(1, weight=1)
        serialControls.columnconfigure(2, weight=0)
        serialControls.columnconfigure(3, weight=0)
        
        # Étiquette pour le port
        portLabel = ctk.CTkLabel(serialControls, text="Port série:", 
                                font=ctk.CTkFont(family=self.museoFonts.get('regular', None), size=14),
                                text_color=COLOR_PALETTE['text_dark'])
        portLabel.grid(row=0, column=0, sticky="w", padx=(0, 10), pady=0)
        
        # Combobox pour les ports
        self.portCombobox = ctk.CTkComboBox(serialControls, 
                                          variable=self.selectedPort,
                                          values=["COM1", "COM2", "COM3"],
                                          font=ctk.CTkFont(family=self.museoFonts.get('regular', None), size=14),
                                          dropdown_font=ctk.CTkFont(family=self.museoFonts.get('regular', None), size=14),
                                          button_color=COLOR_PALETTE['primary'],
                                          button_hover_color=COLOR_PALETTE['accent'],
                                          border_color=COLOR_PALETTE['border'],
                                          width=200)
        self.portCombobox.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady=0)
        
        # Bouton de rafraîchissement des ports
        refreshPortsButton = ctk.CTkButton(serialControls, text="↻", 
                                          command=self.onRefreshPorts,
                                          font=ctk.CTkFont(family=self.museoFonts.get('bold', None), size=14),
                                          fg_color=COLOR_PALETTE['bg_light'],
                                          text_color=COLOR_PALETTE['primary'],
                                          hover_color=COLOR_PALETTE['border'],
                                          corner_radius=4,
                                          width=40,
                                          height=30)
        refreshPortsButton.grid(row=0, column=2, sticky="w", padx=(0, 10), pady=0)
        
        # Bouton de connexion
        self.connectButton = ctk.CTkButton(serialControls, text="Connecter", 
                                         command=self.onConnectPort,
                                         font=ctk.CTkFont(family=self.museoFonts.get('bold', None), size=14),
                                         fg_color=COLOR_PALETTE['primary'],
                                         text_color=COLOR_PALETTE['text_light'],
                                         hover_color=COLOR_PALETTE['accent'],
                                         corner_radius=4,
                                         width=100,
                                         height=30)
        self.connectButton.grid(row=0, column=3, sticky="e", padx=0, pady=0)
        
        # Statut de la connexion
        statusFrame = ctk.CTkFrame(serialFrame, fg_color="transparent")
        statusFrame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        statusFrame.columnconfigure(0, weight=0)
        statusFrame.columnconfigure(1, weight=1)
        
        statusLabel = ctk.CTkLabel(statusFrame, text="Statut:", 
                                  font=ctk.CTkFont(family=self.museoFonts.get('regular', None), size=14),
                                  text_color=COLOR_PALETTE['text_dark'])
        statusLabel.grid(row=0, column=0, sticky="w", padx=(0, 10), pady=0)
        
        self.statusValue = ctk.CTkLabel(statusFrame, 
                                      textvariable=self.connectionStatus,
                                      font=ctk.CTkFont(family=self.museoFonts.get('bold', None), size=14),
                                      text_color=COLOR_PALETTE['text_muted'])
        self.statusValue.grid(row=0, column=1, sticky="w", padx=0, pady=0)

    # Crée la section de connexion à la base de données.
    def createDatabaseSection(self, parent):
        """
        Args:
            parent: Le widget parent
        """
        # Cadre pour la connexion à la base de données
        dbFrame = ctk.CTkFrame(parent, fg_color=COLOR_PALETTE['bg_card'], corner_radius=8, border_width=1, border_color=COLOR_PALETTE['border'])
        dbFrame.grid(row=1, column=0, sticky="ew", padx=0, pady=(0, 20))
        dbFrame.columnconfigure(0, weight=1)
        
        # Titre de la section
        dbTitle = ctk.CTkLabel(dbFrame, text="Connexion à la base de données", 
                              font=ctk.CTkFont(family=self.museoFonts.get('bold', None), size=16),
                              text_color=COLOR_PALETTE['text_dark'])
        dbTitle.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))
        
        # Cadre pour les contrôles
        dbControls = ctk.CTkFrame(dbFrame, fg_color="transparent")
        dbControls.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        dbControls.columnconfigure(0, weight=0)
        dbControls.columnconfigure(1, weight=1)
        
        # Hôte
        hostLabel = ctk.CTkLabel(dbControls, text="Hôte:", 
                                font=ctk.CTkFont(family=self.museoFonts.get('regular', None), size=14),
                                text_color=COLOR_PALETTE['text_dark'])
        hostLabel.grid(row=0, column=0, sticky="w", padx=(0, 10), pady=(0, 10))
        
        hostEntry = ctk.CTkEntry(dbControls, 
                                textvariable=self.dbHost,
                                font=ctk.CTkFont(family=self.museoFonts.get('regular', None), size=14),
                                border_color=COLOR_PALETTE['border'],
                                fg_color=COLOR_PALETTE['bg_light'])
        hostEntry.grid(row=0, column=1, sticky="ew", padx=0, pady=(0, 10))
        
        # Utilisateur
        userLabel = ctk.CTkLabel(dbControls, text="Utilisateur:", 
                                font=ctk.CTkFont(family=self.museoFonts.get('regular', None), size=14),
                                text_color=COLOR_PALETTE['text_dark'])
        userLabel.grid(row=1, column=0, sticky="w", padx=(0, 10), pady=(0, 10))
        
        userEntry = ctk.CTkEntry(dbControls, 
                                textvariable=self.dbUser,
                                font=ctk.CTkFont(family=self.museoFonts.get('regular', None), size=14),
                                border_color=COLOR_PALETTE['border'],
                                fg_color=COLOR_PALETTE['bg_light'])
        userEntry.grid(row=1, column=1, sticky="ew", padx=0, pady=(0, 10))
        
        # Mot de passe
        passwordLabel = ctk.CTkLabel(dbControls, text="Mot de passe:", 
                                    font=ctk.CTkFont(family=self.museoFonts.get('regular', None), size=14),
                                    text_color=COLOR_PALETTE['text_dark'])
        passwordLabel.grid(row=2, column=0, sticky="w", padx=(0, 10), pady=(0, 10))
        
        passwordEntry = ctk.CTkEntry(dbControls, 
                                    textvariable=self.dbPassword,
                                    font=ctk.CTkFont(family=self.museoFonts.get('regular', None), size=14),
                                    border_color=COLOR_PALETTE['border'],
                                    fg_color=COLOR_PALETTE['bg_light'],
                                    show="*")
        passwordEntry.grid(row=2, column=1, sticky="ew", padx=0, pady=(0, 10))
        
        # Base de données
        dbNameLabel = ctk.CTkLabel(dbControls, text="Base de données:", 
                                   font=ctk.CTkFont(family=self.museoFonts.get('regular', None), size=14),
                                   text_color=COLOR_PALETTE['text_dark'])
        dbNameLabel.grid(row=3, column=0, sticky="w", padx=(0, 10), pady=(0, 10))
        
        dbNameEntry = ctk.CTkEntry(dbControls, 
                                   textvariable=self.dbName,
                                   font=ctk.CTkFont(family=self.museoFonts.get('regular', None), size=14),
                                   border_color=COLOR_PALETTE['border'],
                                   fg_color=COLOR_PALETTE['bg_light'])
        dbNameEntry.grid(row=3, column=1, sticky="ew", padx=0, pady=(0, 10))
        
        # Boutons de connexion/déconnexion
        buttonsFrame = ctk.CTkFrame(dbControls, fg_color="transparent")
        buttonsFrame.grid(row=4, column=0, columnspan=2, sticky="e", padx=0, pady=(10, 0))
        
        self.disconnectDbButton = ctk.CTkButton(buttonsFrame, text="Déconnecter", 
                                               command=self.onDisconnectDb,
                                               font=ctk.CTkFont(family=self.museoFonts.get('bold', None), size=14),
                                               fg_color=COLOR_PALETTE['bg_light'],
                                               text_color=COLOR_PALETTE['primary'],
                                               hover_color=COLOR_PALETTE['border'],
                                               corner_radius=4,
                                               width=120,
                                               height=30)
        self.disconnectDbButton.grid(row=0, column=0, sticky="e", padx=(0, 10), pady=0)
        
        self.connectDbButton = ctk.CTkButton(buttonsFrame, text="Connecter", 
                                            command=self.onConnectDb,
                                            font=ctk.CTkFont(family=self.museoFonts.get('bold', None), size=14),
                                            fg_color=COLOR_PALETTE['primary'],
                                            text_color=COLOR_PALETTE['text_light'],
                                            hover_color=COLOR_PALETTE['accent'],
                                            corner_radius=4,
                                            width=120,
                                            height=30)
        self.connectDbButton.grid(row=0, column=1, sticky="e", padx=0, pady=0)
        
        # Statut de la connexion
        statusFrame = ctk.CTkFrame(dbFrame, fg_color="transparent")
        statusFrame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        statusFrame.columnconfigure(0, weight=0)
        statusFrame.columnconfigure(1, weight=1)
        
        statusLabel = ctk.CTkLabel(statusFrame, text="Statut:", 
                                  font=ctk.CTkFont(family=self.museoFonts.get('regular', None), size=14),
                                  text_color=COLOR_PALETTE['text_dark'])
        statusLabel.grid(row=0, column=0, sticky="w", padx=(0, 10), pady=0)
        
        self.dbStatusValue = ctk.CTkLabel(statusFrame, 
                                         textvariable=self.dbStatus,
                                         font=ctk.CTkFont(family=self.museoFonts.get('bold', None), size=14),
                                         text_color=COLOR_PALETTE['text_muted'])
        self.dbStatusValue.grid(row=0, column=1, sticky="w", padx=0, pady=0)
            
    # Met à jour la liste des ports disponibles.
    def updatePortsList(self, ports):
        """
        Args:
            ports: Liste des ports disponibles
        """
        self.portCombobox.configure(values=ports)
        if ports and not self.selectedPort.get():
            self.selectedPort.set(ports[0])
    
    # Met à jour le statut de la connexion série.
    def updateSerialStatus(self, isConnected, port=None):
        """
        Args:
            isConnected: Indique si la connexion est établie
            port: Le port connecté
        """
        if isConnected:
            self.connectionStatus.set(f"Connecté à {port}")
            self.statusValue.configure(text_color=COLOR_PALETTE['primary'])
            self.connectButton.configure(text="Déconnecter")
        else:
            self.connectionStatus.set("Non connecté")
            self.statusValue.configure(text_color=COLOR_PALETTE['text_muted'])
            self.connectButton.configure(text="Connecter")

    # Met à jour le statut de la connexion à la base de données.
    def updateDbStatus(self, isConnected, dbName=None):
        """
        Args:
            isConnected: Indique si la connexion est établie
            db_name: Le nom de la base de données connectée
        """
        if isConnected:
            self.dbStatus.set(f"Connecté à {dbName}")
            self.dbStatusValue.configure(text_color=COLOR_PALETTE['primary'])
            self.connectDbButton.configure(state="disabled")
            self.disconnectDbButton.configure(state="normal")
        else:
            self.dbStatus.set("Non connecté")
            self.dbStatusValue.configure(text_color=COLOR_PALETTE['text_muted'])
            self.connectDbButton.configure(state="normal")
            self.disconnectDbButton.configure(state="disabled")

    # Récupère la configuration de la base de données
    def getDbConfig(self):
        """
        Returns:
            Un dictionnaire contenant la configuration de la base de données
        """
        return {
            'host': self.dbHost.get(),
            'user': self.dbUser.get(),
            'password': self.dbPassword.get(),
            'database': self.dbName.get()
        } 