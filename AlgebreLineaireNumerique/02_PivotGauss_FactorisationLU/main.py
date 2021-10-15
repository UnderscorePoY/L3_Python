from methodes_directes import *


# [1] TEST GAUSS SANS PERMUTATION

A = [[1., 0., 1.], [0., 2., -1.], [-1., 1., -2.]]
b = [2., 1., -2.]

# A = [[1., 0., 1.], [0., 2., -1.], [-1., 1., -2.]]
# b = [2., 1., -2.]
# Résultat attendu : [1.0, 1.0, 1.0]
print(gauss_sans_permutation(A, b))


# [2] TEST GAUSS PIVOT PARTIEL


A = [[0, 1, 0], [1, 1, 1], [0, 1, 2]]
b = [-1, 2, 3]

# A = [[0, 1, 0], [1, 1, 1], [0, 1, 2]]
# b = [-1, 2, 3]
# Résultat attendu : [1.0, -1.0, 2.0]
print(gauss_pivot_partiel(A, b))
