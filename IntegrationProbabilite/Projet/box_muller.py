from random import random as uniform
import matplotlib.pyplot as plt
import numpy as np


def box_muller():
    tirage1 = uniform()
    tirage2 = uniform()

    return np.sqrt(-2 * np.log(tirage1)) * np.cos(2 * np.pi * tirage2)
    # return np.sqrt(-2*np.log(tirage1))*np.sin(2*np.pi*tirage2)


def tirages_box_muller(N):
    return [box_muller() for _ in range(N)]


N = 10_000
tirages_normale_centree_reduite = tirages_box_muller(N)
# Affichage des tirages cos
k = 100
plt.hist(tirages_normale_centree_reduite, k, color='b', density=True, label="Tirages Box-Müller")
# Affichage de la densité théorique de la loi cos
x = np.linspace(-5, 5, 200)
y = [1/np.sqrt(2*np.pi)*np.exp(-(x0**2)/2) for x0 in x]
plt.plot(x, y, color="red", label="Densité gaussienne centrée réduite")
plt.title(f"Emulation d'une loi normale centrée réduite\npar la méthode de Box-Müller")
plt.legend()
plt.show()
