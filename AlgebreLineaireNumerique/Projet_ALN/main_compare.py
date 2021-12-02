import numpy as np
import matplotlib.pyplot as plt
import time
#from sklearn.linear_model import LinearRegression
#from sklearn.metrics import mean_squared_error, r2_score
from scipy.sparse import csr_matrix

R, tmax = 0.065, 60.  # en mètres, en secondes
D = 98.8e-6  # Diffusivité thermique de l'aluminium
Tmax = 80  # °C
Tamb = 20  # °C
Nx_lst = np.array([i for i in range(75, 151, 25)])
# Nx_lst = [50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300]  # Nx, Nt = 35, 1000 stable | 35, 978 instable
temps_mult_simple = np.array([])
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
    print(beta, Nt)

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

    # print(M)

    # On pose les valeurs de la fonction f en les x_i.
    B = np.transpose(np.array([Tamb for _ in range(Nx+2)]))
    B[0] = Tmax

    # Itérations
    '''
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
    #compare = B.copy()

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
    print("Fini pour "+str(Nx))
    #compare -= B
    #print(compare)

# print(temps_mult_simple)
print(temps_mult_np_dot)
print(temps_mult_sparce)

'''
Nx_lst_res = Nx_lst.reshape(-1, 1)
reg = LinearRegression()
reg.fit(np.log(Nx_lst_res), np.log(temps_ecoules))
y_predicted = reg.predict(np.log(Nx_lst_res))
'''

# model evaluation
#mse = mean_squared_error(np.log(temps_ecoules), np.log(y_predicted))

#rmse = np.sqrt(mean_squared_error(np.log(temps_ecoules), np.log(y_predicted)))
#r2 = r2_score(np.log(temps_ecoules), np.log(y_predicted))

'''
# printing values
print('Slope:', reg.coef_)
print('Intercept:', reg.intercept_)
print('MSE:', mse)
print('Root mean squared error: ', rmse)
print('R2 score: ', r2)
'''



plt.xlabel('Nx')
plt.ylabel('Temps (s)')
# plt.plot(Nx_lst, temps_mult_simple, 'r', label="Multiplication naïve")
plt.plot(Nx_lst, temps_mult_np_dot, 'b', label="np.dot")
plt.plot(Nx_lst, temps_mult_sparce, 'g', label="sparce @")
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