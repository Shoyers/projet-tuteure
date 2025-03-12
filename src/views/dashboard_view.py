import tkinter as tk
import customtkinter as ctk
from config.settings import COLOR_PALETTE
from src.views.components.sensor_card import SensorCard

# Vue du tableau de bord qui affiche les valeurs des capteurs et la console.
class DashboardView:
    # Initialise la vue du tableau de bord.
    def __init__(self, parent, museoFonts, onStart=None, onStop=None, onToggleDemo=None):
        """
        Args:
            parent: Le widget parent
            museoFonts: Dictionnaire des polices Museo
            onStart: Fonction à appeler pour démarrer la lecture des données
            onStop: Fonction à appeler pour arrêter la lecture des données
            on_toggle_demo: Fonction à appeler pour activer/désactiver le mode démo
        """
        self.parent = parent
        self.museoFonts = museoFonts
        self.onStart = onStart
        self.onStop = onStop
        self.onToggleDemo = onToggleDemo
        
        # Variables pour les valeurs des capteurs
        self.airQualityVar = ctk.StringVar(value="N/A")
        self.distanceVar = ctk.StringVar(value="N/A")
        self.luminosityVar = ctk.StringVar(value="N/A")
        self.temperatureVar = ctk.StringVar(value="N/A")
        self.humidityVar = ctk.StringVar(value="N/A")
        self.pressureVar = ctk.StringVar(value="N/A")
        
        # Variables pour l'état des boutons
        self.isReading = False
        self.isDemoActive = False
        
        # Créer le contenu du tableau de bord
        self.createDashboardContent()
        
    # Crée le contenu du tableau de bord
    def createDashboardContent(self):
        # Configuration de la grille
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(1, weight=0)  # Contrôles
        self.parent.rowconfigure(2, weight=0)  # Capteurs
        self.parent.rowconfigure(3, weight=1)  # Console
        
        # Section des contrôles
        self.createControlsSection()
        
        # Section capteurs
        sensorSection = ctk.CTkFrame(self.parent, fg_color="transparent");
        sensorSection.grid(row=1, column=0, sticky="ew", padx=0, pady=(0, 20));
        sensorSection.grid_columnconfigure(0, weight=1);
        
        # Titre de la section capteurs
        sensorTitle = ctk.CTkLabel(sensorSection, text="Valeurs des capteurs", 
                                  font=ctk.CTkFont(family=self.museoFonts.get('black', None), size=18),
                                  text_color=COLOR_PALETTE['text_dark']);
        sensorTitle.grid(row=0, column=0, sticky="w", padx=20, pady=(0, 15));
        
        # Conteneur pour les cartes de capteurs
        sensorCardsContainer = ctk.CTkFrame(sensorSection, fg_color="transparent");
        sensorCardsContainer.grid(row=1, column=0, sticky="ew", padx=0, pady=0);
        
        # Création des lignes de capteurs
        self.createModernSensorRows(sensorCardsContainer);
        
        # Section console
        consoleSection = ctk.CTkFrame(self.parent, fg_color="transparent");
        consoleSection.grid(row=2, column=0, sticky="nsew", padx=0, pady=0);
        consoleSection.columnconfigure(0, weight=1);
        consoleSection.rowconfigure(1, weight=1);
        
        # Titre de la section console
        consoleTitle = ctk.CTkLabel(consoleSection, text="Console", 
                                   font=ctk.CTkFont(family=self.museoFonts.get('black', None), size=18),
                                   text_color=COLOR_PALETTE['text_dark']);
        consoleTitle.grid(row=0, column=0, sticky="w", padx=0, pady=(0, 15));
        
        # Console
        consoleCard = ctk.CTkFrame(consoleSection, fg_color=COLOR_PALETTE['bg_card'], corner_radius=8, border_width=1, border_color=COLOR_PALETTE['border']);
        consoleCard.grid(row=1, column=0, sticky="nsew", padx=0, pady=0);
        consoleCard.columnconfigure(0, weight=1);
        consoleCard.rowconfigure(0, weight=1);
        
        self.console = ctk.CTkTextbox(consoleCard, 
                                    font=ctk.CTkFont(family="Consolas", size=12),
                                    fg_color=COLOR_PALETTE['bg_card'], 
                                    border_width=0,
                                    text_color=COLOR_PALETTE['text_dark']);
        self.console.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
    
    def createControlsSection(self):
        """Crée la section des contrôles avec les boutons"""
        # Conteneur pour les contrôles
        controlsContainer = ctk.CTkFrame(self.parent, fg_color=COLOR_PALETTE['bg_card'], corner_radius=8, border_width=1, border_color=COLOR_PALETTE['border']);
        controlsContainer.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 20));
        controlsContainer.grid_columnconfigure(0, weight=1);
        controlsContainer.grid_columnconfigure(1, weight=0);
        controlsContainer.grid_columnconfigure(2, weight=0);
        
        # Titre de la section
        controlsTitle = ctk.CTkLabel(controlsContainer, text="Contrôles", 
                                    font=ctk.CTkFont(family=self.museoFonts.get('bold', None), size=16),
                                    text_color=COLOR_PALETTE['text_dark']);
        controlsTitle.grid(row=0, column=0, sticky="w", padx=20, pady=15);
        
        # Boutons de contrôle
        self.buttonsFrame = ctk.CTkFrame(controlsContainer, fg_color="transparent");
        self.buttonsFrame.grid(row=0, column=2, padx=15, pady=10, sticky="e");
        
        # Bouton de démarrage
        self.startButton = ctk.CTkButton(self.buttonsFrame, text="Démarrer", 
                                        command=self._onStartClick,
                                        font=ctk.CTkFont(family=self.museoFonts.get('bold', None), size=13),
                                        fg_color=COLOR_PALETTE['bg_light'],
                                        text_color=COLOR_PALETTE['primary'],
                                        hover_color=COLOR_PALETTE['border'],
                                        corner_radius=4,
                                        height=30,
                                        width=100);
        self.startButton.grid(row=0, column=0, padx=(0, 10));
        
        # Bouton d'arrêt
        self.stopButton = ctk.CTkButton(self.buttonsFrame, text="Arrêter", 
                                       command=self._onStopClick,
                                       font=ctk.CTkFont(family=self.museoFonts.get('bold', None), size=13),
                                       fg_color=COLOR_PALETTE['danger'],
                                       hover_color="#c82333",
                                       corner_radius=4,
                                       height=30,
                                       width=100,
                                       state="disabled");
        self.stopButton.grid(row=0, column=1, padx=(0, 10));
        
        # Bouton mode démo
        self.demoButton = ctk.CTkButton(self.buttonsFrame, text="Mode démo", 
                                       command=self._onToggleDemoClick,
                                       font=ctk.CTkFont(family=self.museoFonts.get('bold', None), size=13),
                                       fg_color=COLOR_PALETTE['bg_light'],
                                       text_color=COLOR_PALETTE['primary'],
                                       hover_color=COLOR_PALETTE['border'],
                                       corner_radius=4,
                                       height=30,
                                       width=100)
        self.demoButton.grid(row=0, column=2);
    
    # Gère le clic sur le bouton Démarrer
    def _onStartClick(self):
        if self.onStart:
            self.onStart()
            self.updateButtonStates(isReading=True)
    
    # Gère le clic sur le bouton Arrêter
    def _onStopClick(self):
        if self.onStop:
            self.onStop()
            self.updateButtonStates(isReading=False)
    
    # Gère le clic sur le bouton Mode démo
    def _onToggleDemoClick(self):
        if self.onToggleDemo:
            self.onToggleDemo()
            self.isDemoActive = not self.isDemoActive
            self.updateDemoButtonState()
    
    # Met à jour l'état des boutons en fonction de l'état de lecture
    def updateButtonStates(self, isReading):
        self.isReading = isReading
        
        if isReading:
            self.startButton.configure(state="disabled")
            self.stopButton.configure(state="normal")
        else:
            self.startButton.configure(state="normal")
            self.stopButton.configure(state="disabled")
    
    # Met à jour l'état du bouton Mode démo
    def updateDemoButtonState(self):
        if self.isDemoActive:
            self.demoButton.configure(text="Désactiver démo")
        else:
            self.demoButton.configure(text="Mode démo")
    
    # Crée les rangées de capteurs dans un style moderne
    def createModernSensorRows(self, frame):
        # Créer un conteneur pour les capteurs principaux
        self.sensorsContainer = ctk.CTkFrame(frame, fg_color="transparent")
        self.sensorsContainer.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)
        
        # Configurer la grille avec 3 colonnes égales
        self.sensorsContainer.grid_columnconfigure((0, 1, 2), weight=1, uniform="equal")
        
        # Créer les cartes de capteurs avec les icônes spécifiques
        self.airQualityCard = SensorCard(
            self.sensorsContainer, 0, 0, "Qualité de l'air", 
            self.airQualityVar, "src/public/icons/wind.png", 
            COLOR_PALETTE['primary'], self.museoFonts
        )
        
        self.distanceCard = SensorCard(
            self.sensorsContainer, 0, 1, "Distance", 
            self.distanceVar, "src/public/icons/ruler.png", 
            COLOR_PALETTE['primary'], self.museoFonts
        )
        
        self.luminosityCard = SensorCard(
            self.sensorsContainer, 0, 2, "Luminosité", 
            self.luminosityVar, "src/public/icons/sun.png", 
            COLOR_PALETTE['primary'], self.museoFonts
        )
        
        # Créer un conteneur pour le titre BME680
        bmeTitleContainer = ctk.CTkFrame(frame, fg_color="transparent")
        bmeTitleContainer.grid(row=1, column=0, sticky="nsew", padx=20, pady=(20, 5))
        bmeTitleContainer.grid_columnconfigure(0, weight=1)
        
        # Titre pour la section BME680
        bmeSectionTitle = ctk.CTkLabel(bmeTitleContainer, text="Capteur BME680", 
                                       font=ctk.CTkFont(family=self.museoFonts.get('bold', None), size=16),
                                       text_color=COLOR_PALETTE['text_dark'])
        bmeSectionTitle.grid(row=0, column=0, sticky="w")
        
        # Créer un conteneur pour les cartes BME680
        bmeContainer = ctk.CTkFrame(frame, fg_color="transparent")
        bmeContainer.grid(row=2, column=0, sticky="nsew", padx=20, pady=5)
        bmeContainer.grid_columnconfigure((0, 1, 2), weight=1, uniform="equal")
        
        # Créer des cartes individuelles pour chaque mesure BME680
        self.temperatureCard = SensorCard(
            bmeContainer, 0, 0, "Température", 
            self.temperatureVar, "src/public/icons/thermometer-sun.png", 
            COLOR_PALETTE['primary'], self.museoFonts
        )
        
        self.humidityCard = SensorCard(
            bmeContainer, 0, 1, "Humidité", 
            self.humidityVar, "src/public/icons/droplets.png", 
            COLOR_PALETTE['primary'], self.museoFonts
        )
        
        self.pressureCard = SensorCard(
            bmeContainer, 0, 2, "Pression", 
            self.pressureVar, "src/public/icons/circle-gauge.png", 
            COLOR_PALETTE['primary'], self.museoFonts
        )
    
    # Met à jour les valeurs des capteurs affichées dans le tableau de bord.
    def updateSensorValues(self, data):
        """  
        Args:
            data: Dictionnaire contenant les valeurs des capteurs
        """
        # Mettre à jour les variables StringVar
        if 'airQuality' in data:
            self.airQualityVar.set(f"{data['airQuality']} PPM")
        
        if 'distance' in data:
            self.distanceVar.set(f"{data['distance']} m")
        
        if 'luminosity' in data:
            self.luminosityVar.set(f"{data['luminosity']} lux")
        
        if 'temperature' in data:
            self.temperatureVar.set(f"{data['temperature']} °C")
        
        if 'humidity' in data:
            self.humidityVar.set(f"{data['humidity']} %")
        
        if 'pressure' in data:
            self.pressureVar.set(f"{data['pressure']} hPa")
    
    # Ajoute un message à la console.
    def logToConsole(self, message):
        """
        Args:
            message: Le message à ajouter
        """
        self.console.insert(tk.END, f"{message}\n")
        self.console.see(tk.END)
    
    # Efface le contenu de la console.
    def clearConsole(self):
        self.console.delete(1.0, tk.END) 