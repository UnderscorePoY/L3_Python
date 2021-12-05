import numpy as np
import matplotlib.pyplot as plt
import time

from matplotlib import animation
from scipy.sparse import csr_matrix

folder = r'C:\Users\thoma\Documents\MEGAsync\Cours\Maths\10_1_ALN\Projet\gif'

R, tmax = 0.065, 60.  # en mètres, en secondes
Nx = 1_000  # 35, 1000 stable | 35, 978 instable
D = 98.8e-6  # Diffusivité thermique de l'aluminium
Tmax = 80  # °C
Tamb = 20  # °C

dx = R/(Nx+1)
dt = dx**2/(2*D)
Nt = int(tmax/dt)

beta = D*dt/dx**2
while beta >= 1/2:
    Nt += 1
    dt = tmax/(Nt + 1)
    beta = D * dt / dx ** 2

Nt = 2_811_756  # Nt -= 13
dt = tmax/(Nt + 1)
beta = D * dt / dx ** 2
print(beta, Nx, Nt)

# Matrice Euler explicite
M = np.array([[0. for _ in range(Nx+2)] for _ in range(Nx+2)])

M[0][0], M[Nx+1][Nx+1] = 1, 1  # Condition aux bornes
for i in range(1, Nx+1):
    M[i][i] = 1-2.*beta

for i in range(1, Nx+1):
    M[i][i+1] = beta

for i in range(Nx):
    M[i+1][i] = beta

sparceM = csr_matrix(M)
# print(M)

# On pose les valeurs de la fonction f en les x_i.
B = np.transpose(np.array([Tamb for _ in range(Nx+2)]))
B[0] = Tmax

# print(B)

# Préparation de l'affichage graphique
x_i = [i * dx * 100 for i in range(Nx + 2)]  # Positions des points à l'intérieur de l'intervalle
# print(x_i)
it = np.linspace(start=0., stop=1., num=10_000 + 1, endpoint=True)

# Itérations

fig = plt.figure()
line, = plt.plot([], [])
plt.xlim(0, R*100)
plt.ylim(Tamb, Tmax)
#plt.xlim(2.0, 2.1)
#plt.ylim(58.5, 63.5)
plt.xlabel('Position (cm)')
plt.ylabel('Temperature (°C)')

for i in range(Nt):
    X = sparceM @ B
    B = X.copy()
    #if i % 50_000 == 0:
    #    plt.plot(x_i, X, 'b')
plt.plot(x_i, X, 'b,', label="Solution approchée")
plt.plot(x_i, [Tmax-(Tmax-Tamb)*x/(R*100) for x in x_i], "k", label="Solution exacte")
plt.legend()
plt.show()

'''
def animate(i):
    global M, B
    X = sparceM @ B  # X = np.linalg.solve(M, B)
    # print(X)

    if i % 1_000 == 999:
        plt.plot(x_i, X, 'b')
    # line.set_data(x_i, X)
    B = X.copy()

    # filename = folder+'/{:0>9}.png'.format(i)

    # save frame
    # plt.savefig(filename)

    return line,


ani = animation.FuncAnimation(fig, animate, frames=Nt, blit=True, interval=.5, repeat=False)

# time.sleep(5)
plt.show()
'''