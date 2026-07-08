# coding: utf-8 

"""Modélise le plateau de jeu Hexapawn 3x3."""
import random
from typing import List, Tuple, Dict, Optional
  
############ Fonctions manipulation du plateau ############
# Type personnalisé pour la configuration du plateau (9 entiers)
Plateau = tuple[int, int, int, int, int, int, int, int, int]

def convertir_indice(ligne: int, colonne: int) -> int:
    """Convertit ligne et colonne en indice (0-8)."""
    dim_plateau = int(pow(len(grille_aplatie), 0.5))    # Tj de dim = 3
    return ligne * dim_plateau + colonne

def convertir_tableau(i: int) -> tuple[int, int]:
    """Convertit l'indice en ligne, colonne (0, 2)."""
    dim_plateau = int(pow(len(grille_aplatie), 0.5))
    lig, col = i // dim_plateau, i % dim_plateau
    return (lig, col)

def afficher_grille(grille_aplatie) -> None:
    """Affiche la grille de jeu."""
    affichage = {1: "B", 0: ".", -1: "N"}
    print(f"\nPlateau actuel  Les positions")
    print(" | ".join(f"{affichage[x]:>2}" for x in grille_aplatie[0:3]) + "     0 |  1 |  2")
    print(" | ".join(f"{affichage[x]:>2}" for x in grille_aplatie[3:6]) + "     3 |  4 |  5")
    print(" | ".join(f"{affichage[x]:>2}" for x in grille_aplatie[6:9]) + "     6 |  7 |  8")

def jouer_coup(coup: tuple[int, int], *grille_aplatie:Plateau) -> None:
    """Met à jour la grille avec le coup joué."""
    #dep, arr = coup.depart, coup.arrivee
    dep, arr = coup
    grille_aplatie[arr] = grille_aplatie[dep]
    grille_aplatie[dep] = 0
    
    return grille_aplatie

def trouver_coups(joueur: int) -> list[Coup]:
    """Renvoie les coups possibles pour le joueur spécifié."""
    coups: list[Coup] = []
    direction: int = -1 if joueur == 1 else 1 
    etat_actuel = tuple(grille_aplatie)

    for i in range(9):
        if grille_aplatie[i] == joueur:

            # Déplacement simple vers l'avant
            cible: int = i + (direction * 3)
            if 0 <= cible < 9 and grille_aplatie[cible] == 0:
                coups.append((i, cible))
                
            lig, col = convertir_tableau(i)
            # Captures diagonales
            for d_col in [-1, 1]:
                n_col: int = col + d_col
                if 0 <= n_col <= 2:
                    cible_cap: int = convertir_indice(lig + direction, n_col)
                    if 0 <= cible_cap < 9 and grille_aplatie[cible_cap] == -joueur:
                        coups.append((i, cible_cap))

    return coups

def est_finie(joueur_suivant: int) -> tuple[bool, int]:
    """Vérifie la fin de partie (bool, gagnant)."""
    if 1 in grille_aplatie[:3]: return True, 1     # Les Blancs ont atteint la première ligne
    if 1 not in grille_aplatie: return True, -1    # Les Blancs n'ont plus de pions
    if -1 in grille_aplatie[6:]: return True, -1   # Les Noirs ont atteint la dernière ligne
    if -1 not in grille_aplatie: return True, 1    # Les Noirs n'ont plus de pions
    if not trouver_coups(joueur_suivant):  # Aucun coup possible pour le joueur suivant
        return True, -joueur_suivant
    return False, 0

# Type pour la mémoire de l'IA {Etat: [Liste d'objets Coup]}
MemoireIA = dict[Plateau, list[Coup]]

