import numpy as np
from evaluation import *

ORIGINE_PROFONDEUR = 0

def filtre_map(plt,profondeur):
    global ORIGINE_PROFONDEUR
    ORIGINE_PROFONDEUR = profondeur
    masque = np.full(plt.shape, -1, dtype=np.int64)

    for (yy,xx) in np.argwhere((plt == 1) | (plt == 2)):
        borne_y = [
            max(yy-profondeur,0),
            min(yy+(profondeur+1),plt.shape[0])
        ]

        borne_x = [
            max(xx-profondeur,0),
            min(xx+(profondeur+1),plt.shape[1])
        ]

        masque[borne_y[0]:borne_y[1],borne_x[0]:borne_x[1]] = plt[borne_y[0]:borne_y[1],borne_x[0]:borne_x[1]]
    
    return masque

def recup_couche(plt, couche):
    map = np.full(plt.shape, -1, dtype=np.int64)
    for (yy,xx) in np.argwhere((plt == 1) | (plt == 2)):
        borne_y = [
            max(0,yy-couche),
            min(plt.shape[0],yy+(couche+1))
        ]

        borne_x = [
            max(0,xx-couche),
            min(plt.shape[1],xx+(couche+1))
        ]
        map[borne_y[0]:borne_y[1],borne_x[0]:borne_x[1]] = plt[borne_y[0]:borne_y[1],borne_x[0]:borne_x[1]]
    return map

def trier_coups(plt,joueur,plateau=None):
    global ORIGINE_PROFONDEUR
    coups = []
    visite = set()
    for i in range(1,ORIGINE_PROFONDEUR+1):
        couche = recup_couche(plt, i)
        for coord in np.argwhere(couche == 0):
            if tuple(coord) not in visite:
                if plateau is not None:
                    retirer_coups(couche, coord, plateau)
                coups.append(coord)
                visite.add(tuple(coord))
    return trie_score(plt, joueur, coups)

def trie_score(plt, joueur, coups):
    adv = 1 if joueur == 2 else 2
    scores = []
    for coup in coups:
        if plt[coup[0], coup[1]] != 0:
            continue
        plt[coup[0], coup[1]] = joueur
        score_joueur = count_pos(plt,coup[0], coup[1], joueur,local=True)
        plt[coup[0], coup[1]] = adv
        score_adv = count_pos(plt,coup[0], coup[1], adv, local=True)
        plt[coup[0], coup[1]] = 0
        score_general = score_joueur - score_adv
        if abs(score_general) == float("inf"):
            return [coup]
        scores.append((coup, score_general))
    scores.sort(key=lambda x: x[1], reverse=True)
    return [coup for coup, _ in scores]

def retirer_coups(plt, coord, plateau):
    point = 0
    plateau[coord[0],coord[1]] = 2
    if count_pos(plateau,coord[0],coord[1],2,True) >= 10:
        point += 1

    plateau[coord[0],coord[1]] = 1
    if count_pos(plateau,coord[0],coord[1],1,True) >= 10:
        point += 1

    if point == 0:
        plateau[coord[0],coord[1]] = -1
        plt[coord[0],coord[1]] = -1
    else:
        plateau[coord[0],coord[1]] = 0