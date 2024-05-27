from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QPushButton, QStatusBar, QAction, 
                             QWidget, QInputDialog, QMessageBox, QLabel, QMenu)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from demineur import FenetreGame
import pygame

# Classe pour initialiser le menu principal du jeu
class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ESMEXPLORER')

        self.setStyleSheet("background-color: black;")
        
        self.fenetre_game = None

        # Initialisation du mixer Pygame pour la musique du menu
        pygame.mixer.init()
        self.music_file = "../content/music/menu_music.mp3"
        self.play_music()
        self.isMute = False

        # Initialisation du widget principal et de sa mise en page
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout(self.main_widget)

        # Chargement du logo du jeu et ajout au layout
        logo_label = QLabel(self)
        pixmap = QPixmap('../content/chart/esmeexplorer_logo.png')
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Style des boutons de difficulté
        button_style = """
            QPushButton {
                background-color: #008000;
                color: white;
                border: 2px solid black;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #006400;
            }
        """

        # Bouton pour démarrer une partie facile
        facile_button = QPushButton('Planétoïde (8x8, 10 aliens)')
        facile_button.clicked.connect(self.play_facile)
        facile_button.setStyleSheet(button_style)
        layout.addWidget(facile_button)

        # Bouton pour démarrer une partie moyenne
        moyen_button = QPushButton('Planète (16x16, 40 aliens)')
        moyen_button.clicked.connect(self.play_moyen)
        moyen_button.setStyleSheet(button_style)
        layout.addWidget(moyen_button)

        # Bouton pour démarrer une partie difficile
        difficile_button = QPushButton('Planète Mère (24x24, 99 aliens)')
        difficile_button.clicked.connect(self.play_hard)
        difficile_button.setStyleSheet(button_style)
        layout.addWidget(difficile_button)

        # Configuration du widget principal
        self.main_widget.setLayout(layout)
        self.setStatusBar(QStatusBar(self))

        # Initialisation de la barre de menu
        menuBar = self.menuBar()

        # Style de la barre de menu
        menu_style = """
            QMenuBar {
                background-color: #004d00;
                color: white;
                padding: 5px;
            }
            QMenuBar::item {
                background-color: transparent;
            }
            QMenuBar::item:selected {
                background-color: #006400;
            }
        """

        # Style des éléments de menu
        menu_item_style = """
            QMenu {
                background-color: #008000;
                color: white;
            }
            QMenu::item {
                background-color: #008000;
                color: white;
                padding: 10px 20px;
            }
            QMenu::item:selected {
                background-color: #006400;
            }
        """

        menuBar.setStyleSheet(menu_style)
        fichier_fileMenu = menuBar.addMenu("&Fichier")
        fichier_fileMenu.setStyleSheet(menu_item_style)

        # Actions pour sauvegarder et charger la partie
        self.button_charger = QAction('Charger', self)
        self.button_sauvegarder = QAction('Sauvegarder', self)
        fichier_fileMenu.addAction(self.button_charger)
        fichier_fileMenu.addAction(self.button_sauvegarder)
        self.button_charger.triggered.connect(self.charger_partie)
        self.button_sauvegarder.triggered.connect(self.sauvegarder_partie)

        # Menu pour afficher le classement
        classement_fileMenu = menuBar.addMenu("&Classement")
        classement_fileMenu.setStyleSheet(menu_item_style)
        self.button_score = QAction('Meilleurs explorateurs', self)
        self.button_score.setMenu(QMenu(self))
        self.button_score.menu().setStyleSheet(menu_item_style)  

        # Actions pour afficher le classement selon les différents niveaux
        planetoide = QAction('Planètoïde', self)
        planete = QAction('Planète Moyenne', self)
        planete_mere = QAction('Planète Mère', self)
        self.button_score.menu().addAction(planetoide)
        self.button_score.menu().addAction(planete)
        self.button_score.menu().addAction(planete_mere)
        planetoide.triggered.connect(lambda: self.score("Planètoïde"))
        planete.triggered.connect(lambda: self.score("Planète Moyenne"))
        planete_mere.triggered.connect(lambda: self.score("Planète Mère"))
        classement_fileMenu.addAction(self.button_score)

        # Menu pour les options de configuration
        edition_fileMenu = menuBar.addMenu("&Edition")
        edition_fileMenu.setStyleSheet(menu_item_style)
        self.button_identifiant = QAction('Identifiant', self)
        self.button_identifiant.triggered.connect(self.changer_identifiant)
        self.button_propos = QAction('À propos', self)
        self.button_propos.triggered.connect(self.show_about)
        edition_fileMenu.addAction(self.button_identifiant)
        edition_fileMenu.addAction(self.button_propos)

        # Menu pour la gestion du son
        son_fileMenu = menuBar.addMenu("&Son")
        son_fileMenu.setStyleSheet(menu_item_style)
        self.button_volume = QAction('Volume', self)
        self.button_volume.triggered.connect(self.changer_identifiant)
        self.button_mute = QAction('Activer/Désactiver le son', self)
        self.button_mute.triggered.connect(self.mute)
        son_fileMenu.addAction(self.button_mute)

    # Méthode pour changer l'identifiant du joueur
    def changer_identifiant(self):
        dialog = QInputDialog(self)
        dialog.setStyleSheet("QInputDialog { background-color: black; color: green; }"
                            "QLineEdit { background-color: black; color: green; }"
                            "QLabel { color: green }")
        dialog.setInputMode(QInputDialog.TextInput)
        dialog.setWindowTitle("Changer identifiant")
        dialog.setLabelText("Entrez votre identifiant:")
        ok = dialog.exec_()
        if ok:
            text = dialog.textValue()
            self.write("../content/donnee/id.txt", text)

    # Méthode pour afficher la boîte de dialogue "À propos"
    def show_about(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("À propos")
        msg_box.setText(self.read("../content/donnee/readme.txt"))
        msg_box.setStyleSheet("background-color: black; color: green")
        msg_box.exec_()

    # Méthode pour afficher le classement des meilleurs scores pour une planète donnée
    def score(self, planete):
        with open("../content/donnee/score.txt", "r", encoding="UTF-8") as score_file:
            scores = score_file.readlines()
        scores_planete = [score for score in scores if planete in score]
        sorted_scores = sorted(scores_planete, key=lambda x: int(x.split(":")[-2].strip()) * 60 + int(x.split(":")[-1].strip()))
        top_10 = sorted_scores[:10]
        score_text = f"Meilleurs explorateurs:\n"
        for score in top_10:
            score_text += score
        msg_box = QMessageBox()
        msg_box.setWindowTitle(f"Top 10 explorateurs sur {planete}")
        msg_box.setText(score_text.replace(planete,''))
        msg_box.setStyleSheet("background-color: black; color: green")
        msg_box.exec_()

    # Méthode pour lire un fichier et en retourner le contenu
    def read(self, text):
        with open(text, 'r', encoding='UTF-8') as file:
            content = file.read()
        return content
    
    # Méthode pour écrire du contenu dans un fichier
    def write(self, text, content):
        with open(text, 'w', encoding='UTF-8') as file:
            file.write(content)

    # Méthode pour démarrer une partie facile
    def play_facile(self):
        self.play(8, 8, 10, 'Planètoïde')

    # Méthode pour démarrer une partie moyenne
    def play_moyen(self):
        self.play(16, 16, 40, 'Planète Moyenne')

    # Méthode pour démarrer une partie difficile
    def play_hard(self):
        self.play(24, 24, 99, 'Planète Mère')

    # Méthode pour démarrer une partie avec des paramètres donnés
    def play(self, lignes, colonnes, mines, planete):
        self.fenetre_game = FenetreGame(lignes, colonnes, mines, self.read("../content/donnee/id.txt"), self.isMute, planete)
        self.fenetre_game.show()

    # Méthode pour jouer de la musique
    def play_music(self):
        pygame.mixer.music.load(self.music_file)
        pygame.mixer.music.play(-1)

    # Méthode pour activer/désactiver le son
    def mute(self):
        self.isMute = not self.isMute
        if self.isMute:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    # Méthode pour sauvegarder la partie actuelle
    def sauvegarder_partie(self):
        if self.fenetre_game is not None:
            self.fenetre_game.sauvegarder()

    # Méthode pour charger une partie sauvegardée
    def charger_partie(self):
        if self.fenetre_game is None:
            self.fenetre_game = FenetreGame(8, 8, 10, self.read("../content/donnee/id.txt"), self.isMute, 'Planètoïde')
            self.fenetre_game.show()
        self.fenetre_game.charger()
