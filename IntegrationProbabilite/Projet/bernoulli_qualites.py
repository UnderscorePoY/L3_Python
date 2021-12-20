from random import random as uniform
import numpy as np
import matplotlib.pyplot as plt


def bernoulli(p):
    return 1 if uniform() <= p else 0


def normale_centree_reduite_par_bernoulli(p, N):
    esperance = p
    variance = p*(1-p)
    ecart_type = np.sqrt(variance)

    s = 0
    for i in range(N):
        s += bernoulli(p)
    moyenne = s / N

    z = np.sqrt(N)/ecart_type * (moyenne - esperance)

    return z


path = "C:/Users/thoma/Documents/MEGAsync/Cours/Maths/10_1_IP/Projet/data/Bernoulli/"
p = 0.5
produit = 100_000_000
Q = 10
nb_iterations = int(np.log10(produit / Q))
for _ in range(nb_iterations):
    nb_tirages = int(produit / Q)

    tirages = [normale_centree_reduite_par_bernoulli(p, Q) for _ in range(nb_tirages)]

    np.savetxt(path+f'Bernoulli_Q{Q}_N{nb_tirages}_p{p}.csv', tirages, delimiter=',')
    Q *= 10
