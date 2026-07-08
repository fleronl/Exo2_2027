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
                 coups_possibles: Coups = None) -> None:
        """ Constructeur de la classe Coup:
            __plateau attribut privé, état du plateau précédent
            __coups attribut privé, liste des coups disponibles"""
        
        self.__plateau = tuple(etat_precedent) # Etat du plateau
        self.__coups = coups_possibles # Liste de coups enfants qui seront possibles
        
    def ajouter_coups(self, coups: Coups)-> None:
        """ Ajoute une nouvelle liste de coups"""
        self.__coups = coups
        
    def obtenir_coups(self)-> Coups:
        """Donne une liste de coups possible pour un plateau donné"""
        return self.__coups
        
    def supprimer_coup(self, coup: Coup) -> None:
        """Supprime un coup de l'IA qui mène à un échec"""
        self.__coups.remove(coup)

    def __repr__(self) -> str:
        """ Affiche le plateau avec ses coups"""
        return f"({self.__plateau} -> {self.__coups})"
   
if __name__ == "__main__":

    print('Hello')
    plateau: Plateau = [-1, -1, -1, 0, 0, 0, 1, 1, 1]
    coup = Coup(plateau)
    coup.ajouter_coups([(6,3),(7,4),(8,5)])
    #coup.ajouter_coups((6,3))
    print(coup)
    coup.supprimer_coup((7,4))
    print(coup)

    
    
