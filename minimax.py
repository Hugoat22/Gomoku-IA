import numpy as np
from evaluation import *
from outil import *

def minimax(plateau,profondeur=3):

    joueur = 1 if profondeur%2==0 else 2
    
    coups = []

    plt = filtre_map(plateau)

    iteration_max = np.argwhere(plt == 0).shape[0]

    for index,(yy,xx) in enumerate(np.argwhere(plt == 0)):
        print(f"{(index/iteration_max)*100:.2f}%")
        plt[yy,xx] = joueur
        coups.append([(yy,xx),rec_minimax(plt,profondeur-1)])
        plt[yy,xx] = 0

    afficher_grille_scores(plt, coups)

    big = [0,-float("inf")]

    for index, (_, score) in enumerate(coups):
        if big[1] < score:
            big[0] = index
            big[1] = score

    y_f,x_f = coups[big[0]][0]

    return [x_f,y_f]

def rec_minimax(plt,profondeur):
    joueur = 1 if profondeur%2==0 else 2

    if profondeur == 0:
        return score_plt(plt,2) - 10 * score_plt(plt,1)
    
    coups = []

    for yy,xx in np.argwhere(plt == 0):
        plt[yy,xx] = joueur
        coups.append(rec_minimax(plt,profondeur-1))
        plt[yy,xx] = 0

    if joueur == 1:
        return min(coups)
    else:
        return max(coups)
