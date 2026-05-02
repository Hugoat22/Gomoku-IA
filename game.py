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
        self.cases_gagnantes = None
    
    def ajoute_jeton(self,coord : list[int,int] | None) -> None:
        if len(np.argwhere(self.Plateau[PAD:19+PAD,PAD:19+PAD] == 0)) == 0:
            self.gagnant = 3
            return
        if coord is not None:
            if not (0 <= coord[0] < 19 and 0 <= coord[1] < 19):
                return
        else:
            ia = self.joueurs[self.tour_joueur-1]
            coord = minimax_alpha_beta(self.Plateau[PAD:19+PAD,PAD:19+PAD],ia.Profondeur,ia.taux())
        y, x = coord
        if self.Plateau[y+PAD][x+PAD] == 0:
            self.Plateau[y+PAD][x+PAD] = self.tour_joueur
            if self.check(x+PAD,y+PAD):
                self.gagnant = self.tour_joueur
                return
            self.tour_joueur = 1 if self.tour_joueur == 2 else 2
            self.tour += 1

    def check(self,x : int,y : int) -> bool:
        carre = self.Plateau[y-PAD:y+PAD+1,x-PAD:x+PAD+1]
        for direction, elem in enumerate([carre[PAD,:],carre[:,PAD],np.diag(carre),np.diag(np.fliplr(carre))]):
            for i in range(5):
                if np.all(elem[i:i+PAD+1] == self.tour_joueur):
                    self.cases_gagnantes = self._cases_alignees(x, y, direction, i)
                    return True
        return False
    
    def _cases_alignees(self, x : int, y : int, direction : int, debut : int) -> list:
        cases = []
        for k in range(5):
            if direction == 0:    # horizontal
                cases.append((y, x - PAD + debut + k))
            elif direction == 1:  # vertical
                cases.append((y - PAD + debut + k, x))
            elif direction == 2:  # diagonale principale
                cases.append((y - PAD + debut + k, x - PAD + debut + k))
            else:                 # anti-diagonale
                cases.append((y - PAD + debut + k, x + PAD - debut - k))
        return cases