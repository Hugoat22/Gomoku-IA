import numpy as np
from evaluation import *
from outil import *

def minimax_alpha_beta(plateau,profondeur=3,taux=[1,10]):
    if len(np.argwhere((plateau == 1) | (plateau == 2))) == 0:
        return [9,9]
    
    alpha = -float("inf")
    beta = float("inf")

    joueur = 1 if profondeur%2==0 else 2
    
    Eval = -float("inf") if joueur == 2 else float("inf")

    plt = filtre_map(plateau,profondeur)

    coups = trier_coups(plt,joueur,plateau)

    coord = coups[0]

    for (yy,xx) in coups:
        plt[yy,xx] = joueur
        score = rec_minimax(plt,profondeur-1,alpha,beta,taux)
        plt[yy,xx] = 0

        if (joueur == 2 and score == float("inf")) or (joueur == 1 and score == -float("inf")):
            return [yy,xx]

        Eval_pre = Eval

        if joueur == 2:
            Eval = max(Eval, score)
            alpha = max(alpha, Eval)
        else:
            Eval = min(Eval, score)
            beta = min(beta, Eval)

        if Eval_pre != Eval:
            coord = [yy,xx]

        if beta <= alpha:
            break

    return coord

def rec_minimax(plt,profondeur,alpha,beta,taux):
    joueur = 1 if profondeur%2==0 else 2

    if profondeur == 0:
        return taux[0] * score_plt(plt,2) - taux[1] * score_plt(plt,1)
    
    Eval = -float("inf") if joueur == 2 else float("inf")

    coups_tries = trier_coups(plt, joueur)

    for (yy,xx) in coups_tries:
        plt[yy,xx] = joueur
        score = rec_minimax(plt,profondeur-1,alpha,beta,taux)
        plt[yy,xx] = 0
        
        if joueur == 2 and score == float("inf"):
            return float("inf")
        if joueur == 1 and score == -float("inf"):
            return -float("inf")

        if joueur == 2:
            Eval = max(Eval, score)
            alpha = max(alpha, Eval)
        else:
            Eval = min(Eval, score)
            beta = min(beta, Eval)

        if beta <= alpha:
            break

    return Eval
