# projet Robot Ricochet
Projet de programmation du jeu de plateau "Robot Ricochet" dans sa version à un seul joueur.

# Exécution 
- Clonage à partir du lien de github:
[https://github.com/21918142/Projet_Ricochet.git]

# Description du jeu
Le jeu se déroule sur une grille fermée de 16 * 16 cases avec 4 robots de couleurs différentes : bleu, vert, jaune, rouge; un ensemble d'obstacles : murs; et une cible en forme de carré dans une case de la grille qui doit être atteinte par le robot de la même couleur afin de résoudre le jeu.

# Règles globales
- Le joueur ne peut déplacer les robots qu’en ligne droite, horizontale ou verticale et ce dans quatres directions : droite, gauche, haut et bas.
- Cela compte pour un déplacement de robot, indépendamment du nombre de cases parcourues.
- Le joueur ne peut déplacer qu'un seul robot à la fois.
- Le joueur doit cliquer sur le robot qu'il souhaite deplacer
- Les robots ne s’arrêtent que quand ils rencontrent un obstacle qui est soit un mur soit un autre robot.


# Interface graphique
Pour l’interface graphique, les principales caractéristiques dans notre programme sont:
- Les quatre robots représentés par des cercles de couleur rouge, jaune, vert et bleu.
- Les cibles sont représentées par quatres carrés de couleurs différent elles correspondent à l'objectif que le robot de la meme couleur doit atteindre.
- Les quatre cases du milieu sont entourées de murs, et non accessibles par les robots; par ailleurs, un clic sur une de ces cases redémarre la partie au début.
- Quand on clique sur un robot, on peut ensuite le déplacer avec les flèches du clavier.
- Un compteur affiche le nombre de déplacements effectués.
- Quand la cible est atteinte par le robot de la bonne couleur, un message affiche que le jeu est résolu et indique le score (le nombre de déplacements de robots).
- Pour revenir en arrière:
Il vous est possible de revenir en arrière grâce au bouton Undo
- Nouvelle partie:
Afin de redémarrer une partie, il suffit de cliquer sur le carré noir du milieu
- Sauvegarder une partie:
Il vous est possible de sauvergarder une partie en cours en appuyant directement sur le bouton sauvegarder sur l'interface graphique.
- Charger une partie:
Après avoir sauvegardé une partie, vous êtes en mesure de la récupérer et de la continuer grâce ce bouton





# Utilisation du clavier
→ : Right

← : Left

↑  : Up

↓  : Down

# Fonctionnalités avancées
En plus de la programmation du jeu, voici les fonctionnalités avancées que possède notre version du programme:
- La possibilité de sauvegarder une partie en cours, et la recharger ensuite.
- La possibilité de sauvegarder le score d’une partie (le nombre de déplacements de robots), et pouvoir afficher le meilleur score pour chaque robot.
- La possibilité de revenir en arrière en annulant les derniers déplacements du robot.

# But du jeu
- Atteindre la cible de la couleur correspondante à celle du robot.
- Un objectif secondaire du jeu est de le résoudre en faisant le moins de déplacements possible.


