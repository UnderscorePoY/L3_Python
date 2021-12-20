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
Nt_lst = np.array([1_000_000//2])

for Nx in Nx_lst:
    for Nt in Nt_lst:
        dx = R / (Nx + 1)
        dt = tmax / (Nt + 1)
        beta = D * dt / (2 * dx ** 2)

        print("beta={}, Nx={}, Nt={}".format(beta, Nx, Nt))

        X = np.array([0. for _ in range(Nx + 2)])

        # Crank Nicolson
        # I*T^(n+1) = E*T^(n)

        # Matrice I
        diagI = [1 + 2. * beta for _ in range(Nx + 2)]
        diagI[0], diagI[Nx + 1] = 1, 1  # Condition aux bornes

        upper_bandI = [-beta for _ in range(Nx + 1)]
        upper_bandI[0] = 0

        lower_bandI = [-beta for _ in range(Nx + 1)]
        lower_bandI[Nx] = 0

        diagonalsI = [diagI, lower_bandI, upper_bandI]
        I = csc_matrix(diags(diagonalsI, [0, -1, 1]))

        # Matrice E
        diagE = [1 - 2. * beta for _ in range(Nx + 2)]
        diagE[0], diagE[Nx + 1] = 1, 1  # Condition aux bornes

        upper_bandE = [beta for _ in range(Nx + 1)]
        upper_bandE[0] = 0

        lower_bandE = [beta for _ in range(Nx + 1)]
        lower_bandE[Nx] = 0

        diagonalsE = [diagE, lower_bandE, upper_bandE]
        E = csc_matrix(diags(diagonalsE, [0, -1, 1]))


        # Vecteur initial
        B = np.transpose(np.array([Tamb for _ in range(Nx + 2)]))
        B[0] = Tmax


        # superLU sur I
        LU = sla.splu(I)
        # print("L done")
        # print(L)

        x_i = [i * dx * 100 for i in range(Nx + 2)]  # Positions des points à l'intérieur de l'intervalle
        fig = plt.figure()
        line, = plt.plot([], [])
        #plt.xlim(2., 2.1)
        #plt.ylim(58, 64)
        plt.xlim(0, R * 100)
        plt.ylim(Tamb, Tmax)
        plt.xlabel('Position (cm)')
        plt.ylabel('Temperature (°C)')
        plt.plot(x_i, [Tmax - (Tmax - Tamb) * x / (R * 100) for x in x_i], "k,")


        for i in range(Nt):
            Y = E @ B
            B = LU.solve(Y)
            if i % (Nt_lst//50) == 0:
                print(i)
                plt.plot(x_i, B, 'b')
            #B = X.copy()
        plt.show()


        '''
        batch = 50_000
        def animate(i):
            global LU, B, E, X, batch

            for _ in range(batch):
                Y = E @ B
                X = LU.solve(Y)
                B = X.copy()

            #if i % 1_000 == 0:
            # print(i)
            plt.plot(x_i, X, 'b')
            line.set_data(x_i, X)
            # print(x_i)
            #print(X)

            # filename = folder+'/{:0>9}.png'.format(i)

            # save frame
            # plt.savefig(filename)

            return line,


        ani = animation.FuncAnimation(fig, animate, frames=Nt//batch, blit=True, interval=.05, repeat=False)
        '''
        # time.sleep(5)
        plt.show()
