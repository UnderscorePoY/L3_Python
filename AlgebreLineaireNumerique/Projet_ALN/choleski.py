from math import sqrt


def factorisation_choleski(A):
    n = len(A)
    L = [[0. for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(i):
            L[i][j] = A[i][j]
            for k in range(j):
                L[i][j] = L[i][j] - L[i][k] * L[j][k]
            L[i][j] = L[i][j] / L[j][j]
        L[i][i] = A[i][i]
        for j in range(i):
            L[i][i] = L[i][i] - L[i][j] ** 2
        L[i][i] = sqrt(L[i][i])

    return L


def descente_choleski(L, b):
    n = len(L)

    for i in range(n):
        for j in range(i):
            b[i] = b[i] - L[i][j] * b[j]
        b[i] = b[i] / L[i][i]


def remontee_choleski(L, b):
    n = len(L)

    for i in reversed(range(n)):
        for j in range(i + 1, n):
            b[i] = b[i] - L[j][i] * b[j]

        b[i] = b[i] / L[i][i]


def factorisation_choleski_tridiagonal(L):
    n = len(L)

    for i in range(n):
        L[i][i-1] = L[i][i-1] / L[i-1][i-1]

        L[i][i] = L[i][i] - L[i][i-1] ** 2
        L[i][i] = sqrt(L[i][i])

    return L


def descente_choleski_tridiagonal(L, b):
    n = len(L)

    for i in range(n):
        b[i] -= L[i][i-1] * b[i-1]
        b[i] /= L[i][i]

    return b

def remontee_choleski_tridiagonal(L, b):
    n = len(L)

    for i in reversed(range(n)):
        if i + 1 < n:
            b[i] -= L[i+1][i] * b[i+1]
        b[i] /= L[i][i]

    return b


'''
A = [[1, 2, 0, 0], [2, 5, 3, 0], [0, 3, 10, 4], [0, 0, 4, 17]]
L = factorisation_choleski_tridiagonal(A)
print(L)  # L attendu = [[1, 0, 0, 0],[2, 1, 0, 0],[0, 3, 1, 0],[0, 0, 4, 1]]*[[1, 2, 0, 0],[0, 1, 3, 0],[0, 0, 1, 4],[0, 0, 0, 1]]

b = [-3, 1, 8, -56]
descente_choleski_tridiagonal(L, b)
print(b)  # b attendu = [-3, 7, -13, -4]

remontee_choleski_tridiagonal(L, b)
print(b)  # b attendu = [1, -2, 3, -4]
'''
