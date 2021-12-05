import numpy as np
import time
import matplotlib.pyplot as plt

from scipy.sparse import csc_matrix, linalg as sla
from scipy.sparse import diags
from lu import *

R, tmax = 0.065, 60.  # en mètres, en secondes
D = 98.8e-6  # Diffusivité thermique de l'aluminium
Tmax = 80.  # °C
Tamb = 20.  # °C
Nx_list = range(1_000_000, 5_000_001, 1_000_000)
Nt = 3_000_000_000_000

temps_LU_simple = []
temps_LU_tridiagonal = []
temps_superLU = []


for Nx in Nx_list:
    dx = R / (Nx + 1)
    dt = tmax / (Nt + 1)
    beta = D * dt / dx ** 2
    print("beta={}".format(beta))

    # Matrice Euler implicite
    diag = [1 + 2. * beta for _ in range(Nx+2)]
    diag[0], diag[Nx+1] = 1, 1  # Condition aux bornes

    upper_band = [-beta for _ in range(Nx+1)]
    upper_band[0] = 0

    lower_band = [-beta for _ in range(Nx+1)]
    lower_band[Nx] = 0

    diagonals = [diag, lower_band, upper_band]
    M = csc_matrix(diags(diagonals, [0, -1, 1]))

    # Vecteur initial
    B = np.transpose(np.array([Tamb for _ in range(Nx + 2)]))
    B[0] = Tmax

    '''
    # LU simple
    start_time = time.process_time()
    LU = factorisation_LU(M, keep=True)
    end_time = time.process_time()
    temps_LU_simple = np.append(temps_LU_simple, end_time - start_time)
    print("simple {} done - {}s".format(Nx, end_time - start_time))
    '''

    '''
    start_time = time.process_time()
    Y = descente(M, B, keep=True)
    X = remontee(M, Y)
    end_time = time.process_time()
    temps_LU_simple = np.append(temps_LU_simple, end_time - start_time)
    print("simple {} done - {}s".format(Nx, end_time - start_time))

    compare = X.copy()
    '''

    '''
    # LU tridiagonal
    start_time = time.process_time()
    LU = factorisation_LU_tridiagonal(M)
    end_time = time.process_time()
    temps_LU_tridiagonal = np.append(temps_LU_tridiagonal, end_time - start_time)
    print("tridiag {} done - {}s".format(Nx, end_time - start_time))
    '''

    '''
    start_time = time.process_time()
    Y = descente_tridiagonal(M, B, keep=True)
    X = remontee_tridiagonal(M, Y)
    end_time = time.process_time()
    temps_LU_tridiagonal = np.append(temps_LU_tridiagonal, end_time - start_time)
    print("tridiag {} done - {}s".format(Nx, end_time - start_time))
    #compare -= X
    # print(compare)
    '''

    # sparce superLU
    M = csc_matrix(M)
    LU = sla.splu(M)
    start_time = time.process_time()
    X = LU.solve(B)
    end_time = time.process_time()
    temps_superLU = np.append(temps_superLU, end_time - start_time)
    print("superLU {} done - {}s".format(Nx, end_time - start_time))



# slope_LU_simple, _ = np.polyfit(np.log(Nx_list), np.log(temps_LU_simple), 1)
# slope_LU_tridiagonal, _ = np.polyfit(np.log(Nx_list), np.log(temps_LU_tridiagonal), 1)
slope_superLU, _ = np.polyfit(np.log(Nx_list), np.log(temps_superLU), 1)

plt.xlabel('Nx')
plt.ylabel("Durée d'exécution [en s]")
# plt.loglog(Nx_list, temps_LU_simple, 'r', label="LU simple factorisation (ordre={:.3f})".format(slope_LU_simple))
plt.loglog(Nx_list, temps_superLU, 'c', label="sparce superLU descente-remontée (ordre={:.3f})".format(slope_superLU))
plt.legend()
# plt.plot(np.log(Nx_lst), np.log(y_predicted), 'b')
plt.show()


'''
for i in range(Nt):
    Y = descente(LU, B, keep=True)
    X = remontee(LU, Y)

    # Fonctionne correctement, sauf pour les premiers instants où le principe du minimum n'est pas respecté ...
    # X = np.linalg.solve(M, B)

    print(X)
    B = X.copy()
    # if i >= 10:
    #    break
'''
