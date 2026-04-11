import numpy as np
from ia import *
from minimax_alpha_beta import *

PAD = 4
TAILLE = 19
PLATEAU = (PAD * 2) + TAILLE

class Game:

    def __init__(self,joueurs : list[None | IA]) -> None:
        self.Plateau = np.zeros((27,27),dtype=np.int64)
        self.joueurs = joueurs
        self.tour_joueur = 1
        self.tour = 1
        self.gagnant = None
    
    def ajoute_jeton(self,coord : list[int,int] | None) -> None:
        if coord is not None:
            if not (0 <= coord[0] < 19 and 0 <= coord[1] < 19):
                return
        else:
             ia = self.joueurs[self.tour_joueur-1]
             coord = minimax_alpha_beta(self.Plateau[PAD:19+PAD,PAD:19+PAD],ia.Profondeur,ia.taux())
        if self.Plateau[coord[1]+PAD][coord[0]+PAD] == 0:
            self.Plateau[coord[1]+PAD][coord[0]+PAD] = self.tour_joueur
            if self.check(coord[0]+PAD,coord[1]+PAD):
                self.gagnant = self.tour_joueur
                return
            self.tour_joueur = 1 if self.tour_joueur == 2 else 2
            self.tour += 1

    def check(self,x : int,y : int) -> bool:
        carre = self.Plateau[y-PAD:y+PAD+1,x-PAD:x+PAD+1]
        for elem in [carre[PAD,:],carre[:,PAD],np.diag(carre),np.diag(np.fliplr(carre))]:
            for i in range(5):
                if np.all(elem[i:i+PAD+1] == self.tour_joueur):
                    return True
        return False
    
