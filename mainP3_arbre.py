# coding: utf-8

"""
    L'HexaPion (ou HexaPawn) - Représentation sous forme d'Arbre (NSI)
    
    Ce script isole la logique nécessaire pour générer l'arbre complet 
    des parties possibles et explorer ses chemins (parcours en profondeur).
"""

# Constantes de jeu
DIM = 3  # Dimension fixe du plateau (3x3)

class Noeud:
    """
    La classe Noeud représente un état du jeu 
    - le plateau
    - le coup (case de départ et d'arrivée) qui a permis d'y parvenir.
    - Le jouerur qui a joué ce coup.
    - la liste des enfants (états suivants possibles)
    - un indicateur si c'est une feuille (partie terminée)
    - le gagnant si c'est une feuille (0 sinon)
    """
    def __init__(self, plateau: tuple[int, ...], joueur: int, depart: int = None, arrivee: int = None):
        self.plateau = plateau    # Plateau représenté par un tuple de 9 entiers (-1, 0, 1)
        self.joueur = joueur      # Joueur qui a joué le coup pour arriver à cet état (-1 pour Noir, 1 pour Blanc)
        self.depart = depart      # Indice d'origine du pion (None pour la racine)
        self.arrivee = arrivee    # Indice d'arrivée du pion (None pour la racine)
        
        self.enfants: list['Noeud'] = []   # Liste des noeuds enfants (états suivants possibles, les noeuds sont créés récursivement)
        self.est_feuille = False
        self.gagnant = 0

    def Afficher_noeud(self) -> str:
        """Représentation textuelle d'un Noeud."""
        if self.depart is not None and self.arrivee is not None:
            return f"{self.depart} -> {self.arrivee}"
        return "Racine"
    
    def Afficher_grille(self) -> None:
        """Méthode pour afficher la grille de jeu."""
        affichage = {1: "B", 0: ".", -1: "N"}
        print(f"------------")
        print(f" | ".join(f"{affichage[x]:>2}" for x in self.plateau[0:3]))
        print(f" | ".join(f"{affichage[x]:>2}" for x in self.plateau[3:6]))
        print(f" | ".join(f"{affichage[x]:>2}" for x in self.plateau[6:9]))

def convertir_indice(ligne: int, colonne: int) -> int:
    """Convertit des coordonnées (ligne, colonne) en un indice linéaire (0-8)."""
    return ligne * DIM + colonne

def convertir_coordonnees(indice: int) -> tuple[int, int]:
    """Convertit un indice linéaire (0-8) en coordonnées (ligne, colonne)."""
    return indice // DIM, indice % DIM

def jouer_coup(coup: tuple[int, int], plateau: tuple[int, ...]) -> tuple[int, ...]:
    """Retourne une nouvelle grille (tuple) après application du coup (depart, arrivee)."""
    depart, arrivee = coup
    nouvelle_grille = list(plateau)
    nouvelle_grille[arrivee] = nouvelle_grille[depart]
    nouvelle_grille[depart] = 0
    return tuple(nouvelle_grille)

def trouver_coups(joueur: int, plateau: tuple[int, ...]) -> list[tuple[int, int]]:
    """Renvoie la liste des coups (depart, arrivee) possibles pour le joueur spécifié."""
    coups_possibles = []
    direction = -1 if joueur == 1 else 1  # Les blancs (1) montent (-3 en indice), les noirs (-1) descendent (+3)

    for i in range(DIM * DIM):
        if plateau[i] == joueur:
            # 1. Avancement tout droit (uniquement si la case devant est vide)
            cible_devant = i + (direction * DIM)
            if 0 <= cible_devant < DIM * DIM and plateau[cible_devant] == 0:
                coups_possibles.append((i, cible_devant))

            # 2. Prises diagonales (uniquement si un pion adverse s'y trouve)
            lig, col = convertir_coordonnees(i)
            for d_col in [-1, 1]:
                n_col = col + d_col
                if 0 <= n_col < DIM:
                    cible_diag = convertir_indice(lig + direction, n_col)
                    if 0 <= cible_diag < DIM * DIM and plateau[cible_diag] == -joueur:
                        coups_possibles.append((i, cible_diag))

    return coups_possibles

def est_finie(joueur_suivant: int, plateau: tuple[int, ...]) -> tuple[bool, int]:
    """Vérifie si la partie est terminée.
    Retourne (True, gagnant) ou (False, 0).
    """
    # Un pion Blanc a atteint la ligne du haut (indices 0, 1, 2)
    if 1 in plateau[:DIM]: return True, 1
    # Un pion Noir a atteint la ligne du bas (indices 6, 7, 8)
    if -1 in plateau[(DIM-1)*DIM:]: return True, -1
    # Un joueur n'a plus aucun pion
    if 1 not in plateau: return True, -1
    if -1 not in plateau: return True, 1
    # Le joueur suivant est bloqué (aucun coup disponible) -> l'autre gagne
    if not trouver_coups(joueur_suivant, plateau):
        return True, -joueur_suivant
        
    return False, 0

