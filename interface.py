import pygame
import numpy as np

FOND           = ( 12,  17,  35)
PLATEAU_FOND   = (191, 147,  83)
BORD_PLATEAU   = (155, 112,  48)
LIGNES         = (100,  68,  22)
PIECE_NOIR     = ( 22,  22,  22)
PIECE_BLANC    = (245, 240, 225)
CONTOUR_BLANC  = (160, 150, 130)
FOND_BARRE     = ( 18,  25,  52)
SEPARATEUR     = ( 55,  80, 160)
ROUGE          = (230,  75,  55)
OR             = (255, 205,  50)
TEXTE          = (215, 218, 230)
TEXTE_GRIS     = (130, 138, 165)
BTN_FOND       = ( 28,  42,  90)
BTN_SURVOL     = ( 48,  72, 145)
COULEUR_HOSHI  = ( 80,  48,  12)

TAILLE         = 19
LARGEUR_JEU    = 780
HAUTEUR_TOTALE = 780
LARGEUR_BARRE  = 320
LARGEUR_TOTALE = LARGEUR_JEU + LARGEUR_BARRE    # 1100

BORDURE    = 55
DIST       = (LARGEUR_JEU - 2 * BORDURE) / (TAILLE - 1)   # ≈ 37.2 px
PAD        = 4
RAYON      = int(DIST / 2) - 1
RAYON_HOSHI = 4

class Bouton:
    def __init__(self, rect, texte):
        self.rect  = pygame.Rect(rect)
        self.texte = texte

    def dessiner(self, ecran, police):
        survol  = self.rect.collidepoint(pygame.mouse.get_pos())
        couleur = BTN_SURVOL if survol else BTN_FOND
        pygame.draw.rect(ecran, couleur,     self.rect, border_radius=8)
        pygame.draw.rect(ecran, SEPARATEUR, self.rect, 2, border_radius=8)
        surface = police.render(self.texte, True, TEXTE)
        ecran.blit(surface, surface.get_rect(center=self.rect.center))

    def clique(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(event.pos))

