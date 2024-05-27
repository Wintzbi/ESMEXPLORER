import random
import pygame
import json
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QMessageBox, QLabel
from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QIcon

# Classe pour initialiser les types de case
class MineButton(QPushButton):
    def __init__(self, x, y):
        super(MineButton, self).__init__()
        self.x = x
        self.y = y
        self.isMine = False
        self.isShow = False
        self.isFlag = False
        
        alien_icon_path = "../content/chart/alien.png"
        scanner_icon_path = "../content/chart/scanner.png"
        self.alien_icon = QIcon(alien_icon_path)
        self.scanner_icon = QIcon(scanner_icon_path)

    # Méthode permettant l'affichage de la case. S'il s'agit d'une mine, afficher la mine, sinon l'afficher en vert
    def show(self):
        if not self.isShow:
            self.isShow = True
            if self.isMine:
                self.setIcon(self.alien_icon)
                self.setIconSize(QSize(40, 40))
            else:
                self.setStyleSheet("background-color: #008000; color: white; border: 1px solid black;")
            self.setEnabled(False)
            self.setFlat(True)

    # Méthode permettant de placer un drapeau (dans notre cas scanner). Si isFlage = False on enlève le drapeau sinon on le place
    def flag(self):
        if not self.isShow:
            if self.isFlag:
                self.setIcon(QIcon())
                self.isFlag = False
                self.setStyleSheet("background-color: #333333")
            else:
                self.setIcon(self.scanner_icon)
                self.setIconSize(QSize(40, 40))
                self.isFlag = True
                self.setStyleSheet("background-color: #004000")

    # Méthode permettant de savoir quand la souris est pressée
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent().leftClick(self)
        elif event.button() == Qt.RightButton:
            self.parent().rightClick(self)
        super().mousePressEvent(event)            