def construire_arbre(plateau: tuple[int, ...], joueur: int, depart: int = None, arrivee: int = None, niveau: int = 0) -> Noeud:
    """
    Construit l'arbre complet des configurations possibles par récursivité.
    (Illustration du parcours en profondeur).
    """
    noeud = Noeud(plateau, joueur, depart, arrivee)
    
    # 1. Cas de base (Condition d'arrêt)
    termine, gagnant = est_finie(joueur, plateau)
    if termine:
        noeud.est_feuille = True
        noeud.gagnant = gagnant
        noeud.Afficher_grille()
        print(f"Niveau {niveau} - Joueur {'Blancs' if joueur == 1 else 'Noirs'} - Gagnant : {'Blancs' if gagnant == 1 else 'Noirs' if gagnant == -1 else 'Aucun'}")
        return noeud
        
    # 2. Cas récursif
    coups_possibles = trouver_coups(joueur, plateau)
    for coup in coups_possibles:
        nouveau_plateau = jouer_coup(coup, plateau)
        # Appel récursif en passant la main à l'adversaire et en mémorisant le coup
        enfant = construire_arbre(nouveau_plateau, -joueur, coup[0], coup[1], niveau + 1)
        # On relie le noeud courant à son enfant
        noeud.enfants.append(enfant)

    if niveau < 2:  # Affiche la racine et le plateau initial
        noeud.Afficher_grille()
        print(f"Niveau {niveau} - Joueur {'Blancs' if joueur == 1 else 'Noirs'}")
        print(f"{'##################################################' if niveau == 1 else ''}")
    return noeud

def parcours_largeur(noeud: Noeud) -> None:
    """
    Parcours en largeur de l'arbre (NSI : File / FIFO).
    Affiche les noeuds par niveau.
    """
    
    file = [noeud]
    niveau = 0
    
    while file:
        taille_niveau = len(file)
        print(f"\n>>>      Niveau {niveau}        <<<")
        
        for _ in range(taille_niveau):
            courant = file.pop(0)
            print(f"  Noeud : {courant.Afficher_noeud()}")
            courant.Afficher_grille()
            file.extend(courant.enfants)
        
        niveau += 1

def taille_arbre_iterative(racine: Noeud) -> int:
    # On utilise une pile (liste Python) pour stocker les noeuds à visiter
    pile = [racine]
    compteur = 0
    
    while pile:
        # On extrait le dernier noeud ajouté (LIFO)
        noeud_courant = pile.pop()
        compteur += 1
        
        # On ajoute tous les enfants du noeud actuel à la pile pour traitement futur
        for enfant in noeud_courant.enfants:
            pile.append(enfant)
            
    return compteur

def taille_arbre(noeud: Noeud) -> int:
    """
    Calcule le nombre total de noeuds (états de jeu) dans l'arbre.
    """
    if noeud.est_feuille:
        return 1
        
    taille = 1 # On compte le noeud courant
    for enfant in noeud.enfants:
        taille += taille_arbre(enfant)
    return taille

def calculer_toutes_parties(plateau, joueur):
    # Condition d'arrêt : si la partie est finie, on a trouvé 1 chemin complet
    fini, gagnant = est_finie(joueur, plateau)
    if fini:
        return 1
    
    total_chemins = 0
    coups = trouver_coups(joueur, plateau)
    
    for coup in coups:
        nouveau_plateau = jouer_coup(coup, plateau)
        # Exploration récursive pour compter les feuilles de l'arbre
        total_chemins += calculer_toutes_parties(nouveau_plateau, -joueur)
        
    return total_chemins

if __name__ == "__main__":
    plateau_depart = (-1, -1, -1, 0, 0, 0, 1, 1, 1)
    print("Construction de l'arbre en cours...")
    
    # 1. Création de la racine et génération de l'arbre (les Blancs (1) commencent)
    racine_jeu = construire_arbre(plateau_depart, 1)
    
    # 2. Parcours en largeur pour visualiser l'arbre (optionnel)
    parcours_largeur(racine_jeu)
 
    # 2. Manipulation 1 : Compter le nombre d'états
    nb_noeuds = taille_arbre(racine_jeu)
    print(f"L'arbre de jeu complet contient {nb_noeuds} états (noeuds) possibles.")
    nb_noeuds2 = taille_arbre_iterative(racine_jeu)
    print(f"VERION 2 de jeu complet contient {nb_noeuds2} états (noeuds) possibles.")
    
    joueur = 1  # Les Blancs commencent
    total_parties = calculer_toutes_parties(plateau_depart, joueur)
    print(f"Nombre total de parties possibles : {total_parties}")
    
