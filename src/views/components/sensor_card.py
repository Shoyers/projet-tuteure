import customtkinter as ctk;
from config.settings import COLOR_PALETTE;

# Composant réutilisable pour afficher une carte de capteur
class SensorCard:
    # Initialise une carte de capteur
    def __init__(self, parent, row, col, title, valueVar, iconPath, color, museoFonts):
        """      
        Args:
            parent: Le widget parent
            row: La ligne dans la grille
            col: La colonne dans la grille
            title: Le titre de la carte
            value_var: La variable StringVar contenant la valeur
            icon_path: Le chemin vers l'icône
            color: La couleur du texte de la valeur
            museo_fonts: Dictionnaire des polices Museo
        """
        self.parent = parent;
        self.row = row;
        self.col = col;
        self.title = title;
        self.valueVar = valueVar;
        self.iconPath = iconPath;
        self.color = color;
        self.museoFonts = museoFonts;
        
        # Créer la carte
        self.card = self._createCard();
    
    # Crée une carte de capteur dans le style moderne avec une taille fixe
    def _createCard(self):
        # Créer la carte avec une taille fixe
        card = ctk.CTkFrame(self.parent, fg_color=COLOR_PALETTE['bg_card'], corner_radius=8, 
                          border_width=1, border_color=COLOR_PALETTE['border'],
                          width=200, height=120)  # Dimensions fixes
        card.grid(row=self.row, column=self.col, sticky="nsew", padx=10, pady=10)
        card.grid_propagate(False)  # Empêcher la propagation de la grille (taille fixe)
        
        # Configurer les colonnes de la carte
        card.grid_columnconfigure(0, weight=1)
        
        # Titre de la carte
        titleLabel = ctk.CTkLabel(card, text=self.title, 
                                 font=ctk.CTkFont(family=self.museoFonts.get('bold', None), size=16),
                                 text_color=COLOR_PALETTE['text_dark']);
        titleLabel.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10));
        
        # Créer un frame pour la valeur avec une taille fixe
        valueFrame = ctk.CTkFrame(card, fg_color="transparent", width=160, height=40);
        valueFrame.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 20));
        valueFrame.grid_propagate(False);  # Empêcher la propagation de la grille
        
        # Valeur (en grand et en couleur)
        valueLabel = ctk.CTkLabel(valueFrame, 
                                 textvariable=self.valueVar,
                                 font=ctk.CTkFont(family=self.museoFonts.get('bold', None), size=28),
                                 text_color=self.color,
                                 anchor="w");  # Alignement à gauche
        valueLabel.place(x=0, y=0, relwidth=1, relheight=1);  # Utiliser place au lieu de grid
        
        return card;
    
    # Met à jour la valeur affichée dans la carte
    def updateValue(self, newValue):
        """
        Args:
            newValue: La nouvelle valeur à afficher
        """
        self.valueVar.set(newValue);
    
    # Retourne le widget de la carte
    def getWidget(self):
        """
        Returns:
            Le widget CTkFrame de la carte
        """
        return self.card;