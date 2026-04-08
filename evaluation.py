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

def horizontal(plt,y1,x1,joueur,utile):
    score = 0
    if (x1 == 0 or plt[y1,max(0,x1-1)] != joueur):
        taille = 0
        for val in plt[y1,x1:min(plt.shape[1],x1+5)]:
            if val != joueur:
                break
            taille += 1
        if taille == 5:
            return float("inf")
        if (taille >= 2 and utile == False) or utile:
            avant = 0
            for val in plt[y1,max(0,x1-(5-taille)):max(0,x1)][::-1]:
                if val != joueur and val != 0:
                    break
                avant += 1
            apres = 0
            for val in plt[y1,min(plt.shape[1],x1+taille):min(plt.shape[1],x1+5)]:
                if val != joueur and val != 0:
                    break
                apres += 1
            if taille + avant + apres >= 5:
               score += valeur_score(avant, apres, taille, utile)
    return score

def vertical(plt,y1,x1,joueur,utile):
    score = 0
    if (y1 == 0 or plt[max(0,y1-1),x1] != joueur):
        taille = 0
        for val in plt[y1:min(plt.shape[0],y1+5),x1]:
            if val != joueur:
                break
            taille += 1
        if taille == 5:
            return float("inf")
        if (taille >= 2 and utile == False) or utile:
            avant = 0
            for val in plt[max(0,y1-(5-taille)):max(0,y1),x1][::-1]:
                if val != joueur and val != 0:
                    break
                avant += 1
            apres = 0
            for val in plt[min(plt.shape[0],y1+taille):min(plt.shape[0],y1+5),x1]:
                if val != joueur and val != 0:
                    break
                apres += 1
            if taille + avant + apres >= 5:
               score += valeur_score(avant, apres, taille, utile)
    return score

def diagonal(plt,y1,x1,joueur,utile):
    score = 0
    if ((x1 == 0 or y1 == 0) or plt[max(0,y1-1),max(0,x1-1)] != joueur):
        taille = 0
        for val in np.diag(plt[y1:min(plt.shape[0],y1+5),x1:min(plt.shape[1],x1+5)]):
            if val != joueur:
                break
            taille += 1
        if taille == 5:
            return float("inf")
        if (taille >= 2 and utile == False) or utile:
            avant = 0
            for val in np.diag(plt[max(0,y1-(5-taille)):max(0,y1),max(0,x1-(5-taille)):max(0,x1)])[::-1]:
                if val != joueur and val != 0:
                    break
                avant += 1
            apres = 0
            for val in np.diag(plt[min(plt.shape[0],y1+taille):min(plt.shape[0],y1+5),min(plt.shape[1],x1+taille):min(plt.shape[1],x1+5)]):
                if val != joueur and val != 0:
                    break
                apres += 1
            if taille + avant + apres >= 5:
               score += valeur_score(avant, apres, taille, utile)
    return score

def diagonal_inverse(plt,y1,x1,joueur,utile):
    score = 0
    if ((x1 == 0 or y1 == plt.shape[0]-1) or plt[y1+1,x1-1] != joueur):
        taille = 0
        for val in np.diag(np.fliplr(plt[max(0, y1-4):y1+1, x1:min(plt.shape[1], x1+5)])):
            if val != joueur:
                break
            taille += 1
        if taille == 5:
            return float("inf")
        if (taille >= 2 and utile == False) or utile:
            avant = 0
            for val in np.diag(np.fliplr(plt[y1+1:min(plt.shape[0],y1+(5-taille)+1),max(0, x1-(5-taille)):x1])):
                if val != joueur and val != 0:
                    break
                avant += 1
            apres = 0
            for val in np.diag(np.fliplr(plt[max(0, y1-taille-(5-taille)+1):y1-taille+1, x1+taille:min(plt.shape[1],x1+5)])):
                if val != joueur and val != 0:
                    break
                apres += 1
            if taille + avant + apres >= 5:
               score += valeur_score(avant, apres, taille, utile)
    return score

def tout_direction(plt,y1,x1,joueur,dir,utile):
    score = 0
    y_dir,x_dir = DIRECTION[joueur]
    # en cours de generalisation des scores de direction, pas encore fonctionnel
def count_pos(plt,y1,x1,joueur,utile=False):
    score = 0

    score += horizontal(plt,y1,x1,joueur,utile)

    if score == float("inf"):
        return score

    score += vertical(plt,y1,x1,joueur,utile)

    if score == float("inf"):
        return score

    score += diagonal(plt,y1,x1,joueur,utile)

    if score == float("inf"):
        return score

    score += diagonal_inverse(plt,y1,x1,joueur,utile)

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