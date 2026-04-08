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