# Initialisation de la fenètre de jeu du démineur
class FenetreGame(QWidget):
    def __init__(self, lignes, colonnes, mines, identifiant, muted = False, planete = 'Planétoïde'):
        super().__init__()
        self.lignes = lignes
        self.colonnes = colonnes
        self.mines = mines
        self.restMines = mines
        self.identifiant = identifiant
        self.muted = muted
        self.time_score = ''
        self.grid()
        self.firstClick = True
        self.planete = planete

        alien_icon_path = "../content/chart/alien.png"
        scanner_icon_path = "../content/chart/scanner.png"
        self.alien_icon = QIcon(alien_icon_path)
        self.scanner_icon = QIcon(scanner_icon_path)

        self.timerLabel = QLabel("Temps d'exploration : 00:00")
        self.timerLabel.setStyleSheet("color: green;")
        self.layout.addWidget(self.timerLabel, 0, 5, 1, self.colonnes)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTimer)
        self.tempsPasse = 0
        self.isTimer = False

        self.setStyleSheet("background-color: black")

        # On initialise le pygame.mixer pour pouvoir jouer des musiques durant la partie
        pygame.mixer.init()
        self.music_file = self.randomMusic()
        self.play_music()

        pygame.mixer.music.set_endevent(pygame.USEREVENT)

    # Méthode permettat d'initialiser une grille vide ainsi que l'affichage à l'écran
    def grid(self):
        self.setWindowTitle('ESMEXPLORER')
        self.layout = QGridLayout()
        self.buttons = {}
        self.playerLabel = QLabel(f"Joueur : {self.identifiant}")
        self.playerLabel.setStyleSheet("color: green;")
        self.layout.addWidget(self.playerLabel, 0, 0, 1, self.colonnes)

        default_color = "#333333"

        for ligne in range(self.lignes):
            for colonne in range(self.colonnes):
                button = MineButton(ligne, colonne)
                button.setFixedSize(QSize(50 - self.lignes, 50 - self.colonnes))
                button.setStyleSheet(f"background-color: {default_color};")
                self.layout.addWidget(button, ligne + 1, colonne)
                self.buttons[(ligne, colonne)] = button

        self.minesLabel = QLabel(f"Nombre d'aliens : {self.mines}")
        self.minesLabel.setStyleSheet("color: green;")
        self.layout.addWidget(self.minesLabel, self.lignes + 1, 0, 1, self.colonnes)

        if self.lignes <= 8:
            self.restMinesLabel = QLabel(f"Nombre d'aliens restants : {self.restMines}")
            self.restMinesLabel.setStyleSheet("color: green;")
            self.layout.addWidget(self.restMinesLabel, self.lignes + 1, 3, 1, self.colonnes)
        self.setLayout(self.layout)

        for (x, y), button in self.buttons.items():
            if button.isFlag:
                button.flag()


    # Méthode permettant de placer des bombes (aliens) aléatoirement dans la grille initialisée. On place les bombes après le premier clic du joueur
    def setMines(self, clickedButton):
        positions = [(x, y) for x in range(self.lignes) for y in range(self.colonnes)]
        clickX, clickY = clickedButton.x, clickedButton.y
        positions.remove((clickX, clickY))
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (clickX + i, clickY + j) in positions:
                    positions.remove((clickX + i, clickY + j))
        bombes_positions = random.sample(positions, self.mines)
        for position in bombes_positions:
            self.buttons[position].isMine = True
           
    # Méthode clic gauche permettant d'appliquer les actions du clic gauche
    def leftClick(self, button):
        if self.firstClick:
            self.setMines(button)
            self.firstClick = False
            self.showCase(button)
            self.startTimer()
        else:
            if button.isMine:
                self.gameOver()
            else:
                self.showCase(button)

    # Méthode clic droit ayant la même fonction que le clic gauche
    def rightClick(self, button):
        button.flag()
        if button.isFlag and button.isMine:
            self.restMines -= 1
        elif not button.isFlag and button.isMine:
            self.restMines += 1
        if self.lignes <= 8:
            self.restMinesLabel.setText(f"Nombre d'aliens restants : {self.restMines}")
        self.win()

    # Méthode permettant d'afficher la case. Cette méthode se bae autours d'une pile
    def showCase(self, button):
        pile = [button]
        while pile:
            button_test = pile.pop()
            button_test.show()
            button_test.setStyleSheet("background-color: #008000; color: white; border: 1px solid black;")
            if button_test.isMine:
                continue
            count = self.countMines(button_test)
            if count == 0:
                for voisin in self.getVoisin(button_test):
                    if not voisin.isShow and not voisin.isMine:
                        pile.append(voisin)
            else:
                button_test.setText(str(count))
        self.win()

    # Méthode permettant de compter le nombre de mine autours d'une case
    def countMines(self, button):
        count = 0
        for voisin in self.getVoisin(button):
            if voisin.isMine:
                count += 1
        return count

    # Méthode permettant d'obtenir des informations sur tous les voisins d'une case
    def getVoisin(self, button):
        liste_voisin = []
        for i in [-1, 0, 1]: 
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                x_voisin, y_voisin = button.x + i, button.y + j
                if 0 <= x_voisin < self.lignes and 0 <= y_voisin < self.colonnes:
                    liste_voisin.append(self.buttons[(x_voisin, y_voisin)])
        return liste_voisin
    
    # Méthode permettant de lancer la musique
    def play_music(self):
        if not self.muted:
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(loops=-1)

    # Méthode permettant de l'arrêter
    def stop_music(self):
        pygame.mixer.music.stop()

    # Méthode permettant de sélectionner une musique aléatoirement
    def randomMusic(self):
        track_number = random.randint(1, 1)
        return f"../content/music/track{track_number}.mp3"
    
    # Méthode event permettant de lancer une autre musique lorsque la fenêtre est fermée
    def closeEvent(self, event):
        self.music_file = "../content/music/menu_music.mp3"
        self.play_music()
        event.accept()

    # Méthode permettant de changer de musique une fois celle-ci terminée (elle ne semble pas fonctionner en revanche)
    def endMusicEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.music_file = self.randomMusic()
                self.play_music()

    # Méthode permettant de lancer le timer
    def startTimer(self):
        self.timer.start(1000)
        self.timerStarted = True

    # Méthode permettant d'arrêter le timer
    def stopTimer(self):
        self.timer.stop()

    # Méthode permettant d'arrêter le timer
    def updateTimer(self):
        self.tempsPasse += 1
        minutes = self.tempsPasse // 60
        seconds = self.tempsPasse % 60
        timer_text = f"Temps d'exploration: {minutes:02d}:{seconds:02d}"
        self.time_score = timer_text
        self.timerLabel.setText(timer_text)

    # Méthode permettant d'afficher la fin du jeu ainsi que de stopper la partie lorsque celle-ci est perdue
    def gameOver(self):
        for button in self.buttons.values():
            button.show()
        self.music_file = "../content/music/game_over.mp3"
        self.play_music()
        self.stopTimer()
        msg_box = QMessageBox()
        msg_box.setWindowTitle("ESMEXPLORER")
        msg_box.setText("Mission échouée, les aliens envahissent votre vaisseau!")
        msg_box.setStyleSheet("background-color: black; color: green")
        msg_box.exec_()
        self.close()

    # Méthode permettant de tester si la partie est gagnée ou non ainsi que de la terminer dans le cas échéant. On va également sauvegarder le score dans cette partie
    def win(self):
        if self.mines - self.restMines == self.mines:
            self.music_file = "../content/music/victory_music.mp3"
            self.play_music()
            self.stopTimer()
            
            player_name = self.identifiant
            score = self.time_score
            planete = self.planete
            with open("../content/donnee/score.txt", "a", encoding='UTF-8') as score_file:
                score_file.write(f"{planete}{player_name},{score}\n")
                
            msg_box = QMessageBox()
            msg_box.setWindowTitle("ESMEXPLORER")
            msg_box.setText("Mission réussie, les aliens ont été éliminés!")
            msg_box.setStyleSheet("background-color: black; color: green")
            msg_box.exec_()
            self.close()

    # Méthode permettant de sauvergarder la partie
    def sauvegarder_partie(self):
        data = {
            "identifiant": self.identifiant,
            "temps": self.tempsPasse,
            "restMines": self.restMines,
            "lignes": self.lignes,
            "colonnes": self.colonnes,
            "mines": self.mines,
            "firstClick": self.firstClick,
            "planete": self.planete,
            "isTimer": self.isTimer,
            "buttons_state": {(str(x) + ',' + str(y)): {"isShow": button.isShow,"isFlag": button.isFlag} for (x, y), button in self.buttons.items()}}
        with open("../content/donnee/partie_sauvegardee.json", "w") as file:
            json.dump(data, file)

    # Méthode permettant de charger la partie
    def charger_partie(self):
        with open("../content/donnee/partie_sauvegardee.json", "r") as file:
            data = json.load(file)

        pygame.mixer.init()
        self.music_file = self.randomMusic()
        self.play_music()

        self.identifiant = data["identifiant"]
        self.tempsPasse = data["temps"]
        self.restMines = data["restMines"]
        self.lignes = data["lignes"]
        self.colonnes = data["colonnes"]
        self.mines = data["mines"]
        self.firstClick = data["firstClick"]
        self.planete = data["planete"]
        self.isTimer = data["isTimer"]
        
        button_state = data["buttons_state"]
        for key, value in button_state.items():
            x, y = map(int, key.split(","))
            button = self.buttons[(x, y)]
            button.isShow = value["isShow"]
            button.isFlag = value["isFlag"]
            if button.isShow:
                button.show()
            if button.isFlag:
                button.flag()
                button.flag()
        self.show()