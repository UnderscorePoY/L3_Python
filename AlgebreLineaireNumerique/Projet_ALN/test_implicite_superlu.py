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
Nx = 10_000
Nt_list = np.array([100, 200, 300, 400, 500, 700,
                    1000, 2000, 3000, 4000, 5000, 7000,
                    10000, 20000, 30000, 40000, 50000, 70000,
                    ])  # [1_000_000, 500_000, 200_000, 100_000, 50_000, 20_000, 10_000, 5_000, 2_000, 1_000, 500, 200, 100]

temps_LU_simple = []
temps_LU_tridiagonal = []
temps_superLU = []

erreurs = []

dx = R / (Nx + 1)
x_i = [i * dx * 100 for i in range(Nx + 2)]
temperatures_attendues = [Tmax - (Tmax - Tamb) * x / (R * 100) for x in x_i]
for Nt in Nt_list:
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
    #start_time = time.process_time()
    for i in range(Nt):
        if i % 1_000 == 0:
            print(i)
        X = LU.solve(B)
        B = X.copy()
    #end_time = time.process_time()
    #temps_superLU = np.append(temps_superLU, end_time - start_time)
    #print("superLU {} done - {}s".format(Nx, end_time - start_time))

    # Mesure de l'erreur en température
    #plt.plot(x_i, B, 'b')
    #plt.plot(x_i, temperatures_attendues, 'k')
    #plt.show()

    #plt.plot(temperatures_attendues-B)
    erreurs = np.append(erreurs, max(abs(temperatures_attendues-B)))

print(erreurs)
# slope_LU_simple, _ = np.polyfit(np.log(Nx_list), np.log(temps_LU_simple), 1)
# slope_LU_tridiagonal, _ = np.polyfit(np.log(Nx_list), np.log(temps_LU_tridiagonal), 1)
slope_erreurs, _ = np.polyfit(np.log(tmax/(Nt_list+1)), np.log(erreurs), 1)

plt.xlabel('dt')
plt.ylabel("Erreur [en °C]")
# plt.loglog(Nx_list, temps_LU_simple, 'r', label="LU simple factorisation (ordre={:.3f})".format(slope_LU_simple))
plt.loglog(tmax/(Nt_list+1), erreurs, 'm', label="Ordre de l'erreur en temps = {:.3f}".format(slope_erreurs))
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
