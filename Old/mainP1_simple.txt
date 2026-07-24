# coding: utf-8

"""
    L'HexaPion (ou HexaPawn) est un jeu de stratégie abstrait minimaliste inventé par Martin Gardner en 1962.
    Sur un mini-échiquier de 3x3 cases, deux joueurs s’affrontent avec trois pions chacun, en respectant les règles classiques de déplacement et de prise des échecs.
    L'objectif de cet exercice est d'implémenter les règles de ce jeu et de concevoir un algorithme capable d'apprendre par essais-erreurs pour devenir imbattable.

    Modélise le plateau de jeu Hexapion 3x3.

    CECI EST UNE VERSION EN MODE SIMPLE POUR TESTER LE JEU HUMAIN VS IA, SANS SIMULATION DE L'IA.
    L'IA A CEPENDANT UNE MEMOIRE DEJA ENREGISTREE SUR DISQUE POUR APPRENDRE DES PARTIES PRECEDENTES.

    Elle est maintenant mauvaise perdante car elle supprime de sa mémoire le dernier coup joué si elle perd la partie
    et préfère abandonner si elle n'a plus de coups possibles.
    Si l'humain joue en premier, il perdra toujours contre l'IA.
    Dur dur la vie...

    Pour avoir une IA fairplay, il faut supprimer le fichier ia_data.pkl et relancer le jeu pour que l'IA apprenne à jouer contre l'humain.
"""
import os
import pickle
import random

# Constantes de jeu
DIM = 3  # Dimension fixe du plateau (3x3)
   
def convertir_indice(ligne: int, colonne: int, plateau: list) -> int:
    """Convertit ligne et colonne en indice (0-8)."""
    return ligne * DIM + colonne    # Tj de dim = 3

def convertir_coordonnees(i: int, plateau: list) -> tuple[int, int]:
    """Convertit l'indice en ligne, colonne (0, 2)."""
    lig, col = i // DIM, i % DIM
    return (lig, col)

def afficher_grille(plateau: list) -> None:
    """Affiche la grille de jeu."""
    affichage = {1: "B", 0: ".", -1: "N"}
    print(f"\nPlateau actuel  Les positions")
    print(" | ".join(f"{affichage[x]:>2}" for x in plateau[0:3]) + "     0 |  1 |  2")
    print(" | ".join(f"{affichage[x]:>2}" for x in plateau[3:6]) + "     3 |  4 |  5")
    print(" | ".join(f"{affichage[x]:>2}" for x in plateau[6:9]) + "     6 |  7 |  8")

def jouer_coup(coup: tuple[int, int], plateau: list) -> list:
    """Retourne un nouveau plateau après le coup joué."""
    depart, arrivee = coup
    nouvelle_grille = list(plateau)
    nouvelle_grille[arrivee] = nouvelle_grille[depart]
    nouvelle_grille[depart] = 0
    return tuple(nouvelle_grille)

def trouver_coups(joueur: int, plateau: tuple[int, ...]) -> list[tuple[int, int]]:
    """ Renvoie les coups possibles pour le joueur spécifié
        Sous la forme d'une liste de tuples représentant les coups """
    coups_possibles: list = []
    direction: int = -1 if joueur == 1 else 1

    for i in range(DIM * DIM):
        if plateau[i] == joueur:
            # 1. Avancement tout droit (uniquement si la case devant est vide)
            cible_devant = i + (direction * DIM)
            if 0 <= cible_devant < DIM * DIM and plateau[cible_devant] == 0:
                coups_possibles.append((i, cible_devant))

            # 2. Prises diagonales (uniquement si un pion adverse s'y trouve)
            lig, col = convertir_coordonnees(i, plateau)
            for d_col in [-1, 1]:
                n_col = col + d_col
                if 0 <= n_col < DIM:
                    cible_diag = convertir_indice(lig + direction, n_col, plateau)
                    if 0 <= cible_diag < DIM * DIM and plateau[cible_diag] == -joueur:
                        coups_possibles.append((i, cible_diag))

    return coups_possibles

def est_finie(joueur_suivant: int, plateau:  tuple[int, ...]) -> tuple[bool, int]:
    """Vérifie la fin de partie (bool, gagnant)."""
    if 1 in plateau[:3]:
        return (True, 1)     # Les Blancs ont atteint la première ligne
    if 1 not in plateau: 
        return (True, -1)    # Les Blancs n'ont plus de pions
    if -1 in plateau[6:]: 
        return (True, -1)   # Les Noirs ont atteint la dernière ligne
    if -1 not in plateau: 
        return (True, 1)    # Les Noirs n'ont plus de pions
    if not trouver_coups(joueur_suivant, plateau):  # Aucun coup possible pour le joueur suivant
        return (True, -joueur_suivant)
    return (False, 0)

