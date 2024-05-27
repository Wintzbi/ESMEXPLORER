import sys
from PyQt5.QtWidgets import QApplication
from menu import Menu

# Lance le menu et donc le jeu en général
# Se référer à la vidéo ou le README en cas de soucis de compréhension
def main():
    app = QApplication(sys.argv)
    menu = Menu()
    menu.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()