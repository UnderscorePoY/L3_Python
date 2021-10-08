#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 09:31:49 2021

@author: thomas.bescond
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Callable, Any


def methode_newton(f: Callable, f_prime: Callable, x0: float, tol: float) \
    -> Any :
    """
    Applique la méthode de Newton à la résolution de l'équation f(x) = 0, pour un point `x0` proche de la solution recherchée.
    La solution sera retournée avec une erreur maximale fixée par la tolérence `tol`.
    Procédure : x(i+1) = x(i) - f(x(i)) / f'(x(i))
    """
    
        
    x, y = etape_Newton(f, f_prime, x0)
    print(x, y)
    
    n = 0  # Compteur d'itérations
    
    while abs(y-x) > tol:
        x, y = etape_Newton(f, f_prime, y)
        n += 1
        print(x, y)
    
    return y, n

def etape_Newton(f: Callable, f_prime: Callable, y: float) -> Any:
    return y, y - f(y)/f_prime(y)
    

def f_test(x: float):
    return x

def f_prime_test(x: float):
    return 1


def f_pt_fixe(x: Any) -> Any:
    return np.exp(x/5.)

def f_prime_pt_fixe(x: Any) -> Any:
    return 1/5. * np.exp(x/5.)

def f(x: Any) -> Any:
    return x - f_pt_fixe(x)

def f_prime(x: Any) -> Any:
    return 1 - f_prime_pt_fixe(x)


# print(methode_newton(f_test, f_prime_test, 10, 10**-8))  # valeur attendue : 0 en 1 itération.
    
x0 = 20
tol = 10**-8

sol, nb_iter = methode_newton(f, f_prime, x0, tol)  # valeur attendue : 12.713206... en 6 itérations.

x_vals = np.linspace(start=0., stop=22., num=10**4, endpoint=False)
plt.plot(x_vals, f_pt_fixe(x_vals), 'b', x_vals, x_vals, 'k')


x_a, y_a = x0, 0
for i in range(nb_iter):
    
    # FIX THIS !!!
    
    x_b, y_b = x_a, f_pt_fixe(x_a)
    plt.plot([x_a, x_b], [y_a, y_b], 'r')
    
    x_a, y_a = x_b, y_b
    x_b, y_b = etape_Newton(f_pt_fixe, f_prime_pt_fixe, y_a)
    x_b = 0
    print(x_a, y_a, x_b, y_b)
    plt.plot([x_a, x_b], [y_a, y_b], 'r')
    