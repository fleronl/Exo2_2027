# coding: utf-8

"""
    L'HexaPion (ou HexaPawn) - Version simplifiée conforme au programme de Terminale NSI.
    Un jeu d'apprentissage par essais-erreurs (apprentissage par renforcement).
"""

import os
import pickle
import random

# Constantes de jeu
DIM = 3  # Dimension fixe du plateau (3x3)
BLANC = 1
NOIR = -1
VIDE = 0

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


def convertir_indice(ligne: int, colonne: int) -> int:
    """Convertit des coordonnées (ligne, colonne) en un indice linéaire (0-8)."""
    return ligne * DIM + colonne


def convertir_coordonnees(indice: int) -> tuple[int, int]:
    """Convertit un indice linéaire (0-8) en coordonnées (ligne, colonne)."""
    return indice // DIM, indice % DIM


def afficher_grille(plateau: tuple[int, ...]) -> None:
    """Affiche de manière lisible la grille de jeu et les indices associés."""
    symboles = {BLANC: "B", VIDE: ".", NOIR: "N"}
    print("\nPlateau actuel      Positions")
    for i in range(DIM):
        debut = i * DIM
        fin = debut + DIM
        # Ligne de jeu
        ligne_jeu = " | ".join(f"{symboles[x]:>2}" for x in plateau[debut:fin])
        # Ligne d'indices d'aide
        ligne_indices = " | ".join(f"{x:>2}" for x in range(debut, fin))
        print(f"{ligne_jeu}     {ligne_indices}")


def jouer_coup(coup: Coup, plateau: tuple[int, ...]) -> tuple[int, ...]:
    """Retourne une nouvelle grille (tuple) après application du coup."""
    nouvelle_grille = list(plateau)
    nouvelle_grille[coup.arrivee] = nouvelle_grille[coup.depart]
    nouvelle_grille[coup.depart] = VIDE
    return tuple(nouvelle_grille)


def trouver_coups(joueur: int, plateau: tuple[int, ...]) -> list[Coup]:
    """Renvoie la liste des coups légaux possibles pour le joueur spécifié."""
    coups_possibles = []
    direction = -1 if joueur == BLANC else 1  # Les blancs montent (-3 en indice), les noirs descendent (+3)

    for i in range(DIM * DIM):
        if plateau[i] == joueur:
            # 1. Avancement tout droit (uniquement si la case devant est vide)
            cible_devant = i + (direction * DIM)
            if 0 <= cible_devant < DIM * DIM and plateau[cible_devant] == VIDE:
                coups_possibles.append(Coup(i, cible_devant, plateau))

            # 2. Prises diagonales (uniquement si un pion adverse s'y trouve)
            lig, col = convertir_coordonnees(i)
            for d_col in [-1, 1]:
                n_col = col + d_col
                if 0 <= n_col < DIM:
                    cible_diag = convertir_indice(lig + direction, n_col)
                    if 0 <= cible_diag < DIM * DIM and plateau[cible_diag] == -joueur:
                        coups_possibles.append(Coup(i, cible_diag, plateau))

    return coups_possibles


def est_finie(joueur_suivant: int, plateau: tuple[int, ...]) -> tuple[bool, int]:
    """Vérifie si la partie est terminée.
    Retourne (True, gagnant) ou (False, 0).
    """
    # Un pion Blanc a atteint la ligne du haut (indices 0, 1, 2)
    if BLANC in plateau[:DIM]: 
        return True, BLANC
    
    # Un pion Noir a atteint la ligne du bas (indices 6, 7, 8)
    if NOIR in plateau[(DIM-1)*DIM:]: 
        return True, NOIR
    
    # Un joueur n'a plus aucun pion
    if BLANC not in plateau: 
        return True, NOIR
    if NOIR not in plateau: 
        return True, BLANC
    
    # Le joueur suivant est bloqué (aucun coup disponible) -> l'autre gagne
    if not trouver_coups(joueur_suivant, plateau):
        return True, -joueur_suivant
        
    return False, 0


# Gestion de la mémoire de l'IA { Etat: [Liste de Coup] }
def sauvegarder_memoire(chemin: str, memoire: dict) -> None:
    """Sauvegarde la mémoire de l'IA (dictionnaire) dans un fichier."""
    try:
        with open(chemin, "wb") as f:
            pickle.dump(memoire, f)
    except Exception as e:
        print(f"Erreur de sauvegarde : {e}")


