import numpy as np
import matplotlib.pyplot as plt
import time

from scipy.sparse import csr_matrix

R, tmax = 0.065, 60.  # en mètres, en secondes
D = 98.8e-6  # Diffusivité thermique de l'aluminium
Tmax = 80  # °C
Tamb = 20  # °C
Nx_lst = np.array([i for i in range(100, 501, 50)])
# Nx_lst = [50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300]  # Nx, Nt = 35, 1000 stable | 35, 978 instable
temps_mult_simple = np.array([])
temps_mult_tridiagonal = np.array([])
temps_mult_np_dot = np.array([])
temps_mult_sparce = np.array([])

for Nx in Nx_lst:
    dx = R/(Nx+1)
    dt = dx**2/(2*D)
    Nt = int(tmax/dt)

    beta = D*dt/dx**2
    while beta >= 1/2:
        Nt += 1
        dt = tmax/(Nt + 1)
        beta = D * dt / dx ** 2

    # assert beta < 1/2, "Beta = "+str(beta)
    print("beta={}, Nx={}, Nt={}".format(beta, Nx, Nt))

    X = np.array([0. for _ in range(Nx+2)])

    # Matrice Euler explicite
    M = np.array([[0. for _ in range(Nx+2)] for _ in range(Nx+2)])

    M[0][0], M[Nx+1][Nx+1] = 1, 1  # Condition aux bornes
    for i in range(1, Nx+1):
        M[i][i] = 1-2.*beta

    for i in range(1, Nx+1):
        M[i][i+1] = beta

    for i in range(Nx):
        M[i+1][i] = beta

    print(M)

    # On pose les valeurs de la fonction f en les x_i.
    B = np.transpose(np.array([Tamb for _ in range(Nx+2)]))
    B[0] = Tmax

    # Itérations

    '''
    # Multiplication naive
    start_time = time.process_time()
    for i in range(Nt):
        #if i % 1_000 == 0:
        #    print(i)
        for I in range(Nx+2):
            S = 0.
            for J in range(Nx+2):
                S += M[I][J]*B[J]
            X[I] = S
        B = X.copy()
    end_time = time.process_time()
    temps_mult_simple = np.append(temps_mult_simple, end_time - start_time)
    compare = B.copy()
    '''

    '''
    # Multiplication tridiagonale
    B = np.transpose(np.array([Tamb for _ in range(Nx + 2)]))
    B[0] = Tmax
    start_time = time.process_time()
    for i in range(Nt):
        X[0] = B[0]
        X[Nx+1] = B[Nx+1]
        for I in range(1, Nx+1):
            S = 0.
            for J in range(I-1, I+2):
                S += M[I][J]*B[J]
            X[I] = S
        B = X.copy()
    end_time = time.process_time()
    temps_mult_tridiagonal = np.append(temps_mult_tridiagonal, end_time - start_time)
    #compare = B.copy()
    #print(compare)
    '''

    # np.dot
    B = np.transpose(np.array([Tamb for _ in range(Nx + 2)]))
    B[0] = Tmax
    start_time = time.process_time()
    for i in range(Nt):
        #if i % 10_000 == 0:
        #    print(i)
        X = M.dot(B)  # X = np.linalg.solve(M, B)
        B = X.copy()
    end_time = time.process_time()
    temps_mult_np_dot = np.append(temps_mult_np_dot, end_time - start_time)
    compare = B.copy()
    #print(compare)


    sparseM = csr_matrix(M)
    B = np.transpose(np.array([Tamb for _ in range(Nx + 2)]))
    B[0] = Tmax
    #sparseB = csr_matrix(B)
    start_time = time.process_time()
    for i in range(Nt):
        #if i % 10_000 == 0:
        #    print(i)
        X = sparseM @ B  # X = np.linalg.solve(M, B)
        B = X.copy()
    end_time = time.process_time()
    temps_mult_sparce = np.append(temps_mult_sparce, end_time - start_time)
    compare -= B
    #print(compare)


#print(temps_mult_np_dot)
#slope_simple, _ = np.polyfit(np.log(Nx_lst), np.log(temps_mult_simple), 1)
#slope_tridiagonal, _ = np.polyfit(np.log(Nx_lst), np.log(temps_mult_tridiagonal), 1)
slope_np_dot, _ = np.polyfit(np.log(Nx_lst), np.log(temps_mult_np_dot), 1)
slope_sparce, _ = np.polyfit(np.log(Nx_lst), np.log(temps_mult_sparce), 1)
#print(slope_simple, slope_np_dot)
#print(temps_mult_np_dot)
#print(temps_mult_sparce)

plt.xlabel('log(Nx)')
plt.ylabel("log(durée d'exécution [en s])")
#plt.loglog(Nx_lst, temps_mult_simple, 'r', label="Multiplication naïve (ordre={:.3f})".format(slope_simple))
#plt.loglog(Nx_lst, temps_mult_tridiagonal, 'g', label="Multiplication tridiagonale (ordre={:.3f})".format(slope_tridiagonal))
plt.loglog(Nx_lst, temps_mult_np_dot, 'c', label="np.dot (ordre={:.3f})".format(slope_np_dot))
plt.loglog(Nx_lst, temps_mult_sparce, 'm', label="sparce @ (ordre={:.3f})".format(slope_sparce))
plt.legend()
# plt.plot(np.log(Nx_lst), np.log(y_predicted), 'b')
plt.show()




'''
    fig = plt.figure()
    line, = plt.plot([], [])
    plt.xlim(0, R)
    plt.ylim(Tamb, Tmax)
    plt.xlabel('Position (m)')
    plt.ylabel('Temperature (°C)')
    plt.plot(x_i, X)
    plt.show()
'''