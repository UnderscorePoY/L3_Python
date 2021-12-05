import numpy as np
import matplotlib.pyplot as plt
import time

from lu import *
from matplotlib import animation
from scipy.sparse import csr_matrix

R, tmax = 0.065, 60.  # en mètres, en secondes
D = 98.8e-6  # Diffusivité thermique de l'aluminium
Tmax = 80.  # °C
Tamb = 20.  # °C
Nx_lst = np.array([50])
Nt_lst = np.array([10_000])

for Nx in Nx_lst:
    for Nt in Nt_lst:
        dx = R / (Nx + 1)
        dt = tmax / (Nt + 1)
        beta = D * dt / dx ** 2

        print("beta={}, Nx={}, Nt={}".format(beta, Nx, Nt))

        X = np.array([0. for _ in range(Nx + 2)])

        # Matrice Euler implicite
        M = np.array([[0. for _ in range(Nx + 2)] for _ in range(Nx + 2)])

        M[0][0], M[Nx + 1][Nx + 1] = 1, 1  # Condition aux bornes
        for i in range(1, Nx + 1):
            M[i][i] = 1 + 2. * beta

        for i in range(1, Nx + 1):
            M[i][i + 1] = -beta

        for i in range(Nx):
            M[i + 1][i] = -beta

        print(M)

        # On pose les valeurs de la fonction f en les x_i.
        B = np.transpose(np.array([Tamb for _ in range(Nx + 2)]))
        B[0] = Tmax

        # LU
        LU = factorisation_LU_tridiagonal(M)
        x_i = [i * dx * 100 for i in range(Nx + 2)]  # Positions des points à l'intérieur de l'intervalle
        # print("LU done")
        #print(LU)

        fig = plt.figure()
        line, = plt.plot([], [])
        plt.xlim(0, R * 100)
        plt.ylim(Tamb, Tmax)
        plt.xlabel('Position (cm)')
        plt.ylabel('Temperature (°C)')


        def animate(i):
            global LU, B, X
            Y = descente_tridiagonal(LU, B)
            # print(Y)
            X = remontee_tridiagonal(LU, Y)
            # print(X)
            # X=np.linalg.solve(M, B) # Fonctionne correctement

            # if i % 1_000 == 999:
            #    plt.plot(x_i, X, 'b')
            line.set_data(x_i, X)
            # print(x_i)
            print(X)
            B = X.copy()

            # filename = folder+'/{:0>9}.png'.format(i)

            # save frame
            # plt.savefig(filename)

            return line,


        ani = animation.FuncAnimation(fig, animate, frames=Nt, blit=True, interval=.5, repeat=False)

        # time.sleep(5)
        plt.show()
