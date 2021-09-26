from typing import Iterable, Union, Any

import numpy as np
import matplotlib.pyplot as plt

# Application de la discrétisation à pas constant à l'équation de la chaleur unidimensionnelle (spatiale)
#
# Soit f une fonction de classe C1 sur le segment [0,1] à valeurs dans IR. On cherche une fonction u telle que :
#           { -u''(x) = f(x)
#           { u(0) = u(1) = 0
#
# On divise l'intervalle [0,1] en n+1 intervalles de même longueur h (= 1/(n+1)), ce qui produit n points
# intérieurs à l'intervalle. Les positions de ces points sont les x_i = i*h, i entier variant de 1 à n.
# Pour chacun de ces points, on cherche à approximer la valeur de la fonction u recherchée (on cherche donc une
# valeur approchée des u(x_i), désormais notés u_i).
# Par l'application d'un développement de Taylor-Lagrange à u aux points x_(i+1) et x_(i-1), on obtient un
# système linéaire de n équations à n inconnues (les inconnues étant les u_i) en laissant de coté un terme d'erreur,
# ce terme d'erreur étant négligeable lorsque h devient petit, et donc lorsque n devient grand.
#
# La matrice A ci-dessous est la matrice de ce système linéaire.
# Le vecteur B correspond aux valeurs de f en les points intérieurs x_i.


class ModeInterface:
    step_nb = 100

    def u(self, x) -> float:
        pass

    def vect(self, nb_pt_inte: int) -> list:
        pass

    def interval(self):
        return np.linspace(0., 1., self.step_nb + 1)

    def sanitize(self, x: Any) -> Any:
        if isinstance(x, list):
            x = np.asarray(x)
        return x


class CorrespondanceParfaite(ModeInterface):
    # Solution de -u''(x) = 1, u(0) = u(1) = 0
    def u(self, x) -> float:
        x = self.sanitize(x)
        return 1./2 * x * (1-x)

    # Vecteur des f_i
    def vect(self, nb_pt_inte: int) -> list:
        return [1. for _ in range(nb_pt_inte)]


class CorrespondanceApproximative(ModeInterface):
    # Solution de -u''(x) = Pi**2 * sin(Pi*x) , u(0) = u(1) = 0
    def u(self, x: Union[float, Iterable]) -> Any:
        x = self.sanitize(x)
        return np.sin(np.pi * x)

    # Vecteur des f_i
    def vect(self, nb_pt_inte: int) -> list:
        return [np.pi**2 * np.sin(np.pi * j / (nb_pt_inte+1)) for j in range(1, nb_pt_inte+1)]


# VARIABLES UTILISATEUR

MODE: ModeInterface = CorrespondanceApproximative()  # Choix de f parmi les classes ci-dessus
n = 100  # Nombre de points intérieurs à l'intervalle

# FIN

h = 1./(n+1)

A = [[0. for _ in range(n)] for _ in range(n)]
for i in range(n):
    A[i][i] = 2./h**2

for i in range(n-1):
    A[i][i+1] = -1./h**2
    A[i+1][i] = -1./h**2

# On pose les valeurs de la fonction f en les x_i.
B = MODE.vect(n)

# Résolution de l'équation matricielle : AX = B, d'inconnue X (le vecteur de composantes les u_i).
X = np.linalg.solve(A, B)

# Préparation de l'affichage graphique
x_i = [i * h for i in range(1, n+1)]  # Positions des points à l'intérieur de l'intervalle

it = MODE.interval()  # Récupération d'un intervalle potentiellement plus fin pour la solution exacte

plt.plot(x_i, X, 'r.', it, MODE.u(it), 'b-')
plt.xlabel('Position')
plt.ylabel('Value of u')
plt.show()
