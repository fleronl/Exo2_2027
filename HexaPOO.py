# coding: utf-8

"""
    L'HexaPion (ou HexaPawn) est un jeu de stratégie abstrait minimaliste inventé par Martin Gardner en 1962.
    Sur un mini-échiquier de $3 \times 3$ cases, deux joueurs s’affrontent avec trois pions chacun, en respectant les règles classiques de déplacement et de prise des échecs.
    L'objectif de cet exercice est d'implémenter les règles de ce jeu et de concevoir un algorithme capable d'apprendre par essais-erreurs pour devenir imbattable.

    Modélise le plateau de jeu Hexapawn 3x3.
"""
from typing import List, Tuple, Dict, Optional

Plateau = Tuple[int, int, int, int, int, int, int, int, int]
Coup = Tuple[int, int]
Coups = List[Coup]
    
class Coup:
    """ Classe représentant un coup dans le jeu Hexapawn"""
        
    def __init__(self,
                 etat_precedent: Plateau, 
                 coups_possibles: Coups|None) -> None:
        """ Constructeur de la classe Coup:
            __plateau attribut privé, état du plateau précédent
            __coups attribut privé, liste des coups disponibles"""
        
        self.__plateau = tuple(etat_precedent) # Etat du plateau avant de jouer ce coup
        self.__coups = coups_possibles # Liste de coups enfants qui sont possibles
        
    def ajouter_coups(self, coups: Coups)-> None:
        """ Ajoute une liste de coups - A SUPP !"""
        self.__coups.append(coups)
        
    def obtenir_coups(self)-> Coups:
        """Donne une liste de coups possible pour un plateau donné"""
        return self.__coups
        
    def supprimer_coup(self, coup: Coup) -> None:
        """Supprime un coup de l'IA qui mène à un échec"""
        self.__coups.remove(coup)

    def __repr__(self) -> str:
        """ Affiche le plateau avec ses coups"""
        return f"({self.__plateau} -> {self.__coups})"
   
  
############## Classe Plateau ##############
    
class Plateau:
    """ Représente le plateau du jeu Hexapawn
        Type personnalisé pour la configuration du plateau (9 entiers) """
    
    def __init__(self):
        self.__plateau = [-1, -1, -1, 0, 0, 0, 1, 1, 1]
        self.__dimension = int(len(self.__plateau) ** 0.5)
        
    def modifier_plateau(self, plateau: Plateau):
        """ Modifie le plateau actuel"""
        self.plateau = plateau
        ...

    def convertir_indice(self, ligne: int, colonne: int) -> int:
        """Convertit ligne et colonne en indice (0-8)."""
        return ligne * self.__dimension + colonne

    def convertir_tableau(self, i: int) -> tuple[int, int]:
        """Convertit l'indice en ligne, colonne (0, 2)."""
        lig, col = i // self.__dimension, i % self.__dimension
        return (lig, col)

    def afficher_grille(self, grille_aplatie: Plateau) -> None:
        """Affiche la grille de jeu."""
        affichage: dict = {1: "B", 0: ".", -1: "N"}
        print(f"\nPlateau actuel  Les positions")
        print(" | ".join(f"{affichage[x]:>2}" for x in self.__plateau[0:3]) + "     0 |  1 |  2")
        print(" | ".join(f"{affichage[x]:>2}" for x in self.__plateau[3:6]) + "     3 |  4 |  5")
        print(" | ".join(f"{affichage[x]:>2}" for x in self.__plateau[6:9]) + "     6 |  7 |  8")

    def jouer_coup(self, coup: tuple[int, int], *grille_aplatie:Plateau) -> None:
        """Met à jour la grille avec le coup joué."""
        dep, arr = coup
        grille_aplatie[arr] = grille_aplatie[dep]
        grille_aplatie[dep] = 0
    
        return grille_aplatie

    def trouver_coups(self, joueur: int) -> list[Coup]:
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

    def est_finie(self, joueur_suivant: int) -> tuple[bool, int]:
        """Vérifie la fin de partie (bool, gagnant)."""
        if 1 in grille_aplatie[:3]: return True, 1     # Les Blancs ont atteint la première ligne
        if 1 not in grille_aplatie: return True, -1    # Les Blancs n'ont plus de pions
        if -1 in grille_aplatie[6:]: return True, -1   # Les Noirs ont atteint la dernière ligne
        if -1 not in grille_aplatie: return True, 1    # Les Noirs n'ont plus de pions
        if not trouver_coups(joueur_suivant):  # Aucun coup possible pour le joueur suivant
            return True, -joueur_suivant
        return False, 0

if __name__ == "__main__":

    print('Hello')
    plateau: Plateau = [-1, -1, -1, 0, 0, 0, 1, 1, 1]
    coup = Coup(plateau, [(6,3),(7,4),(8,5)])
    #coup.ajouter_coups([(6,3),(7,4),(8,5)])
    print(coup)
    coup.supprimer_coup((7,4))
    print(coup)

    
    
