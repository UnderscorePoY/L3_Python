from scipy.special import erf, erfinv
import numpy as np
from random import random as uniform
from affichage_qualites import densite_normale_centree_reduite
import matplotlib.pyplot as plt


def tirage_rejet(a, b, M):
    nb_iter = 0
    while True:
        nb_iter += 1

        x = a + (b - a) * uniform()
        y = M * uniform()
        if y <= densite_normale_centree_reduite(x):
            return x, nb_iter


def tirages_rejet(a, b, M, N):
    moyenne = 0
    tirages = [0. for _ in range(N)]
    for i in range(N):
        tirages[i], nb_iter = tirage_rejet(a, b, M)
        moyenne += nb_iter
    moyenne /= N

    return tirages, moyenne


def main():
    N = 10_000
    a, b, M = -5, 5, 1 / np.sqrt(2 * np.pi)
    tirages, moyenne = tirages_rejet(a, b, M, N)

    print(moyenne)

    # Densité d'une gaussienne centree reduite
    x = np.linspace(-5, 5, 200)
    y = [densite_normale_centree_reduite(x0) for x0 in x]

    nb_conteneurs = 100
    plt.hist(tirages, nb_conteneurs, color="b", density=True, label=f"Tirages rejet")
    plt.plot(x, y, color="red", label="Densité gaussienne centrée réduite")
    plt.title(f"Emulation d'une loi normale centrée réduite\npar la méthode de rejet")

    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
