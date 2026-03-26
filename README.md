# Space Game

SpaceGame est un jeu dévelopé en Python avec Pygame.

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
ou avec direnv (l'.envrc est fourni)
```
direnv allow
```

### Legacy OSs
Pour les autres systèmes type GNU/Linux ou Windows, il suffit d'installer python et pygame.

Pour lancer le jeu, il suffit de lancer un symple `python main.py` ou `python3 main.py` selon les systèmes.


