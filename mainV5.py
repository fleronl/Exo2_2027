# coding: utf-8

"""
    L'HexaPion (ou HexaPawn) est un jeu de stratégie abstrait minimaliste inventé par Martin Gardner en 1962.
    Sur un mini-échiquier de 3x3 cases, deux joueurs s’affrontent avec trois pions chacun, en respectant les règles classiques de déplacement et de prise des échecs.
    L'objectif de cet exercice est d'implémenter les règles de ce jeu et de concevoir un algorithme capable d'apprendre par essais-erreurs pour devenir imbattable.

    Modélise le plateau de jeu Hexapion 3x3.

    CECI EST UNE VERSION SANS LA PHASE DE SIMULATION DE L'IA, POUR TESTER LE JEU HUMAIN VS IA.
"""
import os
import pickle
import random

# Constantes de jeu
DIM = 3  # Dimension fixe du plateau (3x3)
   
class Coup:
    """Représente un déplacement de pion (départ -> arrivée) et stocke l'état d'origine."""
    def __init__(self, depart: int, arrivee: int, etat_precedent: tuple[int, ...] = None):
        self.depart = depart
        self.arrivee = arrivee
        # On mémorise l'état du plateau avant que ce coup ne soit joué
        self.etat_precedent = etat_precedent

    def __repr__(self) -> str:
        """Représentation textuelle d'un coup."""
        return f"{self.depart} -> {self.arrivee}"

#################################
    
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

def jouer_coup(coup: Coup, plateau: list) -> list:
    """Retourne un nouveau plateau après le coup joué."""
    nouvelle_grille = list(plateau)
    nouvelle_grille[coup.arrivee] = nouvelle_grille[coup.depart]
    nouvelle_grille[coup.depart] = 0

    return tuple(nouvelle_grille)

def trouver_coups(joueur: int, plateau: tuple[int, ...]) -> list[Coup]:
    """Renvoie les coups possibles pour le joueur spécifié."""
    coups_possibles: list = []
    direction: int = -1 if joueur == 1 else 1

    for i in range(DIM * DIM):
        if plateau[i] == joueur:
            # 1. Avancement tout droit (uniquement si la case devant est vide)
            cible_devant = i + (direction * DIM)
            if 0 <= cible_devant < DIM * DIM and plateau[cible_devant] == 0:
                coups_possibles.append(Coup(i, cible_devant, plateau))

            # 2. Prises diagonales (uniquement si un pion adverse s'y trouve)
            lig, col = convertir_coordonnees(i, plateau)
            for d_col in [-1, 1]:
                n_col = col + d_col
                if 0 <= n_col < DIM:
                    cible_diag = convertir_indice(lig + direction, n_col, plateau)
                    if 0 <= cible_diag < DIM * DIM and plateau[cible_diag] == -joueur:
                        coups_possibles.append(Coup(i, cible_diag, plateau))

    return coups_possibles

def est_finie(joueur_suivant: int, plateau:  tuple[int, ...]) -> tuple[bool, int]:
    """Vérifie la fin de partie (bool, gagnant)."""
    if 1 in plateau[:3]: return True, 1     # Les Blancs ont atteint la première ligne
    if 1 not in plateau: return True, -1    # Les Blancs n'ont plus de pions
    if -1 in plateau[6:]: return True, -1   # Les Noirs ont atteint la dernière ligne
    if -1 not in plateau: return True, 1    # Les Noirs n'ont plus de pions
    if not trouver_coups(joueur_suivant, plateau):  # Aucun coup possible pour le joueur suivant
        return True, -joueur_suivant
    return False, 0

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
    
def humain_vs_ia(memoire: dict, plateau: tuple[int, ...]) -> None:
    """Permet à un humain d'affronter l'IA."""
    joueur:int = 1 # Vous jouez les Blancs
    termine: bool = False
    gagnant: int = 0

    # Variables pour mémoriser le dernier coup de l'IA afin d'apprendre en ligne
    dernier_coup_ia = None

    while not termine:
        # --- Initialisation ---
        qui_joue = {1: 'Humain', -1: 'IA'}
        print(f"\n>>> Joueur '{qui_joue[joueur]}' joue <<<")
        afficher_grille(plateau)
        coups_possibles = trouver_coups(joueur, plateau)
        
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
            etat = tuple(plateau)
            if etat not in memoire:
                memoire[etat] = trouver_coups(etat, coups_possibles)
            print(f"Coups possibles restants pour l'IA : {memoire[etat]}")
            coup_obj = random.choice(memoire[etat])
            # On mémorise l'état et l'objet Coup choisis par l'IA
            plateau_precedent_ia = etat
            dernier_coup_ia = coup_obj
            coup_joue = coup_obj.coup
            print(f"L'IA joue : {coup_obj}")
            plateau = coup_obj.etat_suivant
            joueur = -joueur
            termine, gagnant = est_finie(joueur, plateau)
            continue

        plateau = jouer_coup(coup_joue, tuple(plateau))
        joueur = -joueur
        termine, gagnant = est_finie(joueur, plateau)
    
    print(f"\nPartie finie ! Gagnant : {'Humain' if gagnant == 1 else 'IA'}")

    # Si l'IA a perdu, retirer le dernier coup choisi depuis la mémoire
    if gagnant == 1 and dernier_coup_ia and plateau_precedent_ia in memoire:
        print(f"L'IA a perdu. Suppression du coup {dernier_coup_ia} de l'état {plateau_precedent_ia}.")
        try:
            memoire[plateau_precedent_ia].remove(dernier_coup_ia)
        except ValueError:
            pass
        if not memoire[plateau_precedent_ia]:
            del memoire[plateau_precedent_ia]

if __name__ == "__main__":
    # L'IA apprendra au fur et à mesure des parties jouées
    Sauvegarde = "ia_data.pkl"
    ia_data: dict[tuple[int, ...], list[Coup]] = charger_memoire(Sauvegarde)
    print(f"Memoire IA a chargé {len(ia_data)} etats depuis le fichier '{Sauvegarde}'")

    jouer = True
    while jouer:
        plateau: tuple[int, ...] = (-1, -1, -1, 0, 0, 0, 1, 1, 1)
        humain_vs_ia(ia_data, plateau)
        print(f"Memoire IA a sauvegardé {len(ia_data)} etats")
        jouer = input("Voulez-vous rejouer une partie contre l'IA ? (o/n) : ").lower() == 'o'

    # Sauvegarde après la partie pour conserver l'apprentissage
    sauvegarder_memoire(Sauvegarde, ia_data)
    print(f"Memoire IA a sauvegardé {len(ia_data)} etats dans le fichier '{Sauvegarde}'")
