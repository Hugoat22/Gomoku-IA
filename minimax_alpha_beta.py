import time
import numpy as np
from evaluation import *
from outil import *

NB_NOEUDS, NB_CUTS = 0, 0

TEMPS_TRIE_SCORE = 0.0
TEMPS_SCORE_PLT = 0.0
NB_APPELS_TRIE_SCORE = 0
NB_APPELS_SCORE_PLT = 0
NB_COUPS_GENERES = 0

def reset_stats():
    global NB_NOEUDS, NB_CUTS
    global TEMPS_TRIE_SCORE, TEMPS_SCORE_PLT
    global NB_APPELS_TRIE_SCORE, NB_APPELS_SCORE_PLT
    global NB_COUPS_GENERES

    NB_NOEUDS = 0
    NB_CUTS = 0
    TEMPS_TRIE_SCORE = 0.0
    TEMPS_SCORE_PLT = 0.0
    NB_APPELS_TRIE_SCORE = 0
    NB_APPELS_SCORE_PLT = 0
    NB_COUPS_GENERES = 0

def score_plt_profile(plt, joueur):
    global TEMPS_SCORE_PLT, NB_APPELS_SCORE_PLT

    t0 = time.perf_counter()
    res = score_plt(plt, joueur)
    TEMPS_SCORE_PLT += time.perf_counter() - t0
    NB_APPELS_SCORE_PLT += 1

    return res

def trie_score_profile(plt, joueur):
    global TEMPS_TRIE_SCORE, NB_APPELS_TRIE_SCORE, NB_COUPS_GENERES

    t0 = time.perf_counter()
    res = trier_coups(plt, joueur)
    TEMPS_TRIE_SCORE += time.perf_counter() - t0
    NB_APPELS_TRIE_SCORE += 1
    NB_COUPS_GENERES += len(res)

    return res

def barre_progression(index, total, taille=20):
    ratio = (index + 1) / total
    plein = int(ratio * taille)
    vide = taille - plein
    return "[" + "#" * plein + "-" * vide + "]"

def minimax_alpha_beta(plateau,profondeur=3,taux=[1,10]):
    reset_stats()
    t0_total = time.perf_counter()
    global NB_NOEUDS, NB_CUTS
    NB_NOEUDS = 0
    NB_CUTS = 0
    if len(np.argwhere((plateau == 1) | (plateau == 2))) == 0:
        return [9,9]
    
    alpha = -float("inf")
    beta = float("inf")

    joueur = 1 if profondeur%2==0 else 2
    
    Eval = -float("inf") if joueur == 2 else float("inf")

    plt = filtre_map(plateau,profondeur)

    coups = trier_coups(plt,joueur,plateau)

    coord = coups[0]

    for index,(yy,xx) in enumerate(coups):
        bar = barre_progression(index, len(coups))
        progression = ((index + 1) / len(coups)) * 100
        print(f"{bar} {progression:5.1f}% | IA {(len(np.argwhere((plateau == 1) | (plateau == 2)))%2)+1} | coup ({xx},{yy})")

        plt[yy,xx] = joueur
        score = rec_minimax(plt,profondeur-1,alpha,beta,taux)
        plt[yy,xx] = 0

        if (joueur == 2 and score == float("inf")) or (joueur == 1 and score == -float("inf")):
            return [xx,yy]

        Eval_pre = Eval

        if joueur == 2:
            Eval = max(Eval, score)
            alpha = max(alpha, Eval)
        else:
            Eval = min(Eval, score)
            beta = min(beta, Eval)

        if Eval_pre != Eval:
            coord = [xx,yy]

        if beta <= alpha:
            break

    temps_total = time.perf_counter() - t0_total

    """
    debug pour optimiser la vitesse et le nombre de coups
    print(f"temps total : {temps_total:.6f} s")
    print(f"noeuds visités : {NB_NOEUDS}")
    print(f"coupures alpha-beta : {NB_CUTS}")
    print(f"temps trie_score : {TEMPS_TRIE_SCORE:.6f} s")
    print(f"appels trie_score : {NB_APPELS_TRIE_SCORE}")
    print(f"temps score_plt : {TEMPS_SCORE_PLT:.6f} s")
    print(f"appels score_plt : {NB_APPELS_SCORE_PLT}")
    print(f"coups générés : {NB_COUPS_GENERES}")
    

    if NB_APPELS_TRIE_SCORE > 0:
        print(f"moyenne coups / appel trie_score : {NB_COUPS_GENERES / NB_APPELS_TRIE_SCORE:.2f}")

    if NB_NOEUDS > 0:
        print(f"moyenne temps / noeud : {temps_total / NB_NOEUDS:.8f} s")

    """
    return coord

def rec_minimax(plt,profondeur,alpha,beta,taux):
    global NB_NOEUDS, NB_CUTS
    NB_NOEUDS += 1
    joueur = 1 if profondeur%2==0 else 2

    """
    if profondeur == 0:
        return taux[0] * score_plt(plt,2) - taux[1] * score_plt(plt,1)
    """
    
    if profondeur == 0:
        return taux[0] * score_plt_profile(plt, 2) - taux[1] * score_plt_profile(plt, 1)
    
    Eval = -float("inf") if joueur == 2 else float("inf")

    coups_tries = trie_score_profile(plt, joueur)

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
            NB_CUTS += 1
            break

    return Eval
