#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 09:30:34 2021

@author: thomas.bescond
"""

import numpy as np
import matplotlib.pyplot as plt


# Formules élémentaires :
# - RAG     : rectangle à gauche
# - RAD     : rectangle à droite
# - PM      : point milieu
# - TZ      : trapèzes
# - Simpson : Simpson
        
def RAG_elem(f, a, b):
    return (b-a)*f(a)

def RAD_elem(f, a, b):
    return (b-a)*f(b)

def PM_elem(f, a, b):
    return (b-a)*f((a+b)/2)

def TZ_elem(f, a, b):
    return (b-a)*(1/2*(f(a)+f(b)))

def Simpson_elem(f, a, b):
    return (b-a)*(1/6*f(a)+2/3*f((a+b)/2)+1/6*f(b))



# Méthodes composées

def gen_comp(f, elem, noeuds):
    """ Crée une formule de quadrature composée basée sur une formule élémentaire."""
    
    S = 0.
    for i in range(len(noeuds)-1):
        x, y = noeuds[i], noeuds[i+1]
        S += elem(f, x, y)
    
    return S

def RAG_comp(f, noeuds):
    return gen_comp(f, RAG_elem, noeuds)

def RAD_comp(f, noeuds):
    return gen_comp(f, RAD_elem, noeuds)
        
def PM_comp(f, noeuds):
    return gen_comp(f, PM_elem, noeuds)

def TZ_comp(f, noeuds):
    return gen_comp(f, TZ_elem, noeuds)

def Simpson_comp(f, noeuds):
    return gen_comp(f, Simpson_elem, noeuds)


def TZ_comp_opti(f, noeuds):
    """ Formule des trapèzes optimisée pour limiter le nombre d'évaluations de la fonction f.
    2n => n+1 évaluations."""
    
    S = 0
    n = len(noeuds)
    vals = [f(x) for x in noeuds] # Cache les valeurs de f en les noeuds
    
    # terme initial
    S = 1/2*(noeuds[1]-noeuds[0])*vals[0]
    
    # terme final
    if n > 2:
        S += 1/2*(noeuds[n-1]-noeuds[n-2])*vals[n-1]
    
    # termes intermédiaires
    if n > 3:
        for i in range(1, n-1):
            S += (noeuds[i+1]-noeuds[i])*vals[i]
            
    return S

def Simpson_comp_opti(f, noeuds):
    """ Formule de Simpson optimisée pour limiter le nombre d'évaluations de la fonction f.
    3n => 2n+1 évaluations."""
    
    S = 0
    n = len(noeuds)
    vals = [f(x) for x in noeuds] # Cache les valeurs de f en les noeuds
    vals_mil = [f((noeuds[i]+noeuds[i+1])/2) for i in range(n-1)] # Cache les valeurs de f en les milieux des noeuds
    
    # terme initial
    S = 1/6*(noeuds[1]-noeuds[0])*vals[0]
    
    # termes des milieux
    for i in range(n-1):
       S += 2/3*(noeuds[i+1]-noeuds[i])*vals_mil[i]
    
    # terme final   
    if n > 2:
        S += 1/6*(noeuds[n-1]-noeuds[n-2])*vals[n-1]
    
    # termes intermédiaires
    if n > 3:
        for i in range(1, n-1):
            S += 1/3*(noeuds[i+1]-noeuds[i])*vals[i]
        
    return S


# Utils

def verif_noeuds(noeuds):
    """ Vérifie que les noeuds d'une subdivision sont correctement ordonnés, du plus petit
    au plus grand."""
    
    for i in range(len(noeuds)-1):
        x, y = noeuds[i], noeuds[i+1]
        assert x < y, "a n'est pas strictement inférieur à b"


class Test_Env:
    """ Environnement de test compilant les calculs d'intégrales à partir des différentes 
    méthodes de quadrature composée"""
    
    def __init__(self, func, a, b, noeuds):
        self.f = func.f
        self.F = func.F
        self.a = a
        self.b = b
        self.noeuds = noeuds
        
    def run(self):
        exacte = self.F(b) - self.F(a)
        rag_comp = RAG_comp(self.f, noeuds)
        rad_comp = RAD_comp(self.f, noeuds)
        pm_comp = PM_comp(self.f, noeuds)
        tz_comp = TZ_comp(self.f, noeuds)
        simpson_comp = Simpson_comp(self.f, noeuds)
        
        print("Environnement :")
        print("\tIntervalle d'étude [a,b] : [{},{}]".format(self.a, self.b))
        print("\tNombre de noeuds : n = ", len(self.noeuds))
        print("\tNoeuds : ", self.noeuds)
        print()
        
        print("Calculs d'intégrales :")
        print("\tValeur exacte : ", exacte)
        print("\tRAG : ", rag_comp)
        print("\tRAD : ", rad_comp)
        print("\tPoint milieu : ", pm_comp)
        print("\tTrapèzes : ", tz_comp)
        print("\tSimpson : ", simpson_comp)
        
    def __rel_error(calc, expected):
        return 
    
class Func:
    """ Fonction comprenant une fonction f et une primitive F"""
    
    def __init__(self, f, F):
        self.f = f
        self.F = F

def uniform(a, b, n):
    """ Crée une liste de n noeuds uniformément répartis du segment [a,b], bornes comprises."""
    lst = [a+(b-a)*i/(n-1) for i in range(n)]
    return lst



# SCRIPTS

'''
# Test de toutes les méthodes composées sur une fonction

f = Func(lambda x: 1, 
         lambda x: x)

g = Func(lambda x: 2*x, 
         lambda x: x**2)

h = Func(lambda x: 1/x,
         lambda x: np.log(x))

a, b = 1, 2
n = 10
noeuds = uniform(a, b, n)
verif_noeuds(noeuds)

env_h = Test_Env(h, a, b, noeuds)
env_h.run()
'''


# Test d'application de la formule des rectangles à gauches pour un nombre croissant de noeuds

def j(x):
    return x**2

L = [10, 20, 30, 40, 100, 200, 400, 1000, 2000]
a, b = 0, 1
target = 1/3 # x**2 entre 0 et 1

# => rectangles à gauche
results_RAG = []

for n in L:
    noeuds = uniform(a, b, n)
    results_RAG.append(RAG_comp(j, noeuds))

errors_RAG = [abs(target-x) for x in results_RAG]
# print(errors_RAG)

# Pas de la subdivision en fonction de l'erreur
# plt.loglog((b-a)/np.array(L), errors_RAG)

# => Simpson

# TODO : FIX
results_Simpson = []

for n in L:
    noeuds = uniform(a, b, n)
    results_Simpson.append(Simpson_comp_opti(j, noeuds))

errors_Simpson = [abs(target-x) for x in results_Simpson]
print(errors_Simpson)

# Pas de la subdivision en fonction de l'erreur
plt.loglog((b-a)/np.array(L), errors_Simpson)

'''
# Vérifications des formules composées optimisées

def j(x):
    return x**2

a, b = 0, 1
n = 10
noeuds = uniform(a, b, n)
print("Vérification des formules des trapèzes")
print("Méthode non optimisée : ", TZ_comp(j, noeuds))
print("Méthode optimisée : ", TZ_comp_opti(j, noeuds))

print("Vérification des formules de Simpson")
print("Méthode non optimisée : ", Simpson_comp(j, noeuds))
print("Méthode optimisée : ", Simpson_comp_opti(j, noeuds))
'''