def simuler_partie(memoire: MemoireIA, grille_aplatie: Plateau) -> int:
    """Simule une partie Humain vs IA aleatoire en construisant l'arbre des coups joués.
    On retourne le gagnant (-1 ou 1)"""
    joueur: int = 1
    termine: bool = False
    gagnant: int = 0
    grille_precedente_ia: Optional[Plateau] = None
    dernier_coup_ia: Optional[Coup] = None
    
    while not termine:
        qui_joue = {1: 'Humain', -1: 'IA'}
        etat_actuel: Plateau = tuple(grille_aplatie)
        coups_possibles: List[Coup] = trouver_coups(joueur)
        #afficher_grille(grille_aplatie)
        print(f"{qui_joue[joueur]} joue -> coups possibles : {coups_possibles}")

        if not coups_possibles:  # Aucun coup possible pour le joueur courant
            gagnant = -joueur
            break
        
        if joueur == 1: # Blancs (Aléatoire)
            coup_choisi: Coup = random.choice(coups_possibles)  # On choisi un coup parmis les coups possibles
            print(f"coup choisi : {coup_choisi}")
            
        else: # Noirs (IA)
            # Si le plateau n'est pas encore connu on ajoute en memoire
            if etat_actuel not in memoire:
                print(f"Nouvel etat detecte pour l'IA : {etat_actuel} - Coups possibles : {coups_possibles}")
                memoire[etat_actuel] = coups_possibles

            if not memoire[etat_actuel]: # Impasse détectée
                gagnant = -joueur
                break # On sort, plus rien à jouer pour l'IA
                
            coup_choisi = random.choice(memoire[etat_actuel])
            print(f"coup choisi : {coup_choisi}")
            dernier_coup_ia = coup_choisi
            grille_precedente_ia = tuple(grille_aplatie)
            
        jouer_coup(coup_choisi, grille_aplatie)
        joueur = -joueur
        termine, gagnant = est_finie(joueur)
        
    #afficher_grille(grille_aplatie)
    print(f"\nPartie finie ! Gagnant : {qui_joue[gagnant]}")

    if gagnant == 1:
        # L'humain gagne donc on enlève le dernier choix de l'IA qui a conduit à sa défaite
        # dernier coup_ia n'est peut être pas défini si l'IA n'a jamais joué ???????????
        print(f"'\nL'IA a perdu, on supprime le dernier coup joue de la memoire : {etat_actuel} pour {dernier_coup_ia}")
        if dernier_coup_ia and grille_precedente_ia in memoire:
            print(f"IA perdante, on supprime pour le coup {dernier_coup_ia} l'etat {grille_precedente_ia} de la memoire")
            memoire[grille_precedente_ia].remove(dernier_coup_ia)
                
    return gagnant
    
def humain_vs_ia(memoire: MemoireIA, grille_aplatie: Plateau) -> None:
    """Permet à un humain d'affronter l'IA."""

    joueur:int = 1 # Vous jouez les Blancs
    termine: bool = False
    gagnant: int = 0
    coup_precedent: Optional[Coup] = None


    while not termine:
        # --- Initialisation ---
        qui_joue = {1: 'Humain', -1: 'IA'}
        print(f"\n>>> Joueur '{qui_joue[joueur]}' joue <<<")
        afficher_grille(grille_aplatie)
        coups_possibles = trouver_coups(joueur)
        
        if joueur == 1:
            coup_valide = False
            print(f"Coups possibles restants pour l'humain : {coups_possibles}")
            while not coup_valide:
                    try:        
                        dep = int(input("Indice de depart : "))
                        arr = int(input("Indice d'arrivee : "))
                        coup_joue = (dep, arr)
                        assert coup_joue in coups_possibles
                        coup_valide = True
                    except AssertionError:
                        print("Coup invalide. Veuillez réessayer.")
        else:
            etat = tuple(grille_aplatie)
            print(f"Coups possibles restants pour l'IA : {memoire[etat]}")
            coup_joue = random.choice(memoire[etat])
            print(f"L'IA joue : {coup_joue}")
            
        
        #coup_joue = Coup(dep, arr, etat_precedent=tuple(grille), coups_possibles=coups_possibles)
        jouer_coup(coup_joue, grille_aplatie)
        joueur = -joueur
        termine, gagnant = est_finie(joueur)
    
    print(f"\nPartie finie ! Gagnant : {'Humain' if gagnant == 1 else 'IA'}")

