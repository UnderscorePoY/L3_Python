from scipy.special import erf, erfinv
import numpy as np
from random import random as uniform
from affichage_qualites import densite_normale_centree_reduite
import matplotlib.pyplot as plt


def repartition_normale_centree_reduite(x):
    return (1 + erf(x / np.sqrt(2))) / 2


def inv_repartition_normale_centree_reduite(y):
    return np.sqrt(2) * erfinv(2 * y - 1)


def tirages_methode_inversion(N):
    return [inv_repartition_normale_centree_reduite(uniform()) for _ in range(N)]


def main():
    N = 10_000
    tirages = tirages_methode_inversion(N)

    # Densité d'une gaussienne centree reduite
    x = np.linspace(-5, 5, 200)
    y = [densite_normale_centree_reduite(x0) for x0 in x]

    nb_conteneurs = 100
    plt.hist(tirages, nb_conteneurs, color="b", density=True, label=f"Tirages inverse")
    plt.plot(x, y, color="red", label="Densité gaussienne centrée réduite")
    plt.title(f"Emulation d'une loi normale centrée réduite\npar la méthode d'inversion")

    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()