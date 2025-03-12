import tkinter as tk;
from datetime import datetime;

# Redirige la sortie standard vers un widget CTkTextbox
class ConsoleRedirector:
    # Initialise le redirigeur de console
    def __init__(self, textWidget):
        self.textWidget = textWidget;
    
    # Écrit une chaîne dans le widget
    def write(self, string):
        # Ajouter un timestamp pour les nouvelles lignes
        if string.startswith(('Erreur', 'Port', 'Connexion', 'Déconnexion', 'Mode', 'Données', 'Démarrage', 'Arrêt')):
            timestamp = datetime.now().strftime('[%H:%M:%S] ');
            self.textWidget.insert(tk.END, timestamp);
        
        # Appliquer des couleurs en fonction du contenu du message
        if 'Erreur' in string or 'erreur' in string or 'Échec' in string:
            self.textWidget.insert(tk.END, string);
        elif 'succès' in string or 'établie' in string or 'disponible' in string or 'insérées' in string:
            self.textWidget.insert(tk.END, string);
        elif 'Démarrage' in string or 'activé' in string or 'Données' in string:
            self.textWidget.insert(tk.END, string);
        elif 'Arrêt' in string or 'désactivé' in string or 'Utilisez' in string:
            self.textWidget.insert(tk.END, string);
        else:
            self.textWidget.insert(tk.END, string);
            
        self.textWidget.see(tk.END);
    
    # Vide le tampon de sortie
    def flush(self):
        pass; 