def humain_vs_ia_vide() -> int:
    """Simule une partie Humain vs IA aleatoire en construisant l'arbre des coups joués.
    On retourne le gagnant (-1 ou 1)"""
    continuer = ""
    ia_data: MemoireIA = {}
    while continuer != "q":
        grille_aplatie: Plateau = [-1, -1, -1, 0, 0, 0, 1, 1, 1]
        joueur: int = 1
        termine: bool = False
        gagnant: int = 0
        grille_precedente_ia: Optional[Plateau] = None
        dernier_coup_ia: Optional[Coup] = None
        
        while not termine:
            qui_joue = {1: 'Humain', -1: 'IA'}
            etat_actuel: Plateau = tuple(grille_aplatie)
            coups_possibles: List[Coup] = trouver_coups(joueur)
            afficher_grille(grille_aplatie)
            print(f"{qui_joue[joueur]} joue -> coups possibles : {coups_possibles}")

            if not coups_possibles:  # Aucun coup possible pour le joueur courant
                gagnant = -joueur
                break
            
            if joueur == 1: # Blancs (Aléatoire)
                coup_valide = False
                print(f"Coups possibles restants pour l'humain : {coups_possibles}")
                while not coup_valide:
                        try:        
                            dep = int(input("Indice de depart : "))
                            arr = int(input("Indice d'arrivee : "))
                            coup_choisi = (dep, arr)
                            assert coup_choisi in coups_possibles
                            coup_valide = True
                        except AssertionError:
                            print("Coup invalide. Veuillez réessayer.")
                
            else: # Noirs (IA)
                # Si le plateau n'est pas encore connu on ajoute en memoire
                if etat_actuel not in memoire:
                    print(f"Nouvel etat detecte pour l'IA : {etat_actuel} - Coups possibles : {coups_possibles}")
                    memoire[etat_actuel] = coups_possibles

                if not memoire[etat_actuel]: # Impasse détectée
                    gagnant = -joueur
                    break # On sort, plus rien à jouer pour l'IA
                    
                coup_choisi = random.choice(memoire[etat_actuel])
                print(f"coup choisi : {coup_choisi}")
                dernier_coup_ia = coup_choisi
                grille_precedente_ia = tuple(grille_aplatie)
                
            jouer_coup(coup_choisi, grille_aplatie)
            joueur = -joueur
            termine, gagnant = est_finie(joueur)
            
        afficher_grille(grille_aplatie)
        print(f"\nPartie finie ! Gagnant : {qui_joue[gagnant]}")

        if gagnant == 1:
            # L'humain gagne donc on enlève le dernier choix de l'IA qui a conduit à sa défaite
            # dernier coup_ia n'est peut être pas défini si l'IA n'a jamais joué ???????????
            print(f"'\nL'IA a perdu, on supprime le dernier coup joue de la memoire : {etat_actuel} pour {dernier_coup_ia}")
            if dernier_coup_ia and grille_precedente_ia in memoire:
                print(f"IA perdante, on supprime pour le coup {dernier_coup_ia} l'etat {grille_precedente_ia} de la memoire")
                memoire[grille_precedente_ia].remove(dernier_coup_ia)
                    
        #return gagnant
    
        continuer = input("'q' quit ou 'enter'")
    
    
if __name__ == "__main__":
    message = """1. jouer avec un pré-traitement
2. jouer sans pré-traitement
"""
    mon_choix = int(input(message))
    if mon_choix == 1:
        # Phase d'apprentissage (100 simulations)
        ia_data: MemoireIA = {}
        for _ in range(150):
            # Grille aplatie : -1 (Noir/IA), 1 (Blanc/Humain), 0 (Vide)
            grille_aplatie: Plateau = [-1, -1, -1, 0, 0, 0, 1, 1, 1]
            simuler_partie(ia_data, grille_aplatie)
            print(ia_data)
            
        print(f"Apprentissage termine. {len(ia_data)} etats en memoire.")

        # Phase de jeu
        grille_aplatie: list[int] = [-1, -1, -1, 0, 0, 0, 1, 1, 1]
        humain_vs_ia(ia_data, grille_aplatie)
    else:
        # Phase de jeu
        ia_data: MemoireIA = {}
        print(f"Apprentissage en cours de jeu. {len(ia_data)} etats en memoire.")
        humain_vs_ia_vide()

