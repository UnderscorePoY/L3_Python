#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 14:46:52 2022

@author: thomas.bescond
"""

import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import numpy as np


###
### SOLVE IVP
###

# Définition de l'équation différentielle du double ressort

A = np.array([[0, -1], 
              [1, 0]])
B = np.array([0, 
              0])
def equation(t, y):
    global A, B
    return A @ y + B


t0 = 0.0 # seconde
tf = 10.0  # seconde
X0 = [1.,
      0.]  # Condition initiale


erreurs_ivp = []
erreurs_euler = []


ks = [0.01]
for k in ks:
    max_step = k # step pour solve_ivp
    
    # Résolution
    solution = solve_ivp(equation, [t0, tf], X0, max_step=max_step)
    
    instants = solution.t
    ys_ivp = solution.y    
    
    
    ###
    ### SOLUTION EXACTE
    ###
    
    ys_exact = [[np.cos(t) for t in instants],
                [np.sin(t) for t in instants]]
    
    
    ###
    ### SCHEMA D'EULER EXPLICITE
    ###

    X = X0
    x0s = [X0[0]]
    x1s = [X0[1]]
    ts = [0]
    t = 0
    for n in range(int(tf/k)):
        X = (np.array([[1., 0.], [0., 1.]]) + k*A) @ X + k*B
        x0s.append(X[0])
        x1s.append(X[1])
        
        t += k
        ts.append(t)
    
    ###
    ### SCHEMA D'EULER SIMPLECTIQUE
    ### (uniquement cas de la matrice "i")
    
    x0 = X0[0]
    x1 = X0[1]
    x0s_simpl = [x0]
    x1s_simpl = [x1]
    t = 0
    for n in range(int(tf/k)):
        x0 += -k * x1
        x1 += k * x0
        x0s_simpl.append(x0)
        x1s_simpl.append(x1)
        
        t += k
        
    ###
    ### SCHEMA D'EULER IMPLICITE
    ### (uniquement cas de la matrice "i")
    
    x0 = X0[0]
    x1 = X0[1]
    x0s_impl = [x0]
    x1s_impl = [x1]
    t = 0
    for n in range(int(tf/k)):
        x0_c, x1_c = x0, x1
        x0 = (x0_c - k*x1_c)/(1+k**2)
        x1 = (x1_c + k*x0_c)/(1+k**2)
        x0s_impl.append(x0)
        x1s_impl.append(x1)
        
        t += k
    
    
    #print(ys_ivp)
    #plt.plot(ys_ivp[0],ys_ivp[1])# Solution ivp
    #plt.plot(ys_exact[0], ys_exact[1], 'y') # Solution exacte
    plt.plot(x0s, x1s, 'r') # Solution Euler explicite
    #plt.plot(x0s_simpl, x1s_simpl, 'g') # Solution Euler simplectique
    plt.plot(x0s_impl, x1s_impl, 'g') # Solution Euler implicite
    
    plt.axis('equal')
    plt.show()
