import pygame
import numpy as np
from game import Game
from ia import IA

NOIR = (0,0,0)
BLANC = (255,255,255)
BEIGE = (240, 200, 140)

TAILLE = 19
LARGEUR = HAUTEUR = 900
BORDURE = LARGEUR * 0.1
DIST = (LARGEUR - 2 * BORDURE) / (TAILLE - 1)

PAD = 4

pygame.init()

screen = pygame.display.set_mode((LARGEUR, HAUTEUR))

pygame.display.set_caption("Gomoku IA")

def draw_board(partie):
    screen.fill(BEIGE)

    for y in range(TAILLE):
        pygame.draw.line(screen,NOIR,(BORDURE,BORDURE+DIST*y),(LARGEUR - BORDURE,BORDURE+DIST*y),2)
    for x in range(TAILLE):
        pygame.draw.line(screen,NOIR,(BORDURE+DIST*x,BORDURE),(BORDURE+DIST*x,HAUTEUR - BORDURE),2)

    for x,y in np.argwhere((partie.Plateau == 1) | (partie.Plateau == 2)):
        pygame.draw.circle(screen,NOIR,(BORDURE + (y - PAD) * DIST  ,BORDURE + (x - PAD) * DIST ),DIST/2)
    for x,y in np.argwhere(partie.Plateau == 2):
        pygame.draw.circle(screen,BLANC,(BORDURE + (y - PAD) * DIST  ,BORDURE + (x - PAD) * DIST ),DIST/2)


def start():

    ia_1 = IA(1,100)

    ia_2 = IA(1,80)

    joueurs = [ia_1,ia_2]

    partie = Game(joueurs)

    while partie.gagnant is None:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if partie.joueurs[partie.tour_joueur-1] is None:
                    x,y = pygame.mouse.get_pos()
                    coord = [int(round((x - BORDURE) / DIST)), int(round((y - BORDURE) / DIST))]
                    partie.ajoute_jeton(coord)
                    
        draw_board(partie)
        pygame.display.update()

        if partie.joueurs[partie.tour_joueur-1] is not None:
            partie.ajoute_jeton(None)

    while True:
        draw_board(partie)
        pygame.display.update()

    #interface graphique non finie, pas de gestion de la fin de partie ni de l'affichage du gagnant, ni de possibilité de recommencer une partie, etc.
    #focus sur l'ia et l'optimisation de celle ci, pas sur l'interface graphique
        
start()