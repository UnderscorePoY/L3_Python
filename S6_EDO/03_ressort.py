#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 14:57:33 2022

@author: thomas.bescond
"""

import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import numpy as np


###
### SOLVE IVP
###

# Définition de l'équation différentielle du double ressort

lambdaa, mu = 1/4., 1.
A = np.array([[0, 1], [-2*lambdaa, -mu]])
B = np.array([0, lambdaa])
def equation(t, y):
    global A, B
    
    return A @ y + B


t0 = 0.0 # seconde
tf = 10.0  # seconde
x0, x0_prime = 0., 0.
y0 = [x0, x0_prime]  # Condition initiale


erreurs_ivp = []
erreurs_euler = []


ks = [10.**i for i in range(0, -3, -1)]
for k in ks:
    max_step = k # step pour solve_ivp
    
    # Résolution
    solution = solve_ivp(equation, [t0, tf], y0, max_step=max_step)
    
    instants = solution.t
    ys_ivp = solution.y[0]
    
    
    
    
    ###
    ### SOLUTION EXACTE
    ###
    
    def f(t):
        return 1/2*np.exp(-t/2)*(np.exp(t/2) + (-1 + 2*x0)*np.cos(t/2) + (-1 + 2*x0)*np.sin(t/2))
    
    ys_exact = [f(t) for t in instants]
    
    
    diff_ivp = max(abs(np.array([ivp - f(t) for (t,ivp) in zip(instants, ys_ivp)])))
    erreurs_ivp.append(diff_ivp)
    
    
    ###
    ### SCHEMA D'EULER EXPLICITE
    ###

    X = y0
    xs = [X[0]]
    ts = [0]
    t = 0
    for n in range(int(tf/k)):
        X = (np.array([[1., 0.], [0., 1.]]) + k*A) @ X + k*B
        xs.append(X[0])
        
        t += k
        ts.append(t)
    
    diff_euler = max(abs(np.array([euler - f(t) for (t,euler) in zip(ts, xs)])))
    erreurs_euler.append(diff_euler)
    
plt.loglog(ks, erreurs_euler)
plt.loglog(ks, erreurs_ivp)
plt.show()

slope_erreurs_euler, _ = np.polyfit(np.log(ks), np.log(erreurs_euler), 1)
slope_erreurs_ivp, _ = np.polyfit(np.log(ks), np.log(erreurs_ivp), 1)
print('Pente : %f' % slope_erreurs_euler)
print('Pente : %f' % slope_erreurs_ivp)



"""
       
###
### ERREURS A LA VALEUR EXACTE
###
    
diff_ivp = [ivp - f(t) for (t,ivp) in zip(instants, ys_ivp)]
diff_euler = [euler - f(t) for (t,euler) in zip(ts, xs)]

print('Erreur max. solve_ivp : %f' % max(np.abs(diff_ivp)))
print('Erreur max. Euler explicite : %f' % (max(np.abs(diff_euler))))
    
plt.plot(instants, ys_ivp) # Solution ivp
plt.plot(instants, ys_exact, 'y--') # Solution exacte
plt.plot(ts, xs, 'r') # Solution Euler explicite
plt.plot(instants, [0.5 for _ in instants]) # Valeur limite

plt.show()

"""