def sauvegarder_memoire(chemin: str, memoire: dict) -> None:
    """Sauvegarde la mémoire de l'IA sur disque (pickle)."""
    try:
        with open(chemin, "wb") as f:
            pickle.dump(memoire, f)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de la memoire: {e}")

def charger_memoire(chemin: str) -> dict:
    """Charge la mémoire de l'IA depuis disque si disponible."""
    if not os.path.exists(chemin):
        return {}
    try:
        with open(chemin, "rb") as f:
            data = pickle.load(f)
            if isinstance(data, dict):
                return data
    except Exception as e:
        print(f"Erreur lors du chargement de la memoire: {e}")
    return {}
    
def humain_vs_ia(joueur: int, memoire: dict[tuple[int, ...]: tuple[int, int]], plateau: tuple[int, ...]) -> int:
    """Permet à un humain d'affronter l'IA."""
    termine: bool = False
    gagnant: int = 0

    # Variables pour mémoriser le dernier coup de l'IA afin d'apprendre en ligne
    dernier_coup_ia = None

    while not termine:
        # --- Initialisation ---
        qui_joue = {1: 'Humain', -1: 'IA'}
        print(f"\n>>> Joueur '{qui_joue[joueur]}' joue <<<")
        afficher_grille(plateau)
        
        if joueur == 1:
            coup_valide = False
            coups_possibles: list[tuple[int, int]] = trouver_coups(joueur, plateau)
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

                    plateau = jouer_coup(coup_joue, plateau)
        else:
            # --- Tour de l'IA ---

            if plateau not in memoire:
                memoire[plateau] = trouver_coups(joueur, plateau)

            print(f"Coups en mémoire pour l'IA : {memoire[plateau]}) pour l'état {plateau}")
            if not memoire[plateau]:
                print("L'IA n'a aucun coup possible. Elle préfère abondonner !")
                termine, gagnant = True, 1  
                break
            coup_joue = random.choice(memoire[plateau]) # Récupère un objet de la liste des objets
            print(f"L'IA a choisi le coup : {coup_joue} pour l'état {plateau}")
            dernier_coup_ia = coup_joue
            
            plateau_precedent_ia = plateau # Pour supp du plateau si IA perdante le cas échéant
            plateau = jouer_coup(coup_joue, plateau)

        joueur = -joueur
        termine, gagnant = est_finie(joueur, plateau)

    # Si l'IA a perdu, retirer le dernier coup choisi depuis la mémoire
    if gagnant == 1 and dernier_coup_ia is not None and plateau_precedent_ia in memoire:
        print(f"L'IA a perdu. Suppression du dernier coup :")
        print(f"{dernier_coup_ia} : {dernier_coup_ia} de l'état {plateau_precedent_ia}.")

        test = [coup for coup in memoire[plateau_precedent_ia]]
        print(f"Mémoire IA avant : {test}")

        for coup in memoire[plateau_precedent_ia]:
            if coup == dernier_coup_ia:
                memoire[plateau_precedent_ia].remove(coup)

        test = [coup for coup in memoire[plateau_precedent_ia]]
        print(f"Memoire après IA : {test}")

        # Si cet état n'a plus aucun coup gagnant possible, on le nettoie
        #if not memoire[plateau_precedent_ia]:
        #    del memoire[plateau_precedent_ia]

    print(f"\nPartie finie ! Gagnant : {'Humain' if gagnant == 1 else 'IA'}")
    return gagnant

def afficher_stat(memoire: dict[tuple[int, ...]: [int, int]], sauvegarde: str) -> None:
    """ Compte le nombre de plateau et de coups possibles total en mémoire """
    cpt_coup = 0
    for valeur in memoire:
        cpt_coup += len(valeur)
                  
    print(f"Memoire IA -> {len(memoire)} grilles pour {cpt_coup} coups depuis le fichier {sauvegarde}")

if __name__ == "__main__":
    # L'IA apprendra au fur et à mesure des parties jouées
    Sauvegarde = "ia_data_P1.pkl"
    ia_data: dict[tuple[int, ...], tuple[tuple[int, int]]] = charger_memoire(Sauvegarde)
    gagnant = 1 # Par défaut l'Humain commence à jouer les Blancs

    jouer = True
    while jouer:
        plateau: tuple[int, ...] = (-1, -1, -1, 0, 0, 0, 1, 1, 1)
        gagnant = humain_vs_ia(gagnant, ia_data, plateau)
        afficher_stat(ia_data, Sauvegarde)
        jouer = input("Voulez-vous rejouer une partie contre l'IA ? (o/n) : ").lower() == 'o'

    # Sauvegarde après la partie pour conserver l'apprentissage
    sauvegarder_memoire(Sauvegarde, ia_data)

