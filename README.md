# Gomoku avec intelligence artificielle

## Description

Ce projet est une implémentation du jeu **Gomoku** en Python avec une **interface graphique Pygame** et une **intelligence artificielle** basée sur les algorithmes **Minimax** et **Minimax avec élagage Alpha-Bêta**.

L’objectif principal du projet est de travailler sur :

- la représentation d’un plateau de jeu,
- l’évaluation heuristique d’une position,
- la génération et le tri de coups pertinents,
- l’optimisation d’une IA de jeu.

L’interface graphique est volontairement simple, car l’accent a été mis principalement sur **l’IA** et **ses optimisations**.

---

## Règles du jeu

Le Gomoku se joue sur une grille de **19x19**.

Deux joueurs placent chacun leur tour un jeton :

- **joueur 1** : noir
- **joueur 2** : blanc

Le premier joueur qui aligne **5 jetons consécutifs** horizontalement, verticalement ou en diagonale gagne la partie.

---

## Fonctionnalités

- Plateau de Gomoku en **19x19**
- Affichage graphique avec **Pygame**
- Gestion des tours
- Détection de victoire
- IA configurable avec :
  - poids d’attaque
  - poids de défense
- Algorithmes disponibles :
  - **Minimax**
  - **Minimax Alpha-Bêta**
- Heuristique d’évaluation des positions
- Réduction des coups explorés grâce à un filtrage local autour des pièces déjà posées
- Tri des coups pour améliorer les performances de l’algorithme Alpha-Bêta

---

## Structure du projet

```bash
.
├── evaluation.py
├── game.py
├── ia.py
├── main.py
├── minimax.py
├── minimax_alpha_beta.py
└── outil.py
```
main.py

Contient le programme principal :

initialise Pygame,
crée la fenêtre,
dessine le plateau,
lance la partie,
gère les clics du joueur humain,
fait jouer l’IA automatiquement quand c’est son tour.
game.py

Contient la classe Game qui gère :

le plateau,
les joueurs,
le tour actuel,
l’ajout des jetons,
la vérification de victoire.

Le plateau réel utilisé est plus grand que 19x19 afin d’ajouter une bordure de sécurité (PAD = 4) utile pour les vérifications et les calculs.

ia.py

Contient la classe IA.

Cette classe stocke les paramètres de l’intelligence artificielle :

Attaque
Defense

Ces coefficients sont utilisés dans l’évaluation des coups.

evaluation.py

Contient toute la logique d’évaluation heuristique du plateau.

Le fichier analyse les alignements dans les différentes directions :

horizontale
verticale
diagonale principale
diagonale secondaire

Les scores attribués dépendent :

de la longueur de la suite,
du fait qu’elle soit bloquée ou ouverte,
de l’utilité potentielle du coup.

Cette partie est essentielle pour guider l’IA.

minimax.py

Version simple de l’algorithme Minimax.

Cette version explore récursivement les coups possibles sans élagage.

Elle est surtout utile comme base de travail ou de comparaison avec la version optimisée.

minimax_alpha_beta.py

Version optimisée utilisant Minimax avec élagage Alpha-Bêta.

Ce fichier contient :

la recherche récursive,
l’élagage alpha-bêta,
des statistiques de performance :
nombre de nœuds visités,
nombre de coupures,
temps passé dans certaines fonctions,
nombre de coups générés.

C’est cette version qui est utilisée par le jeu.

outil.py

Contient plusieurs fonctions utilitaires liées à l’optimisation :

filtrage des zones pertinentes du plateau,
récupération de couches autour des pièces,
génération de coups candidats,
tri des coups selon leur score,
suppression de coups jugés peu intéressants.

Ce fichier permet de limiter fortement le nombre de coups à explorer.

Installation
Prérequis
Python 3.10 ou plus récent
numpy
pygame
Installation des dépendances

```bash
pip install numpy pygame
```

Lancer le projet

Exécuter :

```bash
python main.py
```

Fonctionnement actuel

Dans main.py, deux IA sont créées :

```python
ia_1 = IA(1,100)
ia_2 = IA(1,80)
```

Puis elles sont ajoutées dans la liste des joueurs :

```python
joueurs = [ia_1, ia_2]
```

Cela signifie qu’actuellement la partie lance un match IA contre IA.

Jouer contre l’IA

Pour permettre à un humain de jouer, il faut remplacer l’un des joueurs par None.

Exemple :

```python
joueurs = [None, ia_2]
```

Dans ce cas :

le joueur 1 est humain,
le joueur 2 est contrôlé par l’IA.
Choix techniques
Plateau avec padding

Le plateau est stocké dans un tableau plus grand que 19x19 :

taille réelle jouable : 19x19
padding : 4
taille totale : 27x27

Cela permet de simplifier certaines vérifications autour des cases sans trop se soucier des bords.

Évaluation heuristique

L’évaluation attribue des scores selon les alignements trouvés.

Exemples :

2 jetons alignés : faible score
3 jetons alignés : score plus élevé
4 jetons alignés : score très important
5 jetons alignés : victoire immédiate (inf)

L’IA prend aussi en compte l’adversaire afin de :

préparer ses propres menaces,
bloquer les menaces adverses.
Réduction de l’espace de recherche

Explorer toutes les cases du plateau serait beaucoup trop coûteux.

Le projet réduit donc les coups possibles en se concentrant uniquement sur les zones proches des pièces déjà placées.

Cela accélère fortement Minimax et Alpha-Bêta.

Tri des coups

Avant d’explorer les coups, ceux-ci sont triés selon un score heuristique.

Cela permet à l’algorithme Alpha-Bêta de faire plus de coupures et donc d’être plus rapide.

Limites actuelles

Le projet est fonctionnel, mais plusieurs points peuvent encore être améliorés :

interface graphique non finalisée,
pas d’affichage du gagnant,
pas de menu de démarrage,
pas de bouton pour recommencer une partie,
pas de choix interactif du mode de jeu,
profondeur de recherche encore limitée par le coût de calcul,
certaines parties du code peuvent encore être optimisées.
Pistes d’amélioration
ajouter une vraie interface utilisateur,
afficher le gagnant à la fin de la partie,
ajouter un mode :
joueur contre joueur,
joueur contre IA,
IA contre IA,
permettre de régler la profondeur de recherche,
améliorer encore la fonction d’évaluation,
paralléliser certains calculs,
réécrire les parties critiques dans un langage plus rapide comme le C.
Auteurs / objectif

Ce projet a été réalisé dans un objectif d’apprentissage autour de :

l’intelligence artificielle de jeu,
les algorithmes de recherche,
l’optimisation,
la manipulation de tableaux avec NumPy,
la création d’une interface simple avec Pygame.
