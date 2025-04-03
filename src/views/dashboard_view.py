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
        self.uvIndexVar = ctk.StringVar(value="N/A")
        self.irValueVar = ctk.StringVar(value="N/A")
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
        self.parent.rowconfigure(0, weight=0)  # Contrôles
        self.parent.rowconfigure(1, weight=0)  # Capteurs
        self.parent.rowconfigure(2, weight=1)  # Console
        
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
        
        # Configurer la grille avec 3 colonnes égales et 4 lignes
        self.sensorsContainer.grid_columnconfigure((0, 1, 2), weight=1, uniform="equal")
        self.sensorsContainer.grid_rowconfigure((0, 1, 2, 3), weight=1)
        
        # Première ligne - Air Quality, Distance
        self.airQualityCard = SensorCard(
            self.sensorsContainer, 0, 0, "Air Quality", 
            self.airQualityVar, "src/public/icons/air-quality.png", 
            COLOR_PALETTE['primary'], self.museoFonts, "ppm"
        )

        self.distanceCard = SensorCard(
            self.sensorsContainer, 0, 1, "Distance", 
            self.distanceVar, "src/public/icons/ruler.png", 
            COLOR_PALETTE['primary'], self.museoFonts, "m"
        )
        
        # Deuxième ligne - Luminosité, UV, IR
        self.luminosityCard = SensorCard(
            self.sensorsContainer, 0, 2, "Luminosité", 
            self.luminosityVar, "src/public/icons/sun.png", 
            COLOR_PALETTE['primary'], self.museoFonts, "lux"
        )
        
        self.uvIndexCard = SensorCard(
            self.sensorsContainer, 1, 0, "UV Index", 
            self.uvIndexVar, "src/public/icons/uv.png", 
            COLOR_PALETTE['primary'], self.museoFonts
        )
        
        self.irValueCard = SensorCard(
            self.sensorsContainer, 1, 1, "Infrarouge", 
            self.irValueVar, "src/public/icons/ir.png", 
            COLOR_PALETTE['primary'], self.museoFonts
        )
        
        # Troisième ligne - Température, Humidité, Pression
        self.temperatureCard = SensorCard(
            self.sensorsContainer, 1, 2, "Température", 
            self.temperatureVar, "src/public/icons/thermometer.png", 
            COLOR_PALETTE['primary'], self.museoFonts, "°C"
        )
        
        self.humidityCard = SensorCard(
            self.sensorsContainer, 2, 0, "Humidité", 
            self.humidityVar, "src/public/icons/humidity.png", 
            COLOR_PALETTE['primary'], self.museoFonts, "%"
        )
        
        self.pressureCard = SensorCard(
            self.sensorsContainer, 2, 1, "Pression", 
            self.pressureVar, "src/public/icons/barometer.png", 
            COLOR_PALETTE['primary'], self.museoFonts, "hPa"
        )
    
    # Met à jour les valeurs des capteurs avec les nouvelles données
    def updateSensorValues(self, data):
        """
        Args:
            data: Dictionnaire contenant les valeurs des capteurs
        """
        # Mettre à jour les variables de données si elles existent
        if 'air_quality' in data and data['air_quality'] is not None and data['air_quality'] != 'N/A':
            self.airQualityVar.set(f"{data['air_quality']:.2f}")
        else:
            self.airQualityVar.set("N/A")
         
        if 'distance' in data and data['distance'] is not None and data['distance'] != 'N/A':
            self.distanceVar.set(f"{data['distance']:.2f}")
        else:
            self.distanceVar.set("N/A")
        
        if 'luminosity' in data and data['luminosity'] is not None and data['luminosity'] != 'N/A':
            self.luminosityVar.set(str(data['luminosity']))
        else:
            self.luminosityVar.set("N/A")
        
        if 'uv_index' in data and data['uv_index'] is not None and data['uv_index'] != 'N/A':
            self.uvIndexVar.set(f"{data['uv_index']:.2f}")
        else:
            self.uvIndexVar.set("N/A")
        
        if 'ir_value' in data and data['ir_value'] is not None and data['ir_value'] != 'N/A':
            self.irValueVar.set(str(data['ir_value']))
        else:
            self.irValueVar.set("N/A")
        
        if 'temperature' in data and data['temperature'] is not None and data['temperature'] != 'N/A':
            self.temperatureVar.set(f"{data['temperature']:.1f}")
        else:
            self.temperatureVar.set("N/A")
        
        if 'humidity' in data and data['humidity'] is not None and data['humidity'] != 'N/A':
            self.humidityVar.set(str(data['humidity']))
        else:
            self.humidityVar.set("N/A")
        
        if 'pressure' in data and data['pressure'] is not None and data['pressure'] != 'N/A':
            self.pressureVar.set(str(data['pressure']))
        else:
            self.pressureVar.set("N/A")
    
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