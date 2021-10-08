#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 09:31:49 2021

@author: thomas.bescond
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Callable, Any


def methode_newton(f: Callable, f_prime: Callable, x0: float, tol: float) -> tuple[float, int, list]:
    """
    Applique la méthode de Newton à la résolution de l'équation f(x) = 0, pour un point `x0` proche de la solution
    recherchée.
    La procédure nécessite les valeurs de la dérivée de `f`.
    Renvoie l'abscisse approximée du zéro de f à une tolérance `tol` près, le nombre d'itérations et les points de
    construction graphique.

    Procédure : x(i+1) = x(i) - f(x(i)) / f'(x(i))
    """

    drawing_points = [(x0, 0)]  # Point de départ de la méthode

    x, y = etape_Newton(f, f_prime, x0)

    n = 0  # Compteur d'itérations
    while abs(y - x) > tol:
        drawing_points.append((x, f(x)))  # Point sur la courbe

        x, y = etape_Newton(f, f_prime, y)
        drawing_points.append((x, 0))  # Point projeté par la tangente

        n += 1

    return y, n, drawing_points


def etape_Newton(f: Callable, f_prime: Callable, y: float) -> tuple[float, float]:
    """Encapsule une étape de l'itération de la méthode de Newton."""
    return y, y - f(y) / f_prime(y)


# Fonction de visualisation des itérations de l'algorithme de Newton
def plot_newton(f: Callable, drawing_points: list, x_start=0., x_end=20.) -> None:
    """
    Affiche un graphique contenant la fonction de l'équation f(x) = 0, ainsi que les points de construction de la
    méthode de Newton.
    Les paramètres optionnels `x_start` et `x_end` permettent de sélectionner des valeurs d'abscisses personnalisées.
    """

    # Crée une liste de nombres uniformément répartis. Utilisé pour les abscisses des divers points à tracer.
    x_vals = np.linspace(start=x_start, stop=x_end, num=10 ** 4, endpoint=False)

    # Initialisation du graphique
    _, ax = plt.subplots()
    ax.plot(x_vals, f(x_vals), 'b')
    # ax.set_aspect('equal')
    ax.grid(True, which='both')
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')

    # Traçage des points de constructions de la méthode de Newton.
    for i in range(1, len(drawing_points) - 1):
        x_a, y_a = drawing_points[i - 1]
        x_b, y_b = drawing_points[i]
        ax.plot([x_a, x_b], [y_a, y_b], 'r')

        x_a, y_a = drawing_points[i]
        x_b, y_b = drawing_points[i + 1]
        ax.plot([x_a, x_b], [y_a, y_b], 'r')

    # Affichage du graphique terminé.
    plt.show()


# Transformations des fonctions dont on cherche des points fixes, en fonctions dont on cherche les zéros : f(x) = 0
def f_to_zero(f: Callable) -> Any:
    return lambda x: x - f(x)


def f_prime_to_zero(f_prime: Callable) -> Any:
    return lambda x: 1 - f_prime(x)


# Fonctions de test dont on cherche les points fixes.
# Pour appliquer la méthode de Newton, chaque fonction renseignée doit être fournie avec sa dérivée.
f1 = lambda x: x ** 2  # valeur attendue avec la méthode de Newton avec x0 = 20 : 1.0 en 9 itérations.
f1_prime = lambda x: 2 * x

f2 = lambda x: np.exp(x / 5.)  # valeur attendue avec la méthode de Newton avec x0 = 20 : 12.713206... en 6 itérations.
f2_prime = lambda x: 1 / 5. * np.exp(x / 5.)


# Variables utilisateur
X0 = 20  # point de départ (abscisse approximative du point fixe)
TOL = 10 ** -8  # tolérance à l'erreur
FUNCTION = f1
FUNCTION_PRIME = f1_prime

# "Début" du script
sol, nb_iter, segments = methode_newton(f_to_zero(FUNCTION), f_prime_to_zero(FUNCTION_PRIME), X0, TOL)

print(sol, nb_iter)
plot_newton(f_to_zero(FUNCTION), segments, x_start=0., x_end=20.)
