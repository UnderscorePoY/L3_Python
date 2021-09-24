#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math as m
import matplotlib as plt

from typing import Callable

def f(x:float) -> float:
    '''
    Fonction test à une variable `x`.
    
    Parameters :
    ------------
        x (float) : Antécédent dont on veut calculer l'image par f
        
    Returns :
    ---------
        (float) : La valeur de la fonction en `x`.
        
    '''
    return m.exp(x/5.)

def dichotomie(f:Callable, a0:float, b0:float, t:float) -> float:
    '''
    Applique l'algorithme de dichotomie à la fonction `f` dans l'intervalle [`a`,`b`], 
    et retourne un zéro éventuel (une solution à l'équation f(x)=0) avec une précision de `t`.
    
    Parameters
    ----------
        f (Callable) : Fonction dont on cherche un zéro
        a0 (float) : Borne inférieure de l'intervalle de recherche
        b0 (float) : Borne supérieure de l'intervalle de recherche
        t (float) : Tolérance d'approximation d'un zéro recherché
        
    Returns
    -------
        a (float) : Borne inférieure d'approximation d'un zéro de f
        b (float) : Borne supérieure d'approximation d'un zéro de f
        n (int) : Nombre d'itérations réalisées
    '''
    
    # Gestion des erreurs possibles
    if(a0 >= b0):
        raise ValueError("Intervalle invalide")
        
    if(t <= 0):
        raise ValueError("Tolérance invalide")

    if(f(a0)*f(b0)>0):
        raise ValueError("La fonction n'a pas de zéro sur cet intervalle")

    
    # Méthode de dichotomie
    a = a0
    b = b0
    n = 0  # Compteur d'itérations
    
    while (b-a) > t:
        n += 1
        c = (a+b) / 2.
        
        if f(a)*f(c) <= 0:
            a = a
            b = c
        else:
            a = c
            b = b
    
    return a, b, n


def point_fixe(f:Callable, x0:float, t:float) -> float:
        '''
    Applique l'algorithme du point fixe à la fonction `f` en démarrant au point `x0`, avec une tolérance de `t`.
    
    Parameters
    ----------
        f (Callable) : Fonction dont on cherche un zéro
        x0 (float) : Point de départ de la méthode
        t (float) : Tolérance d'approximation d'un zéro recherché
        
    Returns
    -------
        y (float) : Une valeur approchée d'un point fixe de f
        n (int) : Nombre d'itérations réalisées
    '''
    
    n = 1 # Compteur d'itérations
    
    x, y = x0, f(x0)
    old_delta = abs(y-x)
    
    while old_delta > t:
        n += 1
        old_delta = abs(y-x)
        x, y = y, f(y)
        #new_delta = abs(y-x)
        #if(new_delta > old_delta):
        #    raise ValueError("f n'est pas contractante autour de `x`")
        
    return y, n