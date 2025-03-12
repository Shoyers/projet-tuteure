import tkinter as tk;
from tkinter import ttk;

# Crée un indicateur LED circulaire avec un design amélioré
def createLed(parent, color, size=20):
    """Crée un indicateur LED circulaire avec un design amélioré"""
    led = tk.Canvas(parent, width=size, height=size, bg='#f5f7fa', highlightthickness=0);
    
    # Créer un effet d'ombre pour donner de la profondeur
    led.create_oval(1, 1, size-1, size-1, fill='#d0d0d0', outline='#c0c0c0');
    
    # Créer un effet de profondeur avec un cercle extérieur plus sombre
    led.create_oval(2, 2, size-2, size-2, fill='#e0e0e0', outline='#d0d0d0');
    
    # Créer le cercle intérieur (la LED elle-même)
    led.create_oval(4, 4, size-4, size-4, fill=color, outline=color);
    
    # Ajouter un effet de brillance pour un aspect plus réaliste
    highlight_size = size // 3;
    led.create_oval(5, 5, 5 + highlight_size, 5 + highlight_size, fill='white', outline='', stipple='gray50');
    
    return led;

# Crée une ligne d'affichage pour un capteur
def createSensorRow(parent, row, icon, title, valueVar, hasProgress=True, color='#3498DB'):
    """Crée une ligne d'affichage pour un capteur"""
    # Frame pour contenir tous les éléments de la ligne
    rowFrame = ttk.Frame(parent);
    rowFrame.grid(row=row, column=0, columnspan=4, sticky='ew', padx=5, pady=10);
    rowFrame.columnconfigure(3, weight=1);
    
    # Conteneur pour l'icône avec un fond coloré
    iconContainer = tk.Frame(rowFrame, bg=color, width=40, height=40);
    iconContainer.grid(row=0, column=0, padx=10, pady=5);
    iconContainer.grid_propagate(False);  # Empêche le redimensionnement
    
    # Icône
    iconLabel = ttk.Label(iconContainer, text=icon, font=('Segoe UI', 18), background=color, foreground='white');
    iconLabel.place(relx=0.5, rely=0.5, anchor='center');
    
    # Titre
    titleLabel = ttk.Label(rowFrame, text=title, style='Title.TLabel');
    titleLabel.grid(row=0, column=1, padx=10, pady=5, sticky='w');
    
    # Valeur
    valueLabel = ttk.Label(rowFrame, textvariable=valueVar, style='Value.TLabel');
    valueLabel.grid(row=0, column=2, padx=10, pady=5);
    
    # Barre de progression (optionnelle)
    if hasProgress:
        progress = ttk.Progressbar(rowFrame, length=150, mode='determinate', style='Horizontal.TProgressbar');
        progress.grid(row=0, column=3, padx=10, pady=5, sticky='ew');
        return progress, valueLabel;
    
    return None, valueLabel;

# Redirige la sortie standard vers un widget Text de Tkinter
class ConsoleRedirector:
    def __init__(self, textWidget):
        self.textWidget = textWidget;
        
        # Définir des couleurs pour différents types de messages
        self.textWidget.tag_configure('error', foreground='#E74C3C');
        self.textWidget.tag_configure('success', foreground='#2ECC71');
        self.textWidget.tag_configure('info', foreground='#3498DB');
        self.textWidget.tag_configure('warning', foreground='#F39C12');
        
        # Ajouter des styles pour les timestamps et les types de messages
        self.textWidget.tag_configure('timestamp', foreground='#7F8C8D');
        self.textWidget.tag_configure('bold', font=('Consolas', 10, 'bold'));
    
    def write(self, string):
        self.textWidget.config(state=tk.NORMAL);
        
        # Ajouter un timestamp pour les nouvelles lignes
        if string.startswith(('Erreur', 'Port', 'Connexion', 'Déconnexion', 'Mode', 'Données', 'Démarrage', 'Arrêt')):
            from datetime import datetime;
            timestamp = datetime.now().strftime('[%H:%M:%S] ');
            self.textWidget.insert(tk.END, timestamp, 'timestamp');
        
        # Appliquer des tags de couleur en fonction du contenu du message
        if 'Erreur' in string or 'erreur' in string or 'Échec' in string:
            self.textWidget.insert(tk.END, string, ('error', 'bold'));
        elif 'succès' in string or 'établie' in string or 'disponible' in string or 'insérées' in string:
            self.textWidget.insert(tk.END, string, ('success', 'bold'));
        elif 'Démarrage' in string or 'activé' in string or 'Données' in string:
            self.textWidget.insert(tk.END, string, ('info', 'bold'));
        elif 'Arrêt' in string or 'désactivé' in string or 'Utilisez' in string:
            self.textWidget.insert(tk.END, string, ('warning', 'bold'));
        else:
            self.textWidget.insert(tk.END, string);
            
        self.textWidget.see(tk.END);
        self.textWidget.config(state=tk.DISABLED);
    
    def flush(self):
        pass; 