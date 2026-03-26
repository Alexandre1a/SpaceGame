# Space Game
[img/logo.png]

Ce projet est un jeu en Python, développé avec Pygame.

Dedant, nous pouvons intéragir avec les planètes, qui donnent des quêtes (livraison d'un point A à un point B).
Ces quêtes sont générées procéduralement, grâce aux planètes (elles-mêmes générées procéduralement).
De plus, le jeu possède un "radar", une flèche nous indiquant la destination.
Et enfin, il y a à dispositon, une minimap, qui s'adapte au niveau du zoom du joueur

Dans le domaine plus technique, nous avons créé des systèmes modulaires, qui permettent d'ajouter du nouveau contenu assez facilement.
Par exemple, dans le main.py nous avons:
```python
self.availableShips = [
    Ship(
        "name",
        "brand",
        "sprite",
        accel,
        maxSpeed,
        drag,
        turnSpeed
    ),
    [...] autres vaisseaux
]
```

Qui permet d'ajouter des vaisseaux très simplement, de changer leurs statistiques de manière centralisée.
Cette liste est utilisée à travers tout le jeu (notament dans la séléction de vaisseaux).

Autre bloc modulaire important, le système de quêtes.
En effet, nous avons d'abord crée un objet `Quest` et un autre `DeliveryQuest` qui héritait de cet objet.
L'objet `Quest` nous permet, en ajoutant par exemple un autre archétype de quête, de le faire simplement, tout en ayant une cohérence avec le jeu


