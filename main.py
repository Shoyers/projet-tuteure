import customtkinter as ctk
import sys
from src.app import SensorDashboardApp
from src.database.connection import DatabaseConnection

# Vérifier la disponibilité des modules
try:
    serialAvailable = True
except Exception as e:
    serialAvailable = False
    serialErrorMessage = str(e)

# Tentative de connexion à MySQL
db = DatabaseConnection()
mysqlAvailable = db.isConnected()
mysqlErrorMessage = db.errorMessage if not mysqlAvailable else ''

# Configuration de CustomTkinter
ctk.set_appearance_mode("light")  # Mode clair
ctk.set_default_color_theme("blue")  # Thème bleu

# Fonction principale de l'application.
def main():
    # Créer la fenêtre racine
    root = ctk.CTk()
    
    # Créer l'application
    app = SensorDashboardApp(root)
    
    try:
        # Démarrer l'application
        app.start()
    except KeyboardInterrupt:
        # Arrêter l'application en cas d'interruption
        app.stop()
    except Exception as e:
        # Afficher les erreurs
        print(f"Erreur: {str(e)}")
        app.stop()
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 