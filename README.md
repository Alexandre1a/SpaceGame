# Space Game

SpaceGame est un jeu dévelopé en Python avec Pygame.

## Sommaire
1 **[Installation](#-Installation)**  
2 **[Lancement](-#Lancement)**  
3 **[Credits](-#about)**  


## Features
    - Une génération procédurale de planètes  
    - Un système de quêtes, basé sur les planètes générées  
    - Un système de sauvegarde  
    - Et de nombreuses autres fonctionalitées...  

## Installation
Pour lancer le jeu, il suffit de:
    - Clonner cette source git avec:
```
git clone https://git.alexdelcamp.fr/SpaceGame
```
et de renter dans le dossier avec
```
cd SpaceGame
```
ou équivalent

### NixOS
Nous proposons une flake nix, pour l'utiliser
```
nix develop
```
ou avec direnv (l'`.envrc` est fourni)
```
direnv allow
```

### Legacy OSs
Pour les autres systèmes type GNU/Linux, OSX ou encore Windows, il suffit d'installer python et pygame grâce au `requirements.txt` via :  
```
pip install -r requirements.txt
```

## Lancement

Pour lancer le jeu, il suffit de lancer un symple `python main.py` ou `python3 main.py` selon les systèmes.  

Ce jeu à fut testé sur NixOS, macOS 15.7 (Sequoia) et Windows 11.  
Pour lancer une nouvelle partie, séléctionner votre vaisseau dans la "Sélection Vaisseau".  
Puis cliquez sur `jouer` et séléctionnez `nouvelle partie`.


## Comment jouer
### Contrôles
Les contrôles ne sont modifiables qu'en modifiant le fichier `entities/ship.py` dans la classe `KeyboardController`

Par défaut nous avons: 
  - `Z` pour accélérer
  - `S` pour ralentir
  - `Q` pour pivoter à gauche
  - `D` pour pivoter à droite
  - `E` pour ouvrir l'overlay d'une planète
  - `P` pour ouvrir le menu de pause

### Interface
Il y a une minicarte à disposition, elle régit au niveau de zoom.  
Une flèche indiquant où se trouve la destination de la quête traquée apparait quand on accepte un quête.


### Objectif
Votre objectif est d'accomplir toutes les quêtes disponibles, sachant qu'il y a une quête/planète...
