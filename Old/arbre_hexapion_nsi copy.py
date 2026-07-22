# coding: utf-8

"""
    L'HexaPion (ou HexaPawn) - Représentation sous forme d'Arbre (NSI)
    
    Ce script isole la logique nécessaire pour générer l'arbre complet 
    des parties possibles et explorer ses chemins (parcours en profondeur).
"""

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


# =================================================================
# FONCTIONS DE LOGIQUE DE JEU (Nécessaires pour construire l'arbre)
# =================================================================

def convertir_indice(ligne: int, colonne: int) -> int:
    """Convertit des coordonnées (ligne, colonne) en un indice linéaire (0-8)."""
    return ligne * DIM + colonne

def convertir_coordonnees(indice: int) -> tuple[int, int]:
    """Convertit un indice linéaire (0-8) en coordonnées (ligne, colonne)."""
    return indice // DIM, indice % DIM

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


# =================================================================
# REPRÉSENTATION ET MANIPULATION DE L'ARBRE (NSI)
# =================================================================

class Noeud:
    """
    Structure d'Arbre pour représenter les états de jeu.
    Chaque noeud contient un état du plateau et la liste de ses enfants.
    """
    def __init__(self, plateau: tuple[int, ...], joueur: int):
        self.plateau = plateau
        self.joueur = joueur
        # Liste contenant des tuples : (Coup_joué, Noeud_suivant)
        self.enfants: list[tuple[Coup, 'Noeud']] = []
        self.est_feuille = False
        self.gagnant = 0

def construire_arbre(plateau: tuple[int, ...], joueur: int) -> Noeud:
    """
    Construit l'arbre complet des configurations possibles par récursivité.
    (Illustration du parcours en profondeur).
    """
    noeud = Noeud(plateau, joueur)
    
    # 1. Cas de base (Condition d'arrêt)
    termine, gagnant = est_finie(joueur, plateau)
    if termine:
        noeud.est_feuille = True
        noeud.gagnant = gagnant
        return noeud
        
    # 2. Cas récursif
    coups_possibles = trouver_coups(joueur, plateau)
    for coup in coups_possibles:
        nouveau_plateau = jouer_coup(coup, plateau)
        # Appel récursif en passant la main à l'adversaire
        enfant = construire_arbre(nouveau_plateau, -joueur)
        # On relie le noeud courant à son enfant via le coup joué
        noeud.enfants.append((coup, enfant))
        
    return noeud

def taille_arbre(noeud: Noeud) -> int:
    """
    Calcule le nombre total de noeuds (états de jeu) dans l'arbre.
    """
    if noeud.est_feuille:
        return 1
        
    taille = 1 # On compte le noeud courant
    for _, enfant in noeud.enfants:
        taille += taille_arbre(enfant)
    return taille

def chemins_gagnants(noeud: Noeud, joueur_cible: int, chemin_actuel: list[Coup] = None) -> list[list[Coup]]:
    """
    Parcours l'arbre pour trouver tous les chemins menant à une victoire d'un joueur.
    (Concept NSI : Recherche de chemins / Backtracking).
    """
    if chemin_actuel is None:
        chemin_actuel = []
        
    chemins_trouves = []
    
    if noeud.est_feuille:
        if noeud.gagnant == joueur_cible:
            # On ajoute une copie du chemin gagnant
            chemins_trouves.append(list(chemin_actuel))
        return chemins_trouves
        
    for coup, enfant in noeud.enfants:
        chemin_actuel.append(coup) # On avance
        chemins_trouves.extend(chemins_gagnants(enfant, joueur_cible, chemin_actuel))
        chemin_actuel.pop() # Backtracking (on recule pour tester une autre branche)
        
    return chemins_trouves


if __name__ == "__main__":
    # Initialisation du plateau de base (3 pions noirs en haut, 3 blancs en bas)
    plateau_depart = (NOIR, NOIR, NOIR, VIDE, VIDE, VIDE, BLANC, BLANC, BLANC)
    
    print("Construction de l'arbre en cours...")
    
    # 1. Création de la racine et génération de l'arbre (les Blancs commencent)
    racine_jeu = construire_arbre(plateau_depart, BLANC)
    
    # 2. Manipulation 1 : Compter le nombre d'états
    nb_noeuds = taille_arbre(racine_jeu)
    print(f"L'arbre de jeu complet contient {nb_noeuds} états (noeuds) possibles.")
    
    # 3. Manipulation 2 : Trouver tous les chemins victorieux pour les Blancs
    victoires_blancs = chemins_gagnants(racine_jeu, BLANC)
    print(f"Il existe {len(victoires_blancs)} séquences (chemins) menant à une victoire des Blancs.")
    
    # Bonus : Afficher la première séquence gagnante trouvée
    if victoires_blancs:
        print("\nExemple de séquence gagnante pour les Blancs :")
        for i, coup in enumerate(victoires_blancs[0], 1):
            joueur_str = "Blancs" if i % 2 != 0 else "Noirs"
            print(f"  Tour {i} ({joueur_str}) : Déplacement du pion {coup.depart} vers {coup.arrivee}")