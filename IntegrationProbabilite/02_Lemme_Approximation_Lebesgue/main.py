from lebesgue import *


# Fonctions utilisateurs
def f1(x) -> float:
    return 1./1000 * (x + 4)*(x + 1)*(x - 2)*(x - 5) + 1


def f2(x) -> float:
    return 2 * np.log(1+abs(x)) * np.exp(-x/50)


def f3(x) -> float:
    return 5 * (1-np.exp(-(x/4)**2))


# Variables utilisateur
A, B = -10., 10.
MAX_N = 5
FUNCTION = f3

# Début script
plot_lemme_approximation(fn=FUNCTION, max_n=MAX_N, a=A, b=B)
