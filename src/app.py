
import customtkinter as ctk
import os

from config.settings import COLOR_PALETTE
from src.views.dashboard_view import DashboardView
from src.views.tables_view import TablesView
from src.views.settings_view import SettingsView
from src.controllers.dashboard_controller import DashboardController
from src.controllers.table_controller import TableController
from src.controllers.settings_controller import SettingsController
from src.services.sensor_service import SensorService
from src.database.connection import DatabaseConnection
from src.database.query_manager import QueryManager
from src.utils.console_redirector import ConsoleRedirector

# Classe principale de l'application de tableau de bord des capteurs.
class SensorDashboardApp:
    # Initialise l'application avec la fenêtre racine.
    def __init__(self, root):
        """
        Args:
            root: La fenêtre racine Tkinter
        """
        self.root = root
        self.root.title("Tableau de bord des capteurs")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Configurer la grille principale
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Charger les polices Museo
        self.museoFonts = self.loadMuseoFonts()
        
        # Initialiser les services
        self.dbConnection = DatabaseConnection()
        
        # Vérifier si la connexion à la base de données est établie
        if self.dbConnection.isConnected():
            self.queryManager = QueryManager(self.dbConnection.connection)
        else:
            self.queryManager = QueryManager(None)
            print("Attention: Connexion à la base de données non établie. Certaines fonctionnalités seront limitées.")
            
        self.sensorService = SensorService()
        
        # Variables pour le mode démo
        self.demoActive = False
        
        # Créer l'interface utilisateur
        self.createUi()
        
        # Configurer les événements de redimensionnement
        self.root.bind("<Configure>", self.onWindowResize)
    
    # Charge les polices Museo depuis le dossier src/public/fonts/museo/
    def loadMuseoFonts(self):
        """Charge les polices Museo depuis le dossier src/public/fonts/museo/"""
        museoFonts = {}
        
        # Chemin vers le dossier des polices Museo
        museoDir = os.path.join('src', 'public', 'fonts', 'museo')
        
        # Vérifier si le dossier existe
        if not os.path.exists(museoDir):
            print(f"Attention: Le dossier {museoDir} n'existe pas.")
            return museoFonts
            
        # Charger les polices Museo
        try:
            # Enregistrer les polices dans Tkinter
            museo100 = os.path.join(museoDir, 'MuseoSans-100.otf')
            museo300 = os.path.join(museoDir, 'MuseoSans-300.otf')
            museo500 = os.path.join(museoDir, 'MuseoSans_500.otf')
            museo700 = os.path.join(museoDir, 'MuseoSans_700.otf')
            museo900 = os.path.join(museoDir, 'MuseoSans_900.otf')
            
            # Vérifier l'existence de chaque fichier
            if os.path.exists(museo100):
                self.root.tk.call('font', 'create', 'MuseoSans-100', '-family', 'MuseoSans', '-weight', 'normal')
                museoFonts['thin'] = 'MuseoSans-100'
                
            if os.path.exists(museo300):
                self.root.tk.call('font', 'create', 'MuseoSans-300', '-family', 'MuseoSans', '-weight', 'normal')
                museoFonts['light'] = 'MuseoSans-300'
                
            if os.path.exists(museo500):
                self.root.tk.call('font', 'create', 'MuseoSans_500', '-family', 'MuseoSans', '-weight', 'normal')
                museoFonts['regular'] = 'MuseoSans_500'
                
            if os.path.exists(museo700):
                self.root.tk.call('font', 'create', 'MuseoSans_700', '-family', 'MuseoSans', '-weight', 'bold')
                museoFonts['bold'] = 'MuseoSans_700'
                
            if os.path.exists(museo900):
                self.root.tk.call('font', 'create', 'MuseoSans_900', '-family', 'MuseoSans', '-weight', 'bold')
                museoFonts['black'] = 'MuseoSans_900'
                
            print("Polices Museo chargées avec succès.")
        except Exception as e:
            print(f"Erreur lors du chargement des polices Museo: {e}")
            
        return museoFonts
    
    # Crée l'interface utilisateur principale
    def createUi(self):
        # Créer le cadre principal avec le fond clair
        self.mainFrame = ctk.CTkFrame(self.root, fg_color=COLOR_PALETTE['bg_light'])
        self.mainFrame.grid(row=0, column=0, sticky="nsew")
        self.mainFrame.grid_columnconfigure(0, weight=1)
        self.mainFrame.grid_rowconfigure(1, weight=1)
        
        # Créer la barre de navigation
        self.createNavbar()
        
        # Créer le conteneur de contenu
        self.contentFrame = ctk.CTkFrame(self.mainFrame, fg_color="transparent")
        self.contentFrame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.contentFrame.grid_columnconfigure(0, weight=1)
        self.contentFrame.grid_rowconfigure(0, weight=1)
        
        # Créer les vues
        self.createViews()
        
        # Afficher la vue du tableau de bord par défaut
        self.switchTab("dashboard")
    
    # Crée la barre de navigation
    def createNavbar(self):
        # Cadre pour la barre de navigation
        navbar = ctk.CTkFrame(self.mainFrame, fg_color=COLOR_PALETTE['primary'], height=60)
        navbar.grid(row=0, column=0, sticky="ew")
        navbar.grid_propagate(False)
        
        # Configurer la grille de la barre de navigation
        navbar.grid_columnconfigure(0, weight=1)
        navbar.grid_columnconfigure(1, weight=1)
        navbar.grid_columnconfigure(2, weight=1)
        navbar.grid_rowconfigure(0, weight=1)
        
        # Variable pour l'onglet actif
        self.activeTab = ctk.StringVar(value="dashboard")
        
        # Bouton pour le tableau de bord
        dashboardBtn = ctk.CTkButton(navbar, text="Tableau de bord", 
                                    command=lambda: self.switchTab("dashboard"),
                                    font=ctk.CTkFont(family=self.museoFonts.get('bold', None), size=14),
                                    fg_color="transparent",
                                    text_color=COLOR_PALETTE['text_light'],
                                    hover_color=COLOR_PALETTE['accent'],
                                    corner_radius=0,
                                    height=60)
        dashboardBtn.grid(row=0, column=0, sticky="nsew")
        
        # Bouton pour les tables
        tablesBtn = ctk.CTkButton(navbar, text="Tables", 
                                 command=lambda: self.switchTab("tables"),
                                 font=ctk.CTkFont(family=self.museoFonts.get('bold', None), size=14),
                                 fg_color="transparent",
                                 text_color=COLOR_PALETTE['text_light'],
                                 hover_color=COLOR_PALETTE['accent'],
                                 corner_radius=0,
                                 height=60)
        tablesBtn.grid(row=0, column=1, sticky="nsew")
        
        # Bouton pour les paramètres
        settingsBtn = ctk.CTkButton(navbar, text="Paramètres", 
                                   command=lambda: self.switchTab("settings"),
                                   font=ctk.CTkFont(family=self.museoFonts.get('bold', None), size=14),
                                   fg_color="transparent",
                                   text_color=COLOR_PALETTE['text_light'],
                                   hover_color=COLOR_PALETTE['accent'],
                                   corner_radius=0,
                                   height=60)
        settingsBtn.grid(row=0, column=2, sticky="nsew")
        
        # Stocker les boutons pour pouvoir les mettre à jour
        self.navButtons = {
            "dashboard": dashboardBtn,
            "tables": tablesBtn,
            "settings": settingsBtn
        }
    
    # Crée les différentes vues de l'application
    def createViews(self):
        # Créer les frames pour chaque vue
        self.dashboardFrame = ctk.CTkFrame(self.contentFrame, fg_color="transparent")
        self.tablesFrame = ctk.CTkFrame(self.contentFrame, fg_color="transparent")
        self.settingsFrame = ctk.CTkFrame(self.contentFrame, fg_color="transparent")
        
        # Configurer les frames
        for frame in [self.dashboardFrame, self.tablesFrame, self.settingsFrame]:
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_rowconfigure(0, weight=1)
        
        # Créer les vues
        self.dashboardView = DashboardView(
            self.dashboardFrame, 
            self.museoFonts,
            onStart=self.startDataReading,
            onStop=self.stopDataReading,
            onToggleDemo=self.toggleDemoMode
        )
        self.tablesView = TablesView(
            self.tablesFrame, 
            self.museoFonts, 
            onTableSelect=self.onTableSelect, 
            onRefreshTables=self.refreshTablesList
        )
        self.settingsView = SettingsView(
            self.settingsFrame,
            self.museoFonts,
            onConnectPort=self.connectToPort,
            onRefreshPorts=self.refreshPorts,
            onConnectDb=self.connectToDb,
            onDisconnectDb=self.disconnectFromDb
        )
        
        # Créer les contrôleurs
        self.dashboardController = DashboardController(
            self.dashboardView, 
            self.sensorService, 
            self.dbConnection.connection
        )
        self.tableController = TableController(
            self.tablesView, 
            self.queryManager
        )
        self.settingsController = SettingsController(
            self.settingsView,
            self.dbConnection,
            self.sensorService
        )
        
        # Rediriger la sortie console vers la console de l'application
        self.consoleRedirector = ConsoleRedirector(self.dashboardView.console)
        
        # Initialiser les données des tables si la connexion est établie
        if self.dbConnection.isConnected():
            self.refreshTablesList()
    
    # Change l'onglet actif.
    def switchTab(self, tabName):
        """
        Args:
            tabName: Nom de l'onglet à afficher
        """
        # Mettre à jour la variable d'onglet actif
        self.activeTab.set(tabName)
        
        # Masquer toutes les vues
        self.dashboardFrame.grid_forget()
        self.tablesFrame.grid_forget()
        self.settingsFrame.grid_forget()
        
        # Afficher la vue sélectionnée
        if tabName == "dashboard":
            self.dashboardFrame.grid(row=0, column=0, sticky="nsew")
        elif tabName == "tables":
            self.tablesFrame.grid(row=0, column=0, sticky="nsew")
        elif tabName == "settings":
            self.settingsFrame.grid(row=0, column=0, sticky="nsew")
        
        # Mettre à jour l'apparence des boutons de navigation
        for name, button in self.navButtons.items():
            if name == tabName:
                button.configure(fg_color=COLOR_PALETTE['accent'])
            else:
                button.configure(fg_color="transparent")
    
    # Gère l'événement de sélection d'une table.
    def onTableSelect(self, tableName):
        """  
        Args:
            table_name: Nom de la table sélectionnée
        """
        self.tableController.loadTableData(tableName)
    
    # Rafraîchit la liste des tables.
    def refreshTablesList(self):
        if not self.dbConnection.isConnected():
            print("Impossible de rafraîchir la liste des tables : connexion à la base de données non établie")
            return
            
        self.tableController.refreshTablesList()
    
    # Se connecte ou se déconnecte du port série sélectionné.
    def connectToPort(self):
        self.settingsController.connectToPort()
    
    # Rafraîchit la liste des ports série disponibles.
    def refreshPorts(self):
        self.settingsController.refreshPorts()
    
    # Se connecte à la base de données avec les paramètres fournis.
    def connectToDb(self):
        self.settingsController.connectToDb()
        
        # Rafraîchir la liste des tables si la connexion est établie
        if self.dbConnection.isConnected():
            self.refreshTablesList()
    
    # Se déconnecte de la base de données.
    def disconnectFromDb(self):
        self.settingsController.disconnectFromDb()
    
    # Active ou désactive le mode démo.
    def toggleDemoMode(self):
        self.demoActive = not self.demoActive
        self.dashboardController.toggleDemoMode()
    
    # Gère l'événement de redimensionnement de la fenêtre pour adapter l'interface.
    def onWindowResize(self, event=None):
        # Mettre à jour les composants qui doivent être redimensionnés
        pass
    
    # Démarre l'application.
    def start(self):
        # Démarrer la lecture des données si la connexion est établie
        if self.sensorService.isAvailable():
            self.dashboardController.startDataReading()
        
        # Démarrer la boucle principale
        self.root.mainloop()
    
    # Arrête l'application proprement.
    def stop(self):
        # Arrêter la lecture des données
        self.dashboardController.stopDataReading()
        
        # Arrêter le rafraîchissement automatique des tables
        self.tableController.stopAutoRefresh()
        
        # Fermer la connexion à la base de données
        self.dbConnection.disconnect()
        
        # Fermer la fenêtre
        self.root.destroy()
    
    # Démarre la lecture des données des capteurs.
    def startDataReading(self):
        self.dashboardController.startDataReading()
        self.dashboardView.logToConsole("Lecture des données démarrée")
    
    # Arrête la lecture des données des capteurs.
    def stopDataReading(self):
        self.dashboardController.stopDataReading()
        self.dashboardView.logToConsole("Lecture des données arrêtée") 