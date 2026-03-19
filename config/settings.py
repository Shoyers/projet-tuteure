from urllib.parse import urlparse;
import logging;

# Configuration du logger pour settings
logger = logging.getLogger('Settings')



# VOIR DRIVE POUR LA SECRET KEY
DB_CONFIG = {
    'host': 'localhost',
    'user': 'client',
    'password': 'root',
    'database': 'serv-projet',
    'port': 3306,  # Port par défaut MySQL
    'connect_timeout': 10,  # Timeout de 10 secondes
    'raise_on_warnings': True
};

logger.info(f"Configuration DB chargée: {DB_CONFIG['user']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}");

# Paramètres de l'interface
UI_CONFIG = {
    'window_title': 'Tableau de bord des capteurs',
    'window_size': '900x700',  # Taille augmentée pour une meilleure lisibilité
    'update_interval': 500,    # ms
    'demo_interval': 2000,     # ms
    'appearance_mode': 'dark',  # Mode d'apparence (light ou dark)
    'color_theme': 'blue',      # Thème de couleur
    'padding': {
        'small': 5,
        'medium': 10,
        'large': 15
    },
    'fonts': {
        'title': ('Segoe UI', 12, 'bold'),
        'subtitle': ('Segoe UI', 11, 'bold'),
        'text': ('Segoe UI', 10),
        'value': ('Segoe UI', 10, 'bold'),
        'console': ('Consolas', 10)
    }
};

# Valeurs par défaut des capteurs
DEFAULT_SENSOR_VALUES = {
    'air_quality': 0,
    'distance': 0.0,
    'luminosity': 0,
    'temperature': 0.0,
    'pressure': 0,
    'humidity': 0
};

# Palettes de couleurs pour l'interface
COLOR_PALETTE = {
    'primary': "#0047AB",      # Bleu
    'secondary': "#FFFFFF",    # Blanc pour le fond
    'accent': "#0056b3",       # Bleu plus foncé pour les éléments actifs
    'success': "#28a745",      # Vert pour les succès
    'warning': "#ffc107",      # Jaune pour les avertissements
    'danger': "#dc3545",       # Rouge pour les erreurs
    'info': "#17a2b8",         # Bleu clair pour les informations
    'text_dark': "#212529",    # Texte foncé
    'text_light': "#FFFFFF",   # Texte clair
    'text_muted': "#6c757d",   # Texte grisé pour les informations secondaires
    'border': "#dee2e6",       # Bordures légères
    'bg_light': "#F8F9FA",     # Gris très clair pour le fond secondaire
    'bg_white': "#FFFFFF",     # Blanc pur pour les cartes et tableaux
    'bg_card': "#FFFFFF"       # Blanc pour les cartes
}; 