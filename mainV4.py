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
from typing import List, Tuple, Dict, Optional

Plateau = Tuple[int, int, int, int, int, int, int, int, int]
Deplace = Tuple[int, int]
Coups = List[Deplace]
    
class Coup:
    """Classe représentant un coup et les états associés pour l'IA."""
        
    def __init__(self,
                 etat_precedent: Plateau,
                 coup: Deplace,
                 etat_suivant: Plateau,
                 coups_possibles: Optional[Coups] = None) -> None:
        
        self.__etat_precedent = tuple(etat_precedent)
        self.__coup = coup
        self.__etat_suivant = tuple(etat_suivant)
        self.__coups = coups_possibles or []
        
    @property
    def etat_precedent(self) -> Plateau:
        return self.__etat_precedent

    @property
    def coup(self) -> Deplace:
        return self.__coup

    @property
    def etat_suivant(self) -> Plateau:
        return self.__etat_suivant

    @property
    def coups_possibles(self) -> Coups:
        return self.__coups
        
    def supprimer_coup(self, coup: Deplace) -> None:
        """Supprime un coup de l'IA qui mène à un échec"""
        self.__coups.remove(coup)

    def __repr__(self) -> str:
        """ Méthode de représentation de l'objet Coup pour l'affichage. """
        return f"{self.__coup} -> {self.__etat_suivant}"

#################################
    
def convertir_indice(ligne: int, colonne: int, plateau: Plateau) -> int:
    """Convertit ligne et colonne en indice (0-8)."""
    dim_plateau = int(pow(len(plateau), 0.5))    # Tj de dim = 3
    return ligne * dim_plateau + colonne

def convertir_tableau(i: int, plateau: Plateau) -> tuple[int, int]:
    """Convertit l'indice en ligne, colonne (0, 2)."""
    dim_plateau = int(pow(len(plateau), 0.5))
    lig, col = i // dim_plateau, i % dim_plateau
    return (lig, col)

def afficher_grille(plateau: Plateau) -> None:
    """Affiche la grille de jeu."""
    affichage = {1: "B", 0: ".", -1: "N"}
    print(f"\nPlateau actuel  Les positions")
    print(" | ".join(f"{affichage[x]:>2}" for x in plateau[0:3]) + "     0 |  1 |  2")
    print(" | ".join(f"{affichage[x]:>2}" for x in plateau[3:6]) + "     3 |  4 |  5")
    print(" | ".join(f"{affichage[x]:>2}" for x in plateau[6:9]) + "     6 |  7 |  8")

def jouer_coup(coup: Deplace, plateau: Plateau) -> Plateau:
    """Retourne un nouveau plateau après le coup joué."""
    dep, arr = coup
    nouvelle_grille = list(plateau)
    nouvelle_grille[arr] = nouvelle_grille[dep]
    nouvelle_grille[dep] = 0

    return tuple(nouvelle_grille)

def trouver_coups(joueur: int, etat_actuel: Plateau) -> Coups:
    """Renvoie les coups possibles pour le joueur spécifié."""
    coups: Coups = []
    direction: int = -1 if joueur == 1 else 1

    for i in range(9):
        if etat_actuel[i] == joueur:
            cible: int = i + (direction * 3)
            if 0 <= cible < 9 and etat_actuel[cible] == 0:
                coups.append((i, cible))

            lig, col = convertir_tableau(i, etat_actuel)
            for d_col in [-1, 1]:
                n_col: int = col + d_col
                if 0 <= n_col <= 2:
                    cible_cap: int = convertir_indice(lig + direction, n_col, etat_actuel)
                    if 0 <= cible_cap < 9 and etat_actuel[cible_cap] == -joueur:
                        coups.append((i, cible_cap))

    return coups

def construire_coups_ia(etat_actuel: Plateau, coups_possibles: Coups) -> list[Coup]:
    """Construit la liste d'objets Coup pour la mémoire de l'IA."""
    coups_ia: list[Coup] = []
    for coup in coups_possibles:
        etat_suivant = jouer_coup(coup, etat_actuel)
        coups_ia.append(Coup(etat_actuel, coup, etat_suivant))
    return coups_ia

def est_finie(joueur_suivant: int, plateau: Plateau) -> tuple[bool, int]:
    """Vérifie la fin de partie (bool, gagnant)."""
    if 1 in plateau[:3]: return True, 1     # Les Blancs ont atteint la première ligne
    if 1 not in plateau: return True, -1    # Les Blancs n'ont plus de pions
    if -1 in plateau[6:]: return True, -1   # Les Noirs ont atteint la dernière ligne
    if -1 not in plateau: return True, 1    # Les Noirs n'ont plus de pions
    if not trouver_coups(joueur_suivant, plateau):  # Aucun coup possible pour le joueur suivant
        return True, -joueur_suivant
    return False, 0

# Type pour la mémoire de l'IA {Etat: [Liste d'objets Coup]}
MemoireIA = dict[Plateau, list[Coup]]

def sauvegarder_memoire(chemin: str, memoire: MemoireIA) -> None:
    """Sauvegarde la mémoire de l'IA sur disque (pickle)."""
    try:
        with open(chemin, "wb") as f:
            pickle.dump(memoire, f)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde de la memoire: {e}")

def charger_memoire(chemin: str) -> MemoireIA:
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
    
def humain_vs_ia(memoire: MemoireIA, plateau: Plateau) -> None:
    """Permet à un humain d'affronter l'IA."""
    joueur:int = 1 # Vous jouez les Blancs
    termine: bool = False
    gagnant: int = 0
    # Variables pour mémoriser le dernier coup de l'IA afin d'apprendre en ligne
    plateau_precedent_ia: Optional[Plateau] = None
    dernier_coup_ia: Optional[Coup] = None

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
                memoire[etat] = construire_coups_ia(etat, coups_possibles)
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
    ia_data: MemoireIA = charger_memoire(Sauvegarde)
    print(f"Memoire IA a chargé {len(ia_data)} etats depuis le fichier '{Sauvegarde}'")

    jouer = True
    while jouer:
        plateau: Plateau = (-1, -1, -1, 0, 0, 0, 1, 1, 1)
        humain_vs_ia(ia_data, plateau)
        print(f"Memoire IA a sauvegardé {len(ia_data)} etats")
        jouer = input("Voulez-vous rejouer une partie contre l'IA ? (o/n) : ").lower() == 'o'

    # Sauvegarde après la partie pour conserver l'apprentissage
    sauvegarder_memoire(Sauvegarde, ia_data)
    print(f"Memoire IA a sauvegardé {len(ia_data)} etats dans le fichier '{Sauvegarde}'")
