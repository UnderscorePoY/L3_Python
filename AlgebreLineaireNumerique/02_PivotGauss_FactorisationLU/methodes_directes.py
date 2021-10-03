import copy

# Ce fichier contient un certain nombre de fonctions permettant de résoudre de diverses façons un système linéaire
# d'équations présenté sous la forme Ax = b, où A est une matrice carrée réelle et b est un vecteur réel.

# Note : Les fonctions ci-dessous ne sont pas des doublons :
# - celles démarrant par un "tiret du bas" contiennent la logique des opérations effectuées.
# - celles NE démarrant PAS par un tel tiret gèrent ce qu'il y a autour de la logique, comme la gestion de la mémoire.


def _factorisation_LU(
        A: list[list[float]],
) -> list[list[float]]:
    """
    Factorise la matrice carrée `A` suivant la décomposition LU:
      - les coefficients sous-diagonaux correspondent à la matrice L (Lower)
      à laquelle doit être ajoutée une diagonale de 1.
      - les coefficient diagonaux et sur-diagonaux correspondent à la matrice U (Upper).
    Ainsi A = LU, et la résolution de Ax = b se décompose comme suit :
     1. Ly = b d'inconnue y, avec y = Ux
     2. Ux = y d'inconnue x

    :param A: la matrice à factoriser suivant la décomposition LU.
    :return: la matrice `A` factorisée.
    """

    n = len(A)

    #      j=0     n-2
    # i=0 (a11 a12 ... a1n) => (a11     a12     ... a1n)
    #     (a21 a22 ... a2n) => (a21/a11 a22     ... a2n)
    #     (a31 a32 ... a3n) => (a31/a11 a32/a22 ... a3n)
    #     (... ... ... ...) => (...     ...     ... ...
    # n-1 (an1 an2 ... ann) => (an1/a11 an2/a22 ... ann)
    for j in range(n - 1):
        for i in range(j + 1, n):
            A[i][j] /= A[j][j]
            for l in range(j + 1, n):
                A[i][l] -= A[i][j] * A[j][l]
    return A


def factorisation_LU(
        A: list[list[float]],
        keep: bool = False
) -> list[list[float]]:
    """
    Factorise la matrice carrée `A` suivant la décomposition LU.

    :param A: la matrice à factoriser.
    :param keep: (default=False) si la matrice doit être gardée intacte. Sinon, les coefficients de L et U seront
    écrits dans la matrice `A` initiale  pour économiser de l'espace mémoire.
    :return: la matrice `A` factorisée.
    """

    B = A
    if keep:
        # Création d'une nouvelle matrice pour ne pas remplacer celle donnée en entrée
        B = copy.deepcopy(B)

    return _factorisation_LU(B)


def _descente(
    A: list[list[float]],
    b: list[float]
) -> list[float]:
    """
    Applique l'étape de descente à l'équation Ly = b d'inconnue y, avec y = Ux.

    :param A: la matrice provenant de la factorisation LU.
    :param b: le vecteur second membre.
    :return: le vecteur y intermédiaire.
    """

    n = len(A)

    # ( 1   0  ...  0) (y1)   (b1)
    # (a21  1  ...  0) (y2)   (b2)
    # (a31 a32 ...  0) (y3) = (b3)
    # (... ... ...  0) (..)   (..)
    # (an1 an2 ...  1) (yn)   (bn)
    for i in range(n):
        for j in range(i):
            b[i] -= A[i][j] * b[j]

    return b


def descente(
        A: list[list[float]],
        b: list[float],
        keep: bool = False
) -> list[float]:
    """
    Applique l'étape de descente à l'équation Ly = b d'inconnue y, avec y = Ux.

    :param A: la matrice provenant de la factorisation LU.
    :param b: le vecteur second membre.
    :param keep: (default=False) si le vecteur doit être gardé intacte. Sinon, les coefficients du vecteur seront
    réécrits pour économiser de l'espace mémoire.
    écrits dans la matrice `A` initiale.
    :return: le vecteur y intermédiaire.
    """

    y = b
    if keep:
        y = copy.deepcopy(b)

    return _descente(A, y)


def remontee(
        A: list[list[float]],
        y: list[float]
) -> list[float]:
    """
    Applique l'étape de remontée à l'équation Ux = y

    :param A : la matrice provenant de la factorisation LU.
    :param y: le vecteur second membre intermédiaire.
    :return: la solution x à l'équation Ux = y d'inconnue x.
    """

    # (a11 a12 ... a1n) (x1)   (y1)
    # ( 0  a22 ... a2n) (x2)   (y2)
    # ( 0   0  ... a3n) (x3) = (y3)
    # (... ... ... ...) (..)   (..)
    # ( 0   0  ... ann) (xn)   (yn)
    n = len(A)
    for i in reversed(range(n)):
        for j in range(i+1, n):
            y[i] -= A[i][j] * y[j]
        y[i] /= A[i][i]

    return y


def gauss_sans_permutation(
    A: list[list[float]],
    b: list[float],
    keep: bool = False
) -> list[float]:
    """
    Applique l'algorithme de Gauss sans permutation à l'équation Ax = b d'inconnue x.
    Sans permutation, certaines matrices ne peuvent pas être résolues avec cette méthode car les pivots peuvent être
    nuls, et entrainer une division par zéro.
    Dès lors qu'une exception `ZeroDivisionError` est levée, A est une telle matrice problématique.

    :param A: la matrice du système linéaire d'équations.
    :param b: le vecteur second membre.
    :param keep: si les objets initiaux doivent être conservés intactes.
    :return: la solution à l'équation Ax = b d'inconnue x.
    """

    LU = factorisation_LU(A, keep)
    y = descente(LU, b, keep)
    x = remontee(LU, y)

    return x
