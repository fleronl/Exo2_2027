import HexaPOOV2

import random
from typing import List, Tuple, Dict, Optional

print('Hello')
plateau = [-1, -1, -1, 0, 0, 0, 1, 1, 1]
coup = HexaPOOV2.Coup(plateau)
coup.ajouter_coups([(6,3),(7,4),(8,5)])
#coup.ajouter_coups((6,3))
print(coup)
coup.supprimer_coup((7,4))
print(coup)
