import numpy as np
from typing import Callable
import matplotlib.pyplot as plt


def f1(x: float) -> float:
    return 1./1000 * (x + 4)*(x + 1)*(x - 2)*(x - 5) + 1


def f2(x: float) -> float:
    return 2 * np.log(1+abs(x))*np.exp(-x/50)


def fonction_lebesgue(fn: Callable, n: int, a=-1., b=1.):
    """
    Construit une "fonction étagée" approximant une fonction `fn` à valeurs positives, pour une ordonnée maximale `n`.
    La construction se restreint à un intervalle [`a`,`b`] (l'intervalle [-10,10] par défaut).
    """

    NUM_POINTS_PAR_UNITE = 1_000

    num_points = int((b-a)*NUM_POINTS_PAR_UNITE)
    x_s = np.linspace(start=a, stop=b, num=num_points, endpoint=False)
    fn_valeurs = fn(x_s)

    fn_etagee_vals = [None for _ in range(num_points)]

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
    plt_couleurs = ['g', 'r', 'c', 'm', 'y', 'k']
    nb_clrs = len(plt_couleurs)
    i_a_afficher = range(max_n, 1, -(max_n//nb_clrs + 1))

    fn_etagee_vals = [None for _ in range(MAX_N + 1)]

    for i in i_a_afficher:
        x_s, fn_etagee_vals[i] = fonction_lebesgue(fn=fn, n=i, a=a, b=b)

        clr = plt_couleurs[(i * nb_clrs - 1)//max_n]
        plt.plot(x_s, fn_etagee_vals[i], clr)

    plt.plot(x_s, FUNCTION(x_s), 'b')
    plt.show()


# Variables utilisateur
A, B = -10., 10.
MAX_N = 10
FUNCTION = f2

# Début script
plot_lemme_approximation(fn=FUNCTION, max_n=MAX_N, a=A, b=B)
