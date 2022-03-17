#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 15:07:45 2022

@author: thomas.bescond
"""

import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
from functools import lru_cache


def f(t, y):
    return y*(1 + sp.exp(-y)) + sp.exp(2*t)


t0, tf = 0., 1.
y0 = 0.

def euler_explicite(f, n):
    y_s = [y0]
    
    times, h = np.linspace(t0, tf, n, retstep=True)
    
    for tk in times[1:]:
        yk = y_s[-1]
        next_y = yk + h * f(tk, yk)
        y_s.append(next_y)
        
    return times, y_s, h

def heun(f, n):
    y_s = [y0]
    
    times, h = np.linspace(t0, tf, n, retstep=True)
    
    for tk in times[:-1]:
        yk = y_s[-1]
        
        yk1 = yk + h * f(tk, yk)
        next_y = yk + h/2 * ( f(tk, yk) + f(tk + h, yk1) )
        y_s.append(next_y)
        
    return times, y_s, h


@lru_cache(maxsize=None)
def runge_kutta_4(f, n):
    y_s = [y0]
    
    times, h = np.linspace(t0, tf, n, retstep=True)
    
    for tk in times[:-1]:
        yk = y_s[-1]
        
        yk1 = yk + h/2 * f(tk, yk)
        yk2 = yk + h/2 * f(tk + h/2, yk1)
        yk3 = yk + h * f(tk + h/2, yk2)
        next_y = yk + h/6 * ( f(tk, yk) + 2*f(tk + h/2, yk1) + 2*f(tk + h/2, yk2) + f(tk + h, yk3) )
        y_s.append(next_y)
        
    return times, y_s, h

### Script ###

# Runge Kutta 4 de référence avec n = 10 000
_, final_y_ref, _ = runge_kutta_4(f, 10_000)
final_y_ref = final_y_ref[-1]

n_s = [10, 20, 50, 100, 200, 500, 1_000]

h_s = []
err_y_s_euler_exp = []
err_y_s_heun = []
err_y_s_runge_kutta_4 = []

for n in n_s:
    _, y_s_euler_exp, h = euler_explicite(f, n)
    _, y_s_heun, _ = heun(f, n)
    _, y_s_runge_kutta_4, _ = runge_kutta_4(f, n)
    
    h_s.append(h)
    
    err_y_euler_exp = y_s_euler_exp[-1]
    err_y_heun = y_s_heun[-1]
    err_y_runge_kutta_4 = y_s_runge_kutta_4[-1]
    
    err_y_s_euler_exp.append( abs(final_y_ref - err_y_euler_exp) )
    err_y_s_heun.append( abs(final_y_ref - err_y_heun) )
    err_y_s_runge_kutta_4.append( abs(final_y_ref - err_y_runge_kutta_4) )


# Régressions linéaires
h_s_log = np.log(np.array(h_s))

err_y_s_euler_exp_log = np.log(np.array(err_y_s_euler_exp))
err_y_s_heun_log = np.log(np.array(err_y_s_heun))
err_y_s_runge_kutta_4_log = np.log(np.array(err_y_s_runge_kutta_4))

euler_ordre, _ = np.polyfit(h_s_log, err_y_s_euler_exp_log, 1)
heun_ordre, _ = np.polyfit(h_s_log, err_y_s_heun_log, 1)
runge_kutta_ordre, _ = np.polyfit(h_s_log, err_y_s_runge_kutta_4_log, 1)

# Graphique

plt.loglog(h_s, err_y_s_euler_exp, label='Euler explicite (ordre %f)' % euler_ordre)
plt.loglog(h_s, err_y_s_heun, label='Heun (ordre %f)' % heun_ordre)
plt.loglog(h_s, err_y_s_runge_kutta_4, label='Runge Kutta 4 (ordre %f)' % runge_kutta_ordre)

plt.xlabel('log(h)')
plt.ylabel('log(err)')
plt.title("Ordres de convergence de méthodes d'approximation numériques")
plt.legend()
plt.show()


