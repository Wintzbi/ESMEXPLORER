# ESMEXPLORER

## Description

ESMEXPLORER is a futuristic minesweeper game where the player must uncover tiles without encountering aliens. The game offers three difficulty levels: Planetoid, Medium Planet, and Mother Planet.

## Prerequisites

To run this project using Python scripts, you will need the following libraries:

- pygame
- PyQt5

You can install these libraries with pip:
```bash
pip install pygame pyqt5
```


## Project Structure

The project is structured as follows:

```bash
project/
│
├── content/
│ ├── chart/
│ │ ├── alien.png
│ │ ├── scanner.png
│ │ ├── esmeexplorer_logo.png
│ │
│ ├── donnee/
│ │ ├── id.txt
│ │ ├── score.txt
│ │ ├── partie_sauvegardee.json
│ │ ├── readme.txt
│ │
│ └── music/
│ ├── menu_music.mp3
│ ├── track1.mp3
│ ├── track2.mp3
│ ├── game_over.mp3
│ ├── victory_music.mp3
│
├── game/
│ ├── menu.py
│ ├── demineur.py
│ ├── main.py
│
└── README.txt
```


## Running the Project


### Running Locally with Python

To run the project locally with Python scripts, execute the `main.py` file:

```bash
python game/main.py
```
## Usage

Start the game and select the difficulty level to begin playing. Use the left click to uncover a tile and the right click to place a flag.

## Saving and Loading Games

You can save your progress using the "Sauvegarder" option in the "Fichier" menu. To load a saved game, use the "Charger" option in the same menu.

## About

For more information about the game, check the "A propos" option in the "Edition" menu.