def charger_memoire(chemin: str) -> dict:
    """Charge la mémoire de l'IA depuis un fichier."""
    if not os.path.exists(chemin):
        return {}
    try:
        with open(chemin, "rb") as f:
            data = pickle.load(f)
            if isinstance(data, dict):
                return data
    except Exception as e:
        print(f"Erreur de chargement : {e}")
    return {}


def humain_vs_ia(memoire: dict, plateau: tuple[int, ...]) -> None:
    """Gère une partie de jeu entre l'Humain (Blancs) et l'IA (Noirs)."""
    joueur_actif = BLANC
    termine = False
    gagnant = 0
    
    # Suivi du dernier coup de l'IA pour l'apprentissage
    dernier_coup_ia = None

    while not termine:
        afficher_grille(plateau)
        
        if joueur_actif == BLANC:
            # --- Tour de l'Humain ---
            print("\n>>> À votre tour (Blancs) <<<")
            coups_possibles = trouver_coups(BLANC, plateau)
            print(f"Coups légaux possibles : {coups_possibles}")
            
            coup_joue = None
            while coup_joue is None:
                try:
                    dep = int(input("Indice de départ : "))
                    arr = int(input("Indice d'arrivée : "))
                    # Recherche si ce coup existe dans les coups légaux
                    for c in coups_possibles:
                        if c.depart == dep and c.arrivee == arr:
                            coup_joue = c
                            break
                    if coup_joue is None:
                        print("Coup invalide. Veuillez réessayer.")
                except ValueError:
                    print("Veuillez entrer des nombres entiers valides.")
            
            plateau = jouer_coup(coup_joue, plateau)
            
        else:
            # --- Tour de l'IA ---
            print("\n>>> Tour de l'IA (Noirs) <<<")
            
            # Si cet état de plateau est inconnu, on l'enregistre avec tous ses coups légaux
            if plateau not in memoire:
                memoire[plateau] = trouver_coups(NOIR, plateau)
            
            # L'IA choisit un coup au hasard parmi ceux restants en mémoire
            choix_disponibles = memoire[plateau]
            print(f"Coups en mémoire de l'IA pour cet état : {choix_disponibles}")
            
            coup_joue = random.choice(choix_disponibles)
            print(f"L'IA a choisi le coup : {coup_joue}")
            
            # Enregistrement du coup joué pour l'apprentissage en cas de défaite
            dernier_coup_ia = coup_joue
            
            plateau = jouer_coup(coup_joue, plateau)

        # Changement de joueur et vérification de fin de partie
        joueur_actif = -joueur_actif
        termine, gagnant = est_finie(joueur_actif, plateau)

    # Affichage du résultat final
    afficher_grille(plateau)
    if gagnant == BLANC:
        print("\nVictoire de l'Humain !")
        # Apprentissage par punition : l'IA retire le dernier coup qui l'a menée à la défaite
        if dernier_coup_ia is not None:
            etat_precedent = dernier_coup_ia.etat_precedent
            if etat_precedent in memoire:
                print(f"L'IA apprend de sa défaite : suppression du coup {dernier_coup_ia} pour l'état {etat_precedent}.")
                try:
                    memoire[etat_precedent].remove(dernier_coup_ia)
                except ValueError:
                    pass
                # Si cet état n'a plus aucun coup gagnant possible, on le nettoie
                if not memoire[etat_precedent]:
                    del memoire[etat_precedent]
    else:
        print("\nL'IA a gagné !")


if __name__ == "__main__":
    fichier_ia = "ia_data.pkl"
    ia_data = charger_memoire(fichier_ia)
    print(f"Mémoire de l'IA chargée : {len(ia_data)} états connus.")

    continuer = True
    while continuer:
        # Initialisation du plateau (3 pions noirs en haut, 3 blancs en bas)
        plateau_depart = (NOIR, NOIR, NOIR, VIDE, VIDE, VIDE, BLANC, BLANC, BLANC)
        humain_vs_ia(ia_data, plateau_depart)
        
        rejouer = input("\nVoulez-vous rejouer une partie ? (o/n) : ").strip().lower()
        continuer = (rejouer == 'o')

    # Sauvegarde des apprentissages de l'IA
    sauvegarder_memoire(fichier_ia, ia_data)
    print(f"\nMémoire de l'IA sauvegardée ({len(ia_data)} états enregistrés). À bientôt !")