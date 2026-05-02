import pygame
from game import Game
from ia import IA
from interface import *

MODES = [
    ("Humain  vs  Humain", "HH"),
    ("Humain  vs  IA",     "HIA"),
    ("IA  vs  IA",         "IAIA"),
]
NOMS_MODES = {
    "HH":   "Humain vs Humain",
    "HIA":  "Humain vs IA",
    "IAIA": "IA vs IA",
}

pygame.init()
ecran = pygame.display.set_mode((LARGEUR_TOTALE, HAUTEUR_TOTALE))
pygame.display.set_caption("Gomoku")

police_titre   = pygame.font.SysFont("segoeui", 72, bold=True)
police_grande  = pygame.font.SysFont("segoeui", 32, bold=True)
police_moyenne = pygame.font.SysFont("segoeui", 22)
police_petite  = pygame.font.SysFont("segoeui", 17)
polices = (police_titre, police_grande, police_moyenne, police_petite)

def menu():
    cx = LARGEUR_TOTALE // 2
    boutons = [
        Bouton((cx - 190, 308 + i * 78, 380, 55), label)
        for i, (label, _) in enumerate(MODES)
    ]
    while True:
        afficher_menu(ecran, boutons, polices)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            for i, bouton in enumerate(boutons):
                if bouton.clique(event):
                    return MODES[i][1]

def creer_joueurs(mode):
    if mode == "HH":
        return [None, None]
    if mode == "HIA":
        return [None, IA(1, 1, 2)]
    return [IA(1, 1, 2), IA(1, 1, 2)]


def boucle_partie(mode):
    partie   = Game(creer_joueurs(mode))
    nom_mode = NOMS_MODES[mode]
    ia_joue  = False

    x_btn  = LARGEUR_JEU + (LARGEUR_BARRE - 210) // 2
    boutons_fin = [
        Bouton((x_btn, 330, 210, 48), "Rejouer"),
        Bouton((x_btn, 396, 210, 48), "Menu principal"),
    ]

    horloge = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if partie.gagnant is not None:
                if boutons_fin[0].clique(event):
                    return "rejouer", mode
                if boutons_fin[1].clique(event):
                    return "menu", None
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if partie.joueurs[partie.tour_joueur - 1] is None:
                        souris_x, souris_y = pygame.mouse.get_pos()
                        if souris_x < LARGEUR_JEU:
                            col   = int(round((souris_x - BORDURE) / DIST))
                            ligne = int(round((souris_y - BORDURE) / DIST))
                            partie.ajoute_jeton([ligne, col])

        # Tour de l'IA
        if partie.gagnant is None and partie.joueurs[partie.tour_joueur - 1] is not None:
            ia_joue = True
            ecran.fill((0, 0, 0))
            afficher_plateau(ecran, partie)
            afficher_barre(ecran, partie, nom_mode, True, polices)
            pygame.display.update()

            partie.ajoute_jeton(None)
            ia_joue = False

        # Dessin
        ecran.fill((0, 0, 0))
        afficher_plateau(ecran, partie)
        afficher_barre(ecran, partie, nom_mode, ia_joue, polices,
                       boutons_fin if partie.gagnant is not None else None)
        pygame.display.update()
        horloge.tick(60)


def main():
    mode = menu()
    while True:
        action, nouveau_mode = boucle_partie(mode)
        mode = nouveau_mode if action == "rejouer" else menu()


main()
