# Exercice 2 (6 points)

Mise à jour de la partie 3 de l'exo 2

Cet exercice porte sur la programmation orientée objet, les arbres de décision et les principes de l’intelligence artificielle.

L'Hexapawn est un jeu de plateau miniature inventé par Martin Gardner en 1962. Il se joue sur une grille de 3 lignes et 3 colonnes avec deux joueurs disposant chacun de trois pions, initialement placés sur leur ligne de départ respective.

## Règles du jeu :

1. **Déplacement simple :** un pion peut avancer d'une case en ligne droite vers l'adversaire, à condition que la case de destination soit vide.

2. **Capture :** un pion peut "manger" un pion adverse en se déplaçant d'une case en diagonale. La case de destination doit impérativement contenir un pion adverse.

3. **Conditions de victoire :** une partie est gagnée si un joueur remplit l'une des trois conditions suivantes :
    - **Conquête :** amener un pion sur la ligne de départ de l'adversaire.
    - **Destruction :** capturer tous les pions de l'adversaire.
     - **Blocage :** l'adversaire, à son tour de jouer, ne peut effectuer aucun mouvement légal.

L'objectif de cet exercice est de modéliser le jeu en Python et de concevoir une Intelligence Artificielle (IA) capable d'apprendre de ses erreurs par un mécanisme de renforcement, en explorant l'arbre des coups possibles.

# Progression des 12 questions

## Partie A : Compréhension du jeu et représentations (Questions 1 à 3)

1. **Question 1 :** Analyse de situation. À partir d'un schéma de plateau, l'élève doit identifier si la partie est finie et quel joueur a gagné selon les trois conditions de victoire : conquête, destruction ou blocage.

2. **Question 2 :** Validation de coups. Pour une position donnée, l'élève doit lister les coups légaux possibles pour les blancs (déplacement simple ou capture en diagonale).

3. **Question 3 :** Modélisation des données. On propose de représenter la grille par une liste de listes ou une liste "aplatie" de 9 éléments. L'élève doit donner l'indice correspondant à une coordonnée précise (ligne, colonne).

## Partie B : Programmation Orientée Objet (Questions 4 à 6)

4. **Question 4 :** Constructeur de classe. Écrire la méthode __init__ d'une classe Plateau qui initialise une grille 3x3 avec les pions blancs et noirs à leurs positions de départ.

5. **Question 5 :** Méthode de déplacement. Compléter une méthode est_vide(ligne, colonne) vérifiant si une case peut recevoir un pion (nécessaire pour le déplacement simple).

6. **Question 6 :** Gestion des captures. Implémenter la logique de capture : vérifier si un pion adverse est présent sur la case diagonale cible pour autoriser la prise.

## Partie C : Intelligence Artificielle et Apprentissage (Questions 7 à 9)

7. **Question 7 :** Structure de l'IA. On introduit le concept des "boîtes d'allumettes" où chaque boîte correspond à un état du jeu. L'élève doit proposer une structure de données (type dictionnaire) associant un état de plateau à une liste de coups possibles.

8. **Question 8 :** Apprentissage par renforcement. Écrire une fonction punir_ia qui, en cas de défaite, retire le dernier coup joué de la liste des choix possibles pour cet état (mécanisme de "suppression de perle").

9. **Question 9 :** Convergence de l'algorithme. Analyser pourquoi, après un certain nombre de défaites, l'IA devient "imbattable" (principe d'élagage de l'arbre des possibles).

## Partie D : Arbres de choix et Min-Max (Questions 10 à 12)

10. **Question 10 :** Structure arborescente. On modélise le jeu par un arbre où chaque nœud est une instance de la classe Noeud. L'élève doit définir les attributs etat et fils.

10. **Question 11 :** Parcours récursif. Écrire une fonction récursive qui génère tous les états accessibles à partir d'une position donnée (création de l'arbre des coups).

12. **Question 12 :** Décision Min-Max. Appliquer un score simple aux feuilles de l'arbre (+1 pour victoire IA, -1 pour victoire humain) et expliquer comment l'IA choisit le coup optimal en remontant les scores dans l'arbre