def afficher_menu(ecran, boutons, polices):
    police_titre, _, police_moyenne, police_petite = polices
    ecran.fill(FOND)

    pygame.draw.circle(ecran, (20, 30, 65), (160, 120), 190)
    pygame.draw.circle(ecran, (20, 30, 65), (940, 650), 210)

    titre = police_titre.render("GOMOKU", True, OR)
    sous  = police_petite.render("Alignez 5 pions de suite pour gagner", True, TEXTE_GRIS)
    ecran.blit(titre, titre.get_rect(center=(LARGEUR_TOTALE // 2, 175)))
    ecran.blit(sous,  sous.get_rect(center=(LARGEUR_TOTALE // 2, 248)))

    pygame.draw.line(ecran, SEPARATEUR,
                     (LARGEUR_TOTALE // 2 - 170, 272),
                     (LARGEUR_TOTALE // 2 + 170, 272), 1)

    for bouton in boutons:
        bouton.dessiner(ecran, police_moyenne)

    pygame.display.update()

def vers_pixel(col, ligne):
    """Coordonnées grille (col, ligne) → pixels écran (x, y)."""
    return int(BORDURE + col * DIST), int(BORDURE + ligne * DIST)


def afficher_plateau(ecran, partie):
    fin_grille = int(BORDURE + (TAILLE - 1) * DIST)

    pygame.draw.rect(ecran, PLATEAU_FOND,  (0, 0, LARGEUR_JEU, HAUTEUR_TOTALE))
    pygame.draw.rect(ecran, BORD_PLATEAU,  (0, 0, LARGEUR_JEU, HAUTEUR_TOTALE), 5)

    for ligne in range(TAILLE):
        y = int(BORDURE + ligne * DIST)
        pygame.draw.line(ecran, LIGNES, (BORDURE, y), (fin_grille, y), 1)

    for col in range(TAILLE):
        x = int(BORDURE + col * DIST)
        pygame.draw.line(ecran, LIGNES, (x, BORDURE), (x, fin_grille), 1)

    for h in [3, 9, 15]:
        for k in [3, 9, 15]:
            pygame.draw.circle(ecran, COULEUR_HOSHI, vers_pixel(h, k), RAYON_HOSHI)

    for y_plt, x_plt in np.argwhere(partie.Plateau == 1):
        col, ligne = int(x_plt - PAD), int(y_plt - PAD)
        if 0 <= col < TAILLE and 0 <= ligne < TAILLE:
            pygame.draw.circle(ecran, PIECE_NOIR, vers_pixel(col, ligne), RAYON)

    for y_plt, x_plt in np.argwhere(partie.Plateau == 2):
        col, ligne = int(x_plt - PAD), int(y_plt - PAD)
        if 0 <= col < TAILLE and 0 <= ligne < TAILLE:
            pygame.draw.circle(ecran, PIECE_BLANC, vers_pixel(col, ligne), RAYON)

    if partie.gagnant and partie.gagnant != 3 and partie.cases_gagnantes:
        debut = partie.cases_gagnantes[0]
        fin   = partie.cases_gagnantes[-1]
        p1 = vers_pixel(debut[1] - PAD, debut[0] - PAD)
        p2 = vers_pixel(fin[1]   - PAD, fin[0]   - PAD)
        pygame.draw.line(ecran, OR, p1, p2, 6)
        for cy, cx in partie.cases_gagnantes:
            pygame.draw.circle(ecran, OR, vers_pixel(cx - PAD, cy - PAD), RAYON + 4, 3)

def afficher_barre(ecran, partie, nom_mode, ia_joue, polices, boutons_fin=None):
    police_titre, police_grande, police_moyenne, police_petite = polices
    x_barre  = LARGEUR_JEU
    cx_barre = x_barre + LARGEUR_BARRE // 2

    pygame.draw.rect(ecran, FOND_BARRE, (x_barre, 0, LARGEUR_BARRE, HAUTEUR_TOTALE))
    pygame.draw.line(ecran, SEPARATEUR, (x_barre, 0), (x_barre, HAUTEUR_TOTALE), 2)

    titre = police_grande.render("GOMOKU", True, OR)
    ecran.blit(titre, titre.get_rect(center=(cx_barre, 48)))

    mode_surf = police_petite.render(nom_mode, True, TEXTE_GRIS)
    ecran.blit(mode_surf, mode_surf.get_rect(center=(cx_barre, 88)))

    pygame.draw.line(ecran, SEPARATEUR,
                     (x_barre + 20, 112), (x_barre + LARGEUR_BARRE - 20, 112), 1)

    if partie.gagnant is None:
        joueur       = partie.tour_joueur
        couleur_pion = PIECE_NOIR if joueur == 1 else PIECE_BLANC

        lbl = police_petite.render("À jouer :", True, TEXTE_GRIS)
        ecran.blit(lbl, (x_barre + 28, 142))

        cx_pion, cy_pion = x_barre + 64, 202
        pygame.draw.circle(ecran, couleur_pion, (cx_pion, cy_pion), 24)

        nom_surf = police_grande.render(f"Joueur {joueur}", True, TEXTE)
        ecran.blit(nom_surf, (x_barre + 102, cy_pion - nom_surf.get_height() // 2))

        if ia_joue:
            animation = ["", ".", "..", "..."]
            frame = (pygame.time.get_ticks() // 400) % 4
            surf_ia = police_petite.render(f"IA réfléchit{animation[frame]}", True, ROUGE)
            ecran.blit(surf_ia, surf_ia.get_rect(center=(cx_barre, 252)))

        pygame.draw.line(ecran, SEPARATEUR,
                         (x_barre + 20, 285), (x_barre + LARGEUR_BARRE - 20, 285), 1)

        tour_surf = police_petite.render(f"Tour n°  {partie.tour}", True, TEXTE_GRIS)
        ecran.blit(tour_surf, (x_barre + 28, 302))

    else:
        if partie.gagnant == 3:
            msg = police_grande.render("Égalité !", True, TEXTE)
            ecran.blit(msg, msg.get_rect(center=(cx_barre, 185)))
        else:
            joueur       = partie.gagnant
            couleur_pion = PIECE_NOIR if joueur == 1 else PIECE_BLANC

            cx_pion, cy_pion = cx_barre, 158
            pygame.draw.circle(ecran, couleur_pion, (cx_pion, cy_pion), 28)

            gagnant_surf = police_grande.render(f"Joueur {joueur} gagne !", True, OR)
            ecran.blit(gagnant_surf, gagnant_surf.get_rect(center=(cx_barre, 210)))

        pygame.draw.line(ecran, SEPARATEUR,
                         (x_barre + 20, 248), (x_barre + LARGEUR_BARRE - 20, 248), 1)

        fin_surf = police_petite.render(f"Partie en {partie.tour} tours", True, TEXTE_GRIS)
        ecran.blit(fin_surf, fin_surf.get_rect(center=(cx_barre, 268)))

        if boutons_fin:
            for bouton in boutons_fin:
                bouton.dessiner(ecran, police_moyenne)
