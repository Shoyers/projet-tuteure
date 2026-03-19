import customtkinter as ctk
from config.settings import COLOR_PALETTE

try:
    import tkintermapview
    MAP_AVAILABLE = True
except ImportError:
    MAP_AVAILABLE = False
    print("Module tkintermapview non disponible. La carte GPS ne sera pas affichée.")
    print("Installez-le avec: pip install tkintermapview")

# Composant carte GPS interactive
class GPSMap:
    def __init__(self, parent, width=400, height=300):
        """
        Initialise le composant de carte GPS.
        
        Args:
            parent: Widget parent
            width: Largeur de la carte
            height: Hauteur de la carte
        """
        self.parent = parent
        self.width = width
        self.height = height
        self.currentMarker = None
        self.mapWidget = None
        
        # Dictionnaire pour stocker plusieurs marqueurs
        self.markers = {}
        
        # Position par défaut (Laon, France - près de votre drone)
        self.defaultLat = 49.837038
        self.defaultLon = 3.300547
        
        # Créer le conteneur de la carte
        self.createMapContainer()
    
    def createMapContainer(self):
        """Crée le conteneur de la carte"""
        # Frame conteneur
        self.mapFrame = ctk.CTkFrame(
            self.parent,
            fg_color=COLOR_PALETTE['bg_card'],
            corner_radius=8,
            border_width=1,
            border_color=COLOR_PALETTE['border']
        )
        
        if not MAP_AVAILABLE:
            # Afficher un message si la bibliothèque n'est pas disponible
            errorLabel = ctk.CTkLabel(
                self.mapFrame,
                text="📍 Carte GPS non disponible\n\nInstallez tkintermapview:\npip install tkintermapview",
                font=ctk.CTkFont(size=14),
                text_color=COLOR_PALETTE['text_muted'],
                justify="center"
            )
            errorLabel.pack(expand=True, fill="both", padx=20, pady=20)
            return
        
        # Créer la carte
        try:
            self.mapWidget = tkintermapview.TkinterMapView(
                self.mapFrame,
                width=self.width,
                height=self.height,
                corner_radius=8
            )
            self.mapWidget.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Définir la position par défaut
            self.mapWidget.set_position(self.defaultLat, self.defaultLon)
            self.mapWidget.set_zoom(14)
            
        except Exception as e:
            print(f"Erreur lors de la création de la carte: {e}")
            errorLabel = ctk.CTkLabel(
                self.mapFrame,
                text=f"Erreur carte GPS:\n{str(e)}",
                font=ctk.CTkFont(size=12),
                text_color=COLOR_PALETTE['danger']
            )
            errorLabel.pack(expand=True, fill="both", padx=20, pady=20)
    
    def updatePosition(self, latitude, longitude, altitude=None):
        """
        Met à jour la position principale sur la carte.
        
        Args:
            latitude: Latitude GPS
            longitude: Longitude GPS
            altitude: Altitude (optionnel)
        """
        self.addMarker("main", latitude, longitude, altitude, "Position actuelle")
        self.mapWidget.set_position(latitude, longitude)
    
    def addMarker(self, marker_id, latitude, longitude, altitude=None, text="Marqueur", icon=None):
        """
        Ajoute ou met à jour un marqueur sur la carte.
        
        Args:
            marker_id: Identifiant unique du marqueur
            latitude: Latitude GPS
            longitude: Longitude GPS
            altitude: Altitude (optionnel)
            text: Texte du marqueur
            icon: Icône personnalisée (optionnel)
        """
        if not MAP_AVAILABLE or not self.mapWidget:
            return
        
        try:
            # Supprimer l'ancien marqueur s'il existe
            if marker_id in self.markers:
                self.markers[marker_id].delete()
            
            # Créer le texte du marqueur
            markerText = f"{text}\nLat: {latitude:.6f}\nLon: {longitude:.6f}"
            if altitude is not None:
                markerText += f"\nAlt: {altitude:.2f}m"
            
            # Ajouter le nouveau marqueur
            marker = self.mapWidget.set_marker(
                latitude,
                longitude,
                text=markerText,
                icon=icon
            )
            
            # Stocker le marqueur
            self.markers[marker_id] = marker
            
        except Exception as e:
            print(f"Erreur lors de l'ajout du marqueur {marker_id}: {e}")
    
    def removeMarker(self, marker_id):
        """
        Supprime un marqueur de la carte.
        
        Args:
            marker_id: Identifiant du marqueur à supprimer
        """
        if marker_id in self.markers:
            try:
                self.markers[marker_id].delete()
                del self.markers[marker_id]
            except Exception as e:
                print(f"Erreur lors de la suppression du marqueur {marker_id}: {e}")
    
    def clearMarkers(self):
        """Supprime tous les marqueurs de la carte."""
        for marker_id in list(self.markers.keys()):
            self.removeMarker(marker_id)
    
    def setZoom(self, zoom):
        """
        Définit le niveau de zoom.
        
        Args:
            zoom: Niveau de zoom (0-19)
        """
        if self.mapWidget:
            try:
                self.mapWidget.set_zoom(zoom)
            except Exception as e:
                print(f"Erreur lors du changement de zoom: {e}")
    
    def setTileServer(self, server="osm"):
        """
        Change le serveur de tuiles.
        
        Args:
            server: Type de carte ("osm", "google normal", "google satellite")
        """
        if not self.mapWidget:
            return
        
        try:
            if server == "osm":
                self.mapWidget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
            elif server == "google normal":
                self.mapWidget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
            elif server == "google satellite":
                self.mapWidget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        except Exception as e:
            print(f"Erreur lors du changement de serveur de tuiles: {e}")
    
    def getFrame(self):
        """
        Retourne le frame conteneur de la carte.
        
        Returns:
            Frame CTk contenant la carte
        """
        return self.mapFrame
    
    def isAvailable(self):
        """
        Vérifie si la carte est disponible.
        
        Returns:
            True si la carte est disponible, False sinon
        """
        return MAP_AVAILABLE and self.mapWidget is not None

