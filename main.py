"""Modélise le plateau de jeu Hexapawn 3x3."""

class Coup:
    """Représente un coup dans le jeu Hexapawn."""
    def __init__(self, depart: int, arrivee: int) -> None:
        self.depart = depart
        self.arrivee = arrivee

    def ajouter_coup(self, depart: int, arrivee: int) -> None:
        """Ajoute un coup à la liste des coups possibles."""
        self.depart = depart
        self.arrivee = arrivee

# Grille aplatie : -1 (Noir/IA), 1 (Blanc/Humain), 0 (Vide)
grille: list[int] = [-1, -1, -1, 0, 0, 0, 1, 1, 1]

def convertir_indice(ligne: int, colonne: int) -> int:
    """Convertit ligne et colonne en indice (0-8)."""
    return ligne * 3 + colonne

def convertir_tableau(i: int) -> tuple[int, int]:
    """Convertit l'indice en ligne, colonne (0, 2)."""
    lig, col = i // 3, i % 3
    return (lig, col)

def afficher_grille() -> None:
    """Affiche la grille de jeu."""
    print(f"\nPlateau actuel   Les positions")
    print(" | ".join(f"{x:>2}" for x in grille[0:3]) + "     0 |  1 |  2")
    print(" | ".join(f"{x:>2}" for x in grille[3:6]) + "     3 |  4 |  5")
    print(" | ".join(f"{x:>2}" for x in grille[6:9]) + "     6 |  7 |  8")

def jouer_coup(coup: Coup) -> None:
    """Met à jour la grille avec le coup joué."""
    dep, arr = coup.depart, coup.arrivee
    grille[arr] = grille[dep]
    grille[dep] = 0

def trouver_coups_legaux(joueur: int) -> list[Coup]:
    """Renvoie les coups possibles pour le joueur spécifié."""
    coups: list[Coup] = []
    direction: int = -1 if joueur == 1 else 1 
    etat_actuel = tuple(grille)

    for i in range(9):
        if grille[i] == joueur:

            # Déplacement simple vers l'avant
            cible: int = i + (direction * 3)
            if 0 <= cible < 9 and grille[cible] == 0:
                coups.append((i, cible, etat_actuel))
                
            lig, col = convertir_tableau(i)
            # Captures diagonales
            for d_col in [-1, 1]:
                n_col: int = col + d_col
                if 0 <= n_col <= 2:
                    cible_cap: int = convertir_indice(lig + direction, n_col)
                    if 0 <= cible_cap < 9 and grille[cible_cap] == -joueur:
                        coups.append(Coup(i, cible_cap, etat_avant=etat_actuel))
        
    return coups



if __name__ == "__main__":
    # --- Initialisation ---
    afficher_grille()
