import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from config.settings import COLOR_PALETTE

# Vue pour l'affichage des tables de la base de données
class TablesView:
    # Initialise la vue des tables
    def __init__(self, parent, museoFonts, onTableSelect, onRefreshTables):
        """   
        Args:
            parent: Le widget parent
            museoFonts: Dictionnaire des polices Museo
            onTableSelect: Fonction à appeler lorsqu'une table est sélectionnée
            onRefreshTables: Fonction à appeler pour rafraîchir la liste des tables
        """
        self.parent = parent
        self.museoFonts = museoFonts
        self.onTableSelect = onTableSelect
        self.onRefreshTables = onRefreshTables
        
        # Variables pour le tableau
        self.tableInitialized = False
        self.currentTableName = None
        self.currentColumns = []
        self.treeView = None
        self.mainFrame = None
        
        # Créer le contenu de l'onglet Tables
        self.createTablesContent()
    
    # Crée le contenu de l'onglet Tables
    def createTablesContent(self):
        # Section principale
        mainSection = ctk.CTkFrame(self.parent, fg_color="transparent")
        mainSection.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        mainSection.columnconfigure(0, weight=1)
        mainSection.columnconfigure(1, weight=3)
        mainSection.rowconfigure(0, weight=1)
        
        # Panneau de gauche (liste des tables)
        self.leftPanel = ctk.CTkFrame(mainSection, 
            fg_color=COLOR_PALETTE['bg_card'], 
            corner_radius=8, 
            border_width=2, 
            border_color=COLOR_PALETTE['border'],
            height=600)
        self.leftPanel.grid(row=0, column=0, sticky="n", padx=(0, 10), pady=0)
        self.leftPanel.grid_propagate(False)  # Empêche le redimensionnement automatique
        self.leftPanel.columnconfigure(0, weight=1)
        self.leftPanel.rowconfigure(1, weight=1)
        
        # Titre du panneau de gauche
        leftTitleFrame = ctk.CTkFrame(self.leftPanel, fg_color="transparent", height=40)
        leftTitleFrame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
        leftTitleFrame.columnconfigure(0, weight=1)
        
        leftTitle = ctk.CTkLabel(leftTitleFrame, text="Tables disponibles", 
                                font=ctk.CTkFont(family=self.museoFonts.get('bold', None), size=16),
                                text_color=COLOR_PALETTE['text_dark'])
        leftTitle.grid(row=0, column=0, sticky="w", padx=0, pady=0)
        
        # Cadre pour les tables
        tablesFrame = ctk.CTkFrame(self.leftPanel, fg_color="transparent")
        tablesFrame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        tablesFrame.columnconfigure(0, weight=1)
        tablesFrame.rowconfigure(0, weight=1)
        
        # Liste des tables
        self.tablesListbox = tk.Listbox(tablesFrame, 
                                       font=("Segoe UI", 12),
                                       bg=COLOR_PALETTE['bg_light'],
                                       fg=COLOR_PALETTE['text_dark'],
                                       selectbackground=COLOR_PALETTE['primary'],
                                       selectforeground=COLOR_PALETTE['text_light'],
                                       borderwidth=1,
                                       relief="solid",
                                       highlightthickness=0)
        self.tablesListbox.grid(row=0, column=0, sticky="nsew")
        self.tablesListbox.bind('<<ListboxSelect>>', self._onTableSelect)
        
        # Scrollbar pour la liste
        tablesScrollbar = tk.Scrollbar(tablesFrame, command=self.tablesListbox.yview)
        tablesScrollbar.grid(row=0, column=1, sticky="ns")
        self.tablesListbox.config(yscrollcommand=tablesScrollbar.set)
        
        # Bouton de rafraîchissement des tables
        refreshButtonFrame = ctk.CTkFrame(self.leftPanel, fg_color="transparent")
        refreshButtonFrame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        refreshTablesButton = ctk.CTkButton(refreshButtonFrame, text="Rafraîchir les tables", 
                                           command=self.onRefreshTables,
                                           font=ctk.CTkFont(family=self.museoFonts.get('bold', None), size=13),
                                           fg_color=COLOR_PALETTE['primary'],
                                           text_color=COLOR_PALETTE['text_light'],
                                           hover_color=COLOR_PALETTE['accent'],
                                           corner_radius=4,
                                           height=30)
        refreshTablesButton.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        
        # Panneau de droite (données de la table)
        self.rightPanel = ctk.CTkFrame(mainSection, fg_color=COLOR_PALETTE['bg_card'], corner_radius=8, border_width=1, border_color=COLOR_PALETTE['border'])
        self.rightPanel.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.rightPanel.columnconfigure(0, weight=1)
        self.rightPanel.rowconfigure(1, weight=1)
        
        # Titre du panneau de droite avec bouton de rafraîchissement
        rightTitleFrame = ctk.CTkFrame(self.rightPanel, fg_color="transparent", height=40)
        rightTitleFrame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 0))
        rightTitleFrame.columnconfigure(0, weight=1)
        rightTitleFrame.columnconfigure(1, weight=0)
        
        self.rightTitle = ctk.CTkLabel(rightTitleFrame, text="Données de la table", 
                                     font=ctk.CTkFont(family=self.museoFonts.get('bold', None), size=16),
                                     text_color=COLOR_PALETTE['text_dark'])
        self.rightTitle.grid(row=0, column=0, sticky="w", padx=0, pady=0)
        
        # Bouton de rafraîchissement des données
        self.refreshDataButton = ctk.CTkButton(rightTitleFrame, text="↻ Rafraîchir", 
                                              command=self._refreshCurrentTable,
                                              font=ctk.CTkFont(family=self.museoFonts.get('bold', None), size=13),
                                              fg_color=COLOR_PALETTE['bg_light'],
                                              text_color=COLOR_PALETTE['primary'],
                                              hover_color=COLOR_PALETTE['border'],
                                              corner_radius=4,
                                              width=100,
                                              height=30)
        self.refreshDataButton.grid(row=0, column=1, sticky="e", padx=0, pady=0)
        
        # Statut du rafraîchissement automatique
        self.autoRefreshStatus = ctk.CTkLabel(rightTitleFrame, 
                                             text="Auto-refresh: Inactif", 
                                             font=ctk.CTkFont(family=self.museoFonts.get('regular', None), size=12),
                                             text_color=COLOR_PALETTE['text_muted'])
        self.autoRefreshStatus.grid(row=0, column=2, sticky="e", padx=(10, 0), pady=0)
        
        # Cadre pour les données
        dataFrame = ctk.CTkFrame(self.rightPanel, fg_color="transparent")
        dataFrame.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        dataFrame.columnconfigure(0, weight=1)
        dataFrame.rowconfigure(0, weight=1)
        
        # Zone de texte pour les données
        self.tableData = tk.Text(dataFrame, 
                                font=("Consolas", 11),
                                bg=COLOR_PALETTE['bg_light'],
                                fg=COLOR_PALETTE['text_dark'],
                                borderwidth=1,
                                relief="solid",
                                wrap="none",
                                highlightthickness=0)
        self.tableData.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbars pour les données
        dataScrollbarY = tk.Scrollbar(dataFrame, command=self.tableData.yview)
        dataScrollbarY.grid(row=0, column=1, sticky="ns")
        
        dataScrollbarX = tk.Scrollbar(dataFrame, command=self.tableData.xview, orient="horizontal")
        dataScrollbarX.grid(row=1, column=0, sticky="ew")
        
        self.tableData.config(yscrollcommand=dataScrollbarY.set, xscrollcommand=dataScrollbarX.set)
        
        # Initialisation avec un message d'aide
        self.tableData.insert(tk.END, "Sélectionnez une table dans la liste de gauche pour afficher ses données.")
    
    # Gère l'événement de sélection d'une table.
    def _onTableSelect(self, event=None):
        """
        Args:
            event: L'événement de sélection d'une table
        """
        selection = self.tablesListbox.curselection()
        if selection:
            table_name = self.tablesListbox.get(selection[0])
            self.onTableSelect(table_name)
    
    # Rafraîchit les données de la table actuellement sélectionnée.
    def _refreshCurrentTable(self):
        """
        Args:
            event: L'événement de rafraîchissement des données de la table
        """
        if self.currentTableName:
            self.onTableSelect(self.currentTableName)
    
    # Met à jour la liste des tables
    def updateTablesList(self, tables):
        """
        Args:
            tables: Liste des noms de tables
        """
        self.tablesListbox.delete(0, tk.END)
        for table in tables:
            self.tablesListbox.insert(tk.END, table)

    # Met à jour les données de la table
    def updateTableData(self, tableName, columns, rows):
        """ 
        Args:
            tableName: Nom de la table
            columns: Liste des noms de colonnes
            rows: Liste des lignes de données
        """
        self.currentTableName = tableName
        self.currentColumns = columns
        
        # Mettre à jour le titre
        self.rightTitle.configure(text=f"Données de la table: {tableName}")
        
        # Créer la vue du tableau
        self.createTableView(tableName, columns, rows)

    # Crée une vue de tableau pour afficher les données
    def createTableView(self, tableName, columns, rows):
        """
        Args:
            tableName: Nom de la table
            columns: Liste des noms de colonnes
            rows: Liste des lignes de données
        """
        # Effacer le contenu précédent
        self.tableData.delete(1.0, tk.END)
        
        if not columns or not rows:
            self.tableData.insert(tk.END, "Aucune donnée disponible pour cette table.")
            return
        
        # Supprimer le widget TreeView existant s'il existe
        if self.treeView:
            self.treeView.destroy()
        
        if self.mainFrame:
            self.mainFrame.destroy()
        
        # Créer un cadre pour le TreeView
        self.mainFrame = ctk.CTkFrame(self.rightPanel, fg_color="transparent")
        self.mainFrame.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        self.mainFrame.columnconfigure(0, weight=1)
        self.mainFrame.rowconfigure(0, weight=1)
        
        # Créer un cadre pour le TreeView avec scrollbars
        treeFrame = ctk.CTkFrame(self.mainFrame, fg_color="transparent")
        treeFrame.grid(row=0, column=0, sticky="nsew")
        treeFrame.columnconfigure(0, weight=1)
        treeFrame.rowconfigure(0, weight=1)
        
        # Créer le TreeView
        self.treeView = ttk.Treeview(treeFrame, columns=columns, show="headings")
        
        # Configurer les colonnes
        for col in columns:
            self.treeView.heading(col, text=col)
            self.treeView.column(col, width=100)  # Largeur par défaut
        
        # Ajouter les données
        for row in rows:
            self.treeView.insert("", "end", values=row)
        
        # Ajouter les scrollbars
        vsb = ttk.Scrollbar(treeFrame, orient="vertical", command=self.treeView.yview)
        hsb = ttk.Scrollbar(treeFrame, orient="horizontal", command=self.treeView.xview)
        self.treeView.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Placer les widgets
        self.treeView.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Configurer le style du TreeView
        style = ttk.Style()
        style.configure("Treeview", 
                        background=COLOR_PALETTE['bg_light'],
                        foreground=COLOR_PALETTE['text_dark'],
                        rowheight=25,
                        fieldbackground=COLOR_PALETTE['bg_light'])
        style.configure("Treeview.Heading", 
                        background=COLOR_PALETTE['primary'],
                        foreground=COLOR_PALETTE['text_dark'],
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview", 
                 background=[("selected", COLOR_PALETTE['accent'])],
                 foreground=[("selected", COLOR_PALETTE['text_light'])])
        
        # Configurer le redimensionnement du cadre
        self.mainFrame.bind("<Configure>", self._configureFrame)
        
        self.tableInitialized = True
    
    # Ajuste la taille des colonnes du TreeView lors du redimensionnement.
    def _configureFrame(self, event=None):
        if self.treeView and self.currentColumns:
            # Calculer la largeur disponible
            availableWidth = event.width - 20  # Tenir compte de la scrollbar
            
            # Calculer la largeur de chaque colonne
            colWidth = availableWidth // len(self.currentColumns)
            
            # Définir la largeur des colonnes
            for col in self.currentColumns:
                self.treeView.column(col, width=colWidth)

    
    # Met à jour l'affichage du statut de rafraîchissement automatique.
    def updateAutoRefreshStatus(self, isActive=False, interval=0):
        """ 
        Args:
            isActive: Indique si le rafraîchissement automatique est actif
            interval: Intervalle de rafraîchissement en secondes
        """
        if isActive:
            self.autoRefreshStatus.configure(
                text=f"Auto-refresh: Actif ({interval}s)",
                text_color=COLOR_PALETTE['primary']
            )
        else:
            self.autoRefreshStatus.configure(
                text="Auto-refresh: Inactif",
                text_color=COLOR_PALETTE['text_muted']
            )
    # Affiche un message dans la zone de données.
    def showMessage(self, message):
        """
        Args:
            message: Le message à afficher
        """
        self.tableData.delete(1.0, tk.END)
        self.tableData.insert(tk.END, message) 