# Introduction

L'HexaPion (ou HexaPawn) est un jeu de stratégie abstrait minimaliste inventé par Martin Gardner en 1962.

![image_e349d876](attachment:image_e349d876)

L'objectif de cet exercice est d'implémenter les règles de ce jeu et de concevoir un algorithme pour q'une IA soit capable d'apprendre par essais-erreurs pour devenir imbattable.

Sur un mini-échiquier de 3x3 cases, deux joueurs s’affrontent avec trois pions chacun, en respectant les règles classiques de déplacement et de prise des échecs.

Les règles du jeu :
- **Déplacement simple :** un pion peut avancer d'une case en ligne droite vers l'adversaire, à condition que la case de destination soit vide.

- **Capture :** un pion peut "manger" un pion adverse en se déplaçant d'une case en diagonale. La case de destination doit impérativement contenir un pion adverse.

- **Conditions de victoire :** une partie est gagnée si un joueur remplit l'une des trois conditions suivantes :

    - **Conquête :** amener un pion sur la ligne de départ de l'adversaire.
    - **Destruction :** capturer tous les pions de l'adversaire.
    - **Blocage :** l'adversaire, à son tour de jouer, ne peut effectuer aucun mouvement légal.

---
# Partie A : Compréhension et représentations

On représente la grille de jeu par un tableau (type list en Python) de 9 cases. Les cases sont numérotées de 0 à 8, de gauche à droite et de haut en bas.

Les pions blancs sont représentés par la valeur 1, les pions noirs par -1 et les cases vides par 0.

![image_2bd0ef49](attachment:image_2bd0ef49)

Figure 1 : État initial du plateau et numérotation des cases

```text
   Les indices           Les pions
    0 | 1 | 2       -1, -1, -1,  <- Noirs
   -----------       
    3 | 4 | 5        0,  0,  0,  <- Vide
   -----------
    6 | 7 | 8        1,  1,  1   <- Blancs
```

Ce plateau sera représenté pa la liste Python suivante :

```python
plateau = [-1, -1, -1, 0, 0, 0, 1, 1, 1]
```



## Question 1
À partir de la situation de la Figure 1, si le joueur Blanc déplace son pion de la case 7 vers la case 4, donnez la liste Python représentant le nouvel état du plateau.

Justifiez que ce coup est légal selon les trois règles énoncées.



#### Solution :

À partir d'un schéma de plateau, l'élève doit identifier si la partie est finie et quel joueur a gagné selon les trois conditions de victoire : conquête, destruction ou blocage.

**Nouvel état du plateau et justification de la légalité**
Nouvel état du plateau (liste Python) : [-1, -1, -1, 0, 1, 0, 1, 0, 1]

**Justification :**

Situation initiale : Le plateau est représenté par la liste [-1, -1, -1, 0, 0, 0, 1, 1, 1].

Le coup : Le joueur Blanc (valeur 1) déplace son pion de la case 7 vers la case 4.

Règle appliquée : Selon la règle du déplacement simple, un pion peut avancer d'une case en ligne droite vers l'adversaire si la case de destination est vide.

#### Barème : **0.50 points** -> 0.50 pt/réponse

## Question 2
On considère la situation suivante pour le joueur Noir représentée par la liste [0, -1, 0, 0, 1, -1, 1, 0, 0]
:
- Un pion blanc est en case 4 et 6.
- Un pion noir est en case 1 et 5.
        
Le joueur Noir peut-il gagner la partie immédiatement ?

Si oui, précisez par quelle condition de victoire et quel déplacement.

#### Solution :

Validation de coups. Pour une position donnée, l'élève doit lister les coups légaux possibles pour les noirs (déplacement simple ou capture en diagonale).

**Possibilité de victoire immédiate pour le joueur Noir**

Réponse : Oui, le joueur Noir peut gagner la partie immédiatement.

Condition de victoire et déplacement :

- Condition : La Conquête.

- Déplacement : Le pion noir situé en case 6 effectue un déplacement simple vers la case 8.

#### Barème : **0.75 points** -> 0.25 pts/réponse

## Question 3

Pour faciliter la programmation, on souhaite convertir les coordonnées de type (ligne, colonne) où ligne et colonne varient de 0 à 2 en un indice unique du tableau (de 0 à 8).

**/Optionnel/**
Pour effectuer cette conversion, l'indice 'aplati' correspont à la multipication de la coordonnée 'ligne' par le nombre de colonnes du plateau à laquelle on ajoute la coordonnée 'colonne'**/Optionnel/**

Complétez le programme en proposant une formule permettant de calculer cet indice 'aplati' à partir des coordonnées 'ligne' et 'colonne'.

```python
def convertir_indice(ligne: int, colonne: int, plateau: list) -> int:
    """Convertit ligne et colonne en indice (0-8)."""
    ...
```

**Exemple : La case en ligne 1 et en colonne 2 doit correspondre à l'indice 5**


#### Solution :

Modélisation des données. On propose de représenter la grille par une liste "aplatie" de 9 éléments. L'élève doit donner l'indice correspondant à une coordonnée précise (ligne, colonne) du plateau de jeu.


```python
def convertir_indice(ligne: int, colonne: int, plateau: list) -> int:
    """Convertit ligne et colonne en indice (0-8)."""
    return ligne * 3 + colonne    # Tj de dim = 3

plateau = [0, -1, 0, 0, 1, -1, 1, 0, 0]
ligne = 1
colonne = 2

convertir_indice(1, 2, plateau)
```




    5



#### Barème : **1 point** -> 1 pt/réponse

## Question 4

On considère la fonction `jouer_coup()` permettant de jouer un déplacement valide selon les critères de déplacement décrits plus haut.

La fonction prend pour arguments :
- une variable `coup` de type *tuple* comportant deux entiers (case de départ et case d'arrivée)
- une variable `plateau` de type *tuple* comportant les neuf cases du jeu.

La fonction retourne une nouvelle grille modifiée.

Compléter la fonction `jouer_coup()` :

```python
def jouer_coup(coup: tuple[int, int], plateau: tuple[int, ...]) -> list:
    """Retourne une nouvelle grille après le coup joué."""
    nouvelle_grille = list(plateau)
    ...
    ...
    return tuple(nouvelle_grille)
```

#### Solution


```python
def jouer_coup(coup: tuple[int, int], plateau: tuple[int, ...]) -> list:
    """Retourne une nouvelle grille après le coup joué."""
    nouvelle_grille = list(plateau)
    nouvelle_grille[coup[1]] = nouvelle_grille[coup[0]]
    nouvelle_grille[coup[0]] = 0
    return tuple(nouvelle_grille)

coup = (7, 4)
jouer_coup(coup, plateau)

```




    (0, -1, 0, 0, 0, -1, 1, 0, 0)



#### Barème : **0.50 points** -> 0.25 pts/réponse

## Question 5

Pour quelle raison la variable `nouvelle_grille` est convertie en un type *list* pour ensuite être reconvertie en un type *tuple* ?

#### Solution

Le type tuple de la variable `nouvelle_grille` est non mutable, la conversion de type de cette variable est donc obligatoire pour toute modificication de son contenu.


#### Barème : **1 point**

## Question 6

Lorsque que c'est au joueur *humain* de jouer, il faut s'assurer que le choix de son déplacment est valide en faisant parti des possibilités de déplacements sur le plateau actuel founies par la variable `coups_list` comprenant l'ensemble des tuples *coup de départ* et *coup d'arrivée*

Complétez la partie du programme qui permet de faire ce test:

```python
        if joueur == 1:
            coup_valide = False
            print(f"Coups possibles restants pour l'humain : {coups_list}")
            while not coup_valide:
                    try:        
                        dep = int(input("Indice de depart : "))
                        ...
                        ...
                        ...
                        ...
                    except AssertionError:
                        print("Coup invalide. Veuillez réessayer.")
```

#### Solution 

```python
        if joueur == 1:
            coup_valide = False
            print(f"Coups possibles restants pour l'humain : {coups_list}")
            while not coup_valide:
                    try:        
                        dep = int(input("Indice de depart : "))
                        arr = int(input("Indice d'arrivee : "))
                        coup_joue = (dep, arr)
                        assert coup_joue in coups_list
                        coup_valide = True
                    except AssertionError:
                        print("Coup invalide. Veuillez réessayer.")
```

#### Barème : **1 point** -> 0.25 pt/ligne

---
## Partie B : Programmation Orientée Objet

Dans cette partie, on utilise le paradigme de la programmation orientée objet pour modéliser les coups possibles que l'IA peut jouer à partir d'un plateau donné.

On donne la Classe Coup suivante :

```python
class Coup:
    """Représente un déplacement de pion (départ -> arrivée) et stocke l'état d'origine."""

    def __init__(self, depart: int, arrivee: int, etat_precedent: tuple[int, ...] = None):
        self.etat_precedent = etat_precedent   # On mémorise l'état du plateau avant que ce coup ne soit joué
        self.depart = depart                   # Indice de départ (0-8)
        self.arrivee = arrivee                 # Indice d'arrivée (0-8)
```

## Question 7

Donnez les attributs de la classe `Coup` ainsi que leurs types

#### Solution

- **etat_precedent :** tuple de 9 entiers
- **depart :** entier
- **arrivee :** entier

#### Barème : **0.75 points ->** 0.25 pt / réponse

## Question 8

Proposez une méthode `obtenir_coup()` de la classe `Coup` pour retourner un tuple constitué du déplacement d'un point de son point de départ vers son point d'arrivée.


#### Solution :


```python
class Coup:
    """Représente un déplacement de pion (départ -> arrivée) et stocke l'état d'origine."""

    def __init__(self, depart: int, arrivee: int, etat_precedent: tuple[int, ...] = None):
        self.etat_precedent = etat_precedent
        self.depart = depart
        self.arrivee = arrivee

    def obtenir_coup(self) -> tuple[int, int]:
        """retourne un tuple coup """
        return (self.depart, self.arrivee)

```

#### Barème : **0.75 points**

## Question 9

########################################################################
### Question 5

La méthode est_vide(ligne, colonne) renvoie True si la case désignée par ses coordonnées est libre, et False sinon. Elle utilise la formule de conversion d'indice vue à la Question 3.

Recopier et compléter le code de cette méthode.

```python
def est_vide(self, ligne, colonne):
    # Calcul de l'indice dans la liste aplatie
    ...
    if self.grille[indice] == ... :
        return True
    else:
        return False
```


```python
class Plateau:
    def __init__(self):
        self.taille = 3
        self.grille = [-1, -1, -1, 0, 0, 0, 1, 1, 1]
        self.joueur_courant = 1

    def est_vide(self, ligne, colonne):

        # Calcul de l'indice dans la liste aplatie
        indice = ligne * self.taille + colonne
        if self.grille[indice] == 0 :
            return True
        else:
            return False
        
p = Plateau()

assert p.est_vide(0, 2) == False
assert p.est_vide(1, 1) == True
```

### Question 6
Selon les règles du jeu, un pion peut capturer un pion adverse en se déplaçant d'une case en diagonale, à condition que la case de destination contienne un pion de l'adversaire.

Écrire le code de la méthode peut_manger(self, lig_arr, col_arr, valeur_adversaire) qui renvoie True si la capture est possible sur la case de destination, et False sinon.

```python
def peut_manger(self, lig_arr, col_arr, valeur_adversaire):
    """
    Vérifie si la case de destination (lig_arr, col_arr) 
    contient un pion adverse permettant la capture.
    """
    # À rédiger
```

#### Solution :


```python
class Plateau:
    def __init__(self):
        self.taille = 3
        self.grille = [-1, -1, -1, 0, 0, 0, 1, 1, 1]
        self.joueur_courant = 1
        
    def peut_manger(self, lig_arr, col_arr, valeur_adversaire):
        index_aplati = (lig_arr * self.taille) + col_arr
        if self.grille[index_aplati] == valeur_adversaire:
            return True
        else:
            return False
        
p = Plateau()

assert p.peut_manger(0, 2, -1) == True
assert p.peut_manger(1, 1, -1) == False
```

---
## Partie C : Intelligence Artificielle et Apprentissage

Dans cette partie, on modélise l'IA par un mécanisme d'apprentissage par renforcement inspiré des « boîtes d'allumettes » de Martin Gardner.

Chaque boîte représente un état du jeu et contient des jetons (ou « perles ») correspondant aux coups possibles.


### Question 7
On utilise un dictionnaire memoire_ia pour stocker la connaissance de la machine. Les clés sont les configurations du plateau (représentées par des tuples) et les valeurs sont des listes de coups possibles.

1. Donner l'instruction Python permettant de créer une entrée dans memoire_ia pour l'état initial (-1, -1, -1, 0, 0, 0, 1, 1, 1) avec les coups possibles vers les cases 3, 4 et 5.

2. Pourquoi l'emploi d'un tuple est nécessaire pour la clé du du dictionnaire ?


#### Solution :
l'état est un tuple, car une liste ne peut pas servir de clé dans un dictionnaire Python car une clé est non modifiable


```python
memoire_ia = {}
memoire_ia[(-1, -1, -1, 0, 0, 0, 1, 1, 1)] = [3, 4, 5]
```

### Question 8
Lorsqu'une partie est perdue, l'IA est « punie » : on retire de sa mémoire le dernier coup joué pour qu'elle ne le reproduise plus.

On dispose d'une liste historique contenant des tuples (etat, coup) joués par l'IA. Compléter la fonction punir_ia ci-dessous.

```python
def punir_ia(memoire_ia, historique):
    # Récupération du dernier état et du dernier coup
    dernier_etat, dernier_coup = historique[-1]
    
    # Suppression du coup fautif dans le dictionnaire
    if dernier_coup in memoire_ia[dernier_etat]:
        memoire_ia[dernier_etat].remove(...)
```

#### Solution :

Le mécanisme de « punition » consiste à retirer le coup fautif de la liste des choix pour l'état concerné.


```python
def punir_ia(memoire_ia, historique):
    # Récupération du dernier état et du dernier coup
    dernier_etat, dernier_coup = historique[-1]
    
    # Suppression du coup fautif dans le dictionnaire
    if dernier_coup in memoire_ia[dernier_etat]:
        memoire_ia[dernier_etat].remove(dernier_coup) # L'élément à retirer est le dernier_coup
```

### Question 9
L'Hexapawn est un jeu « résolu » ne comportant que 66 parties différentes.

En vous appuyant sur le principe d'élagage, expliquer pourquoi l'IA devient mathématiquement imbattable après un certain nombre de défaites.

#### Solution :

L'Hexapawn est un jeu « résolu » car le nombre de configurations et de parties possibles est fini et très limité (seulement 66 variantes).

L'IA utilise un mécanisme d'apprentissage par « punition » qui repose sur l'élagage : à chaque défaite, la machine retire définitivement de sa mémoire le coup qui a mené à l'échec. 

Comme le nombre de coups possibles par état est restreint et connu à l'avance, l'IA finit par supprimer toutes les *mauvaises branches* de son arbre de choix.

Une fois que tous les chemins menant à une défaite ont été éliminés, il ne reste dans le dictionnaire que les séquences de coups garantissant la victoire ou le blocage de l'adversaire. L'algorithme converge vers une stratégie optimale pour elle.

En fait il faut une dizaine de défaites seulement, l'IA sera imbattable (au mieux réussite par conquête, au pire réussite par blocage).



## Partie D : Arbres de choix et Min-Max

Pour anticiper les coups de l'adversaire, on modélise l'ensemble des suites de coups possibles par une structure arborescente. Chaque nœud de l'arbre représente un état du plateau.

### Question 10

On considère la classe Noeud ci-dessous.

Recopier et compléter le constructeur pour initialiser l'état du plateau (etat) et la liste des nœuds enfants (fils).

```python
class Noeud:
    def __init__(self, etat):
        self.etat = ...
        self.fils = ... # Liste de Noeud
```

#### Solution :


```python
class Noeud:
    def __init__(self, etat):
        self.etat = etat
        self.fils = [] # Liste de Noeud
```

### Question 10 bis (Niveau Moyen - Logique de jeu)

Compléter la méthode est_finie(self) de la classe Plateau qui renvoie un tuple (bool, gagnant). Elle doit vérifier les trois conditions :

- Conquête : un pion blanc est en ligne 0 (indices 0, 1, 2) ou noir en ligne 2 (indices 6, 7, 8).
- Destruction : un joueur n'a plus de pions (valeur 1 ou -1 absente de la liste).
- Blocage : le joueur dont c'est le tour n'a aucun coup légal possible.


```python
def est_finie(self, joueur_suivant):
    # 1. Conquête : un pion atteint la ligne adverse [1, 2]
    for i in range(0, 3): # Ligne 0 pour les blancs
        if self.grille[i] == 1: return (True, 1)
    for i in range(6, 9): # Ligne 2 pour les noirs
        if self.grille[i] == -1: return (True, -1)

    # 2. Destruction : un joueur n'a plus de pions [1, 2]
    if 1 not in self.grille: return (True, -1)
    if -1 not in self.grille: return (True, 1)

    # 3. Blocage : le joueur suivant ne peut plus bouger [1, 2]
    # trouver_coups_legaux renvoie la liste des coups possibles
    if len(trouver_coups_legaux(tuple(self.grille), joueur_suivant)) == 0:
        return (True, -joueur_suivant) # L'adversaire gagne

    return (False, 0)
```

### Question 11
On souhaite générer l'arbre de tous les coups possibles à partir d'un état donné.

La fonction trouver_coups_legaux(etat, joueur) renvoie la liste des états accessibles en un coup.

Compléter la fonction récursive generer_arbre(noeud_courant, joueur) qui prend en paramètre un objet Noeud et remplit son attribut fils avec les configurations suivantes.

```python
def generer_arbre(noeud_courant, joueur):
    # On récupère les configurations accessibles
    etats_suivants = trouver_coups_legaux(noeud_courant.etat, joueur)
    
    for etat in etats_suivants:
        nouveau_fils = Noeud(etat)
        noeud_courant.fils.append(...)
        # Appel récursif pour le joueur suivant (-joueur)
        generer_arbre(..., -joueur)
```

#### Solution :


```python
def generer_arbre(noeud_courant, joueur):
    # On récupère les configurations accessibles
    etats_suivants = trouver_coups_legaux(noeud_courant.etat, joueur)
    
    for etat in etats_suivants:
        nouveau_fils = Noeud(etat)
        noeud_courant.fils.append(nouveau_fils)
        # Appel récursif pour le joueur suivant (-joueur)
        generer_arbre(nouveau_fils, -joueur)
```

### Question 11 bis (Niveau Difficile - Simulation)

Écrire une fonction simuler_partie(plateau, memoire_ia) qui simule une partie complète entre l'IA (pions noirs) et un joueur aléatoire (pions blancs).

- À chaque tour de l'IA, elle choisit un coup au hasard dans memoire_ia[etat].
- Elle doit stocker le parcours dans une liste historique.
- En cas de défaite de l'IA, la fonction doit appeler punir_ia pour retirer le dernier coup.

#### Solution :

Points clés de l'algorithme :
- Historique : On stocke chaque couple (etat, coup) pour pouvoir remonter à la "mauvaise perle" en fin de partie.
- Initialisation : Si l'IA rencontre une nouvelle configuration, elle découvre et stocke tous les coups légaux possibles.
- Punition : L'apprentissage n'a lieu qu'en cas de défaite : on retire définitivement le dernier mouvement de la mémoire.


```python
def simuler_partie(plateau, memoire_ia):
    historique = []
    joueur_actuel = 1  # Les blancs commencent [3, 4]
    termine, gagnant = plateau.est_finie(joueur_actuel)

    while not termine:
        etat = tuple(plateau.grille) # Tuple requis pour servir de clé [2, 5]
        
        if joueur_actuel == 1: # Joueur aléatoire (Blancs)
            coups = trouver_coups_legaux(etat, 1)
            coup = random.choice(coups)
            plateau.jouer_coup(coup)
        else: # Intelligence Artificielle (Noirs)
            # Initialise la "boîte" si l'état est inconnu [2]
            if etat not in memoire_ia:
                memoire_ia[etat] = trouver_coups_legaux(etat, -1)
            
            # Choix d'une "perle" au hasard [6, 7]
            # On suppose que l'IA n'est pas déjà bloquée (vérifié par est_finie)
            coup = random.choice(memoire_ia[etat])
            historique.append((etat, coup)) # Mémorise pour punition éventuelle [5, 8]
            plateau.jouer_coup(coup)
        
        joueur_actuel = -joueur_actuel
        termine, gagnant = plateau.est_finie(joueur_actuel)

    # Phase d'apprentissage par punition [5, 9, 10]
    if gagnant == 1: # Si l'IA (Noirs) a perdu
        punir_ia(memoire_ia, historique)
```

### Question 12
On attribue un score aux feuilles de l'arbre : +1 si l'IA gagne, −1 si l'humain gagne.

L'algorithme Min-Max permet de faire remonter ces scores :
- Si c'est au tour de l'IA, elle choisit le coup menant au fils ayant le score maximum.
- Si c'est au tour de l'humain, on suppose qu'il joue parfaitement et choisit le fils ayant le score minimum.

Expliquer pourquoi, dans une configuration où tous les fils d'un nœud "IA" ont un score de −1, l'IA est certaine de perdre, quel que soit son choix.


#### Solution :

Si tous les fils valent −1, cela signifie que peu importe le mouvement choisi par l'IA, l'adversaire dispose d'une stratégie pour gagner (score minimal remonté). L'élagage vu en Partie C aurait consisté à supprimer ces branches dès leur identification

### Question 12 bis (Difficulté : Experte)

On considère qu'un état est une impasse si sa liste de coups possibles dans memoire_ia devient vide (suite à des punitions successives). Pour optimiser l'IA, on implémente une fonction récursive propager_perte(memoire_ia, historique). Si le dernier coup joué a conduit l'IA dans une impasse, ce coup doit être supprimé de l'état précédent dans la mémoire, et ainsi de suite.

Recopier et compléter le code récursif suivant :
```python
def propager_perte(memoire_ia, historique):
    if len(historique) == 0:
        return None  # Cas d'arrêt : plus d'historique
    
    etat_prec, coup_prec = historique.pop()
    # On supprime le coup menant à l'impasse
    if coup_prec in memoire_ia[etat_prec]:
        memoire_ia[etat_prec].remove(coup_prec)
    
    # Si l'état précédent devient lui-même une impasse
    if len(memoire_ia[etat_prec]) == ... :
        return propager_perte(..., ...) # Appel récursif
```

#### Solution

Explication de la logique :
- Dépilage : La fonction utilise historique.pop() pour remonter le temps.
- Élagage : Elle retire le coup "fautif" du dictionnaire memoire_ia.
- Récursivité : Si l'IA se rend compte qu'elle n'a plus aucune option dans un état donné (len == 0), cet état est considéré comme perdu par avance. Elle appelle alors propager_perte pour supprimer le coup qui l'a menée dans cette "impasse" dès le tour précédent


```python
def propager_perte(memoire_ia, historique):
    # Cas d'arrêt : on a remonté tout l'historique de la partie
    if len(historique) == 0:
        return None
    
    # On récupère le dernier état et le coup joué par l'IA
    etat_prec, coup_prec = historique.pop()
    
    # On supprime le coup qui a mené à l'impasse
    if coup_prec in memoire_ia[etat_prec]:
        memoire_ia[etat_prec].remove(coup_prec)
    
    # Si cette suppression rend l'état précédent vide (impasse totale),
    # on propage la perte récursivement à l'état encore avant.
    if len(memoire_ia[etat_prec]) == 0:
        return propager_perte(memoire_ia, historique)
```

---
## Version full du code



```python

```
