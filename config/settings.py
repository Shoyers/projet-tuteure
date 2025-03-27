from urllib.parse import urlparse;


# Lecture de l'URL de connexion depuis le fichier .env
#with open('.env', 'r') as f:
#    for line in f:
#        if line.startswith('SERVER_MYSQL_URL='):
#            db_url = line.split('=', 1)[1].strip();
#            break;

# Parse l'URL de connexion MySQL
#parsed = urlparse(db_url);
#DB_CONFIG = {
#    'host': parsed.hostname,
#    'user': parsed.username,
#    'password': parsed.password,
#    'database': parsed.path[1:]  # Enlever le premier '/'
#};

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'serv-projet'
};


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
    'temperature': 20.0,
    'pressure': 1000,
    'humidity': 50
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
    'bg_card': "#FFFFFF"       # Blanc pour les cartes
}; 