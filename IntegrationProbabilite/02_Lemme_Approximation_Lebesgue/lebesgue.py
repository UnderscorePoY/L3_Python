import numpy as np
from typing import Callable
import matplotlib.pyplot as plt


def fonction_lebesgue(fn: Callable, n: int, x_min=-1., x_max=1.):
    """
    Construit une "fonction étagée" approximant une fonction `fn` à valeurs positives, pour une ordonnée maximale `n`.
    La construction se restreint à un intervalle [`a`,`b`] (l'intervalle [-10,10] par défaut).
    """

    NUM_POINTS_PAR_UNITE = 1_000

    num_points = int((x_max - x_min) * NUM_POINTS_PAR_UNITE)
    x_s = np.linspace(start=x_min, stop=x_max, num=num_points, endpoint=False)
    fn_valeurs = fn(x_s)

    fn_etagee_vals = [0. for _ in range(num_points)]

    for i in range(num_points):
        val = fn_valeurs[i]
        if val < 0:
            raise ValueError("La fonction ne doit retourner que des valeurs positives ou nulles.")

        if val >= n:
            etage = n
        else:
            k = int(val * 2**n)
            etage = k / 2. ** n

        fn_etagee_vals[i] = etage

    return x_s, fn_etagee_vals


def plot_lemme_approximation(fn: Callable, max_n: int, a: float, b: float):
    """
    Affiche dans un graphique unique le graphe de la fonction `fn` ainsi ceux de plusieurs fonctions étagées de Lebesgue
    uniformément réparties entre n=1 et n=`max_n`.
    """

    # Gestion des couleurs des graphes et choix des indices des courbes à tracer
    plt_couleurs = ['g', 'r', 'c', 'm', 'y', 'k']
    nb_clrs = len(plt_couleurs)
    i_a_afficher = range(max_n, 1, -(max_n//nb_clrs + 1))

    x_s = []
    fn_etagee_vals = [None for _ in range(max_n + 1)]

    for i in i_a_afficher:
        # Génération de la fonction étagée de Lebesgue pour n=i
        x_s, fn_etagee_vals[i] = fonction_lebesgue(fn=fn, n=i, x_min=a, x_max=b)

        # Récupération de la couleur et traçage
        clr = plt_couleurs[(i * nb_clrs - 1)//max_n]
        plt.plot(x_s, fn_etagee_vals[i], clr)

    plt.plot(x_s, fn(x_s), 'b')
    plt.show()
