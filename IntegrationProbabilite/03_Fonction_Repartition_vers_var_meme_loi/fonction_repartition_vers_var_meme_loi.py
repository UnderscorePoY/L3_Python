from typing import Callable
import random, math


def repartition_bernoulli(t: float) -> int:
    """
    Fonction de répartition associée à la loi de Bernoulli de paramètre p.
    p doit être déclaré en variable globale (oulalah c'est pas bien).
    """
    if p <= 0 or p >=1:
        raise ValueError("Paramètre p invalide : valeur dans ]0,1[ attendue.")
        
    # Graphe de la fonction de répartition de la loi de Bernoulli
    
    #                 (1) |         -------------
    #                     |         °
    #                     |         °
    #               (1-p) ----------c                   
    #                     |         °
    # --------------------c_________°____________
    #                     0         1
    
    f = 0
    if t < 0:
        f = 0
    elif t < 1:
        f = 1-p
    else:
        f = 1
        
    return f


def G(u: float, F: Callable, t_min=-10, t_max=10) -> float:
    # On cherche la plus petite valeur de t telle que F(t) >= u.
    # La recherche se fait de façon itérative dans une unique direction pour éviter les écueils d'arrondis
    # dans la recherche par dichotomie, bien que cette dernière soit plus rapide.
    
    EPSILON = 10**-3
    
    a, b = t_min-EPSILON, t_max+EPSILON
    
    Fa, Fb = F(a)-u, F(b)-u
    # print(u, Fa, Fb)
    
    if Fa*Fb > 0:
        raise ValueError("G(u) n'est pas trouvable sur cet intervalle.")
    
    c = (a+b)/2
    Fc = F(c)-u
    if Fa*Fc <= 0:
        while Fa*Fc <= 0:
            c -= EPSILON
            Fc = F(c)-u
        c += EPSILON
    else:
        while Fc*Fb <= 0:
            c += EPSILON
            Fc = F(c)-u
            
    return c
    

# Test répartition Bernoulli

# random.seed(0x3141592)  # Pour la reproductibilité

p = 0.5
NB_LANCERS = 1_000
resultats = [0, 0]  # Une tirage de Bernoulli ne retourne que 0 ou 1
t_min = 0
t_max = 1

for i in range(NB_LANCERS):
    r = random.random()
    
    t = G(r, repartition_bernoulli, t_min, t_max)
    
    resultats[int(t)] += 1
    
    
esperance = resultats[1] / NB_LANCERS
variance = resultats[1] / NB_LANCERS - esperance**2
ecart_type = math.sqrt(variance)

esperance_th = p
variance_th = p*(1-p)
ecart_type_th = math.sqrt(variance_th)

print(resultats)
print("Esperance : {}, Esperance théorique : {}".format(esperance, esperance_th))
print("Variance : {}, Variance théorique : {}".format(variance, variance_th))
print("Ecart-type : {}, Ecart-type théorique : {}".format(ecart_type, ecart_type_th))
