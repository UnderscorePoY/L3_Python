import numpy as np
import matplotlib.pyplot as plt
import time

from lu import *
from choleski import *
from matplotlib import animation
from scipy.sparse import csr_matrix, csc_matrix, diags, linalg as sla

R, tmax = 0.065, 60.  # en mètres, en secondes
D = 98.8e-6  # Diffusivité thermique de l'aluminium
Tmax = 80.  # °C
Tamb = 20.  # °C
Nx_lst = np.array([10_000])
Nt_lst = np.array([2_811_768])

for Nx in Nx_lst:
    for Nt in Nt_lst:
        dx = R / (Nx + 1)
        dt = tmax / (Nt + 1)
        beta = D * dt / dx ** 2

        print("beta={}, Nx={}, Nt={}".format(beta, Nx, Nt))

        X = np.array([0. for _ in range(Nx + 2)])

        # Matrice Euler implicite
        diag = [1 + 2. * beta for _ in range(Nx + 2)]
        diag[0], diag[Nx + 1] = 1, 1  # Condition aux bornes

        upper_band = [-beta for _ in range(Nx + 1)]
        upper_band[0] = 0

        lower_band = [-beta for _ in range(Nx + 1)]
        lower_band[Nx] = 0

        diagonals = [diag, lower_band, upper_band]
        M = csc_matrix(diags(diagonals, [0, -1, 1]))

        # Vecteur initial
        B = np.transpose(np.array([Tamb for _ in range(Nx + 2)]))
        B[0] = Tmax

        # superLU
        LU = sla.splu(M)
        # print("L done")
        # print(L)

        x_i = [i * dx * 100 for i in range(Nx + 2)]  # Positions des points à l'intérieur de l'intervalle
        fig = plt.figure()
        line, = plt.plot([], [])
        plt.xlim(0, R * 100)
        plt.ylim(Tamb, Tmax)
        plt.xlabel('Position (cm)')
        plt.ylabel('Temperature (°C)')

        for i in range(Nt):
            X = LU.solve(B)
            if i % 50_000 == 0:
                print(i)
                plt.plot(x_i, X, 'b')
            B = X.copy()
        plt.show()
        '''
        def animate(i):
            global LU, B, X
            X = LU.solve(B)

            if i % 1_000 == 0:
                print(i)
                plt.plot(x_i, X, 'b')
            #line.set_data(x_i, X)
            # print(x_i)
            #print(X)
            B = X.copy()

            # filename = folder+'/{:0>9}.png'.format(i)

            # save frame
            # plt.savefig(filename)

            return line,
        '''

        # ani = animation.FuncAnimation(fig, animate, frames=Nt, blit=True, repeat=False)#interval=.5, repeat=False)

        # time.sleep(5)
        # plt.show()
