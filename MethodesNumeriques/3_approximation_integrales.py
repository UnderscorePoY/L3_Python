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
    # TODO : FIX !!!!!!!
    lst = [a+(b-a)*i/(n-1) for i in range(n)]
    return lst


f = Func(lambda x: 1, 
         lambda x: x)

g = Func(lambda x: 2*x, 
         lambda x: x**2)

h = Func(lambda x: 1/x,
         lambda x: np.log(x))


# Script
'''
a, b = 1, 2
n = 10
noeuds = [a+(b-a)*i/n for i in range(n+1)]
verif_noeuds(noeuds)

env_h = Test_Env(h, a, b, noeuds)
env_h.run()
'''

def j(x):
    return x**2

L = [10, 20, 30, 40, 100, 200, 400, 1000, 2000]
a, b = 0, 1

results_RAG = []
for n in L:
    noeuds = [a+(b-a)*i/(n-1) for i in range(n)]
    results_RAG.append(RAG_comp(j, noeuds))
    
print(results_RAG)
    

    
    
    
    