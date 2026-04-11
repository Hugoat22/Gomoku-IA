import numpy as np

DIRECTION = [(0,1),(1,0),(1,1),(-1,1)]

def valeur_score(avant, apres, taille,utile):
    match taille:
        case 4:
            if avant != 0 and apres != 0:
                return 1000000
            else:
                return 100000
        case 3:
            if avant != 0 and apres != 0:
                return 10000
            else:
                return 1000
        case 2:
            if avant != 0 and apres != 0:
                return 100
            else:
                return 10
        case 1:
            if utile:
                return 10
        case 0:
            if utile:
                return 10
    return 0

def tout_direction(plt,y1,x1,joueur,dir,utile):
    y_dir,x_dir = DIRECTION[dir]
    L,l = plt.shape
    x_pred = x1 - x_dir
    y_pred = y1 - y_dir
    if 0 <= y_pred < L and 0 <= x_pred < l and plt[y_pred,x_pred] == joueur:
        return 0
    x_suc = x1 + x_dir
    y_suc = y1 + y_dir
    score = 0
    taille = 1
    while 0 <= x_suc < l and 0 <= y_suc < L:
        if plt[y_suc,x_suc] != joueur:
            break
        taille += 1
        if taille == 5:
            return float("inf")
        x_suc += x_dir
        y_suc += y_dir
    if (taille >= 2 and utile == False) or utile:
        avant = 0
        x_pred = x1 - x_dir
        y_pred = y1 - y_dir
        while taille + avant != 5 and 0 <= x_pred < l and 0 <= y_pred < L:
            if plt[y_pred,x_pred] != joueur and plt[y_pred,x_pred] != 0:
                break
            avant += 1
            x_pred -= x_dir
            y_pred -= y_dir
        apres = 0
        x_suc = x1 + taille * x_dir
        y_suc = y1 + taille * y_dir
        while taille + apres != 5 and 0 <= x_suc < l and 0 <= y_suc < L:
            if plt[y_suc,x_suc] != joueur and plt[y_suc,x_suc] != 0:
                break
            apres += 1
            x_suc += x_dir
            y_suc += y_dir
        if taille + avant + apres >= 5:
            score += valeur_score(avant, apres, taille, utile)
    return score

def count_pos(plt,y1,x1,joueur,utile=False):
    score = 0

    for dir in range(4):
        score += tout_direction(plt,y1,x1,joueur,dir,utile)
        if score == float("inf"):
            return score

    if np.sum(plt[max(0,y1-1):min(plt.shape[0],y1+2),max(0,x1-1):min(plt.shape[1],x1+2)] == joueur) == 1 and score == 0:
        score += 1

    return score

def score_plt(plt, joueur):
    score = 0

    for y1, x1 in np.argwhere(plt == joueur):
        score += count_pos(plt,y1,x1,joueur)
        if score == float("inf"):
            break
    return score