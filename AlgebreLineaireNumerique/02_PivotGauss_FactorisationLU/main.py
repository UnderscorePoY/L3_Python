from methodes_directes import *

A = [[1., 0., 1.], [0., 2., -1.], [-1., 1., -2.]]
b = [2., 1., -2.]

# A = [[1., 0., 1.], [0., 2., -1.], [-1., 1., -2.]]
# b = [2., 1., -2.]
# Résultat attendu : [1.0, 1.0, 1.0]
print(gauss_sans_permutation(A, b))
