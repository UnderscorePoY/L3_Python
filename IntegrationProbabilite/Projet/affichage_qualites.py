import numpy as np
import matplotlib.pyplot as plt
import csv
import re
from os import listdir
from os.path import isfile, join


def densite_normale_centree_reduite(x):
    return 1/np.sqrt(2*np.pi)*np.exp(-(x**2)/2)


def csv_filename_to_float_tuple(path, filename, regex):
    Q, N, p = re.match(regex, filename).groups()
    Q, N, p = int(Q), int(N), float(p)
    with open(path+filename, newline='') as csvfile:
        tirages = [float(x[0]) for x in list(csv.reader(csvfile, delimiter=','))]
        entry = {'Q': Q, "N": N, "p": p, "tirages": tirages}

    return entry


def main():
    path = "C:/Users/thoma/Documents/MEGAsync/Cours/Maths/10_1_IP/Projet/data/Bernoulli/"
    regex = r"Bernoulli_Q(\d+)_N(\d+)_p([0-9\.]+).csv"

    filenames = [f for f in listdir(path) if isfile(join(path, f))]

    list_tirages = np.array([])
    for filename in filenames:
        entry = csv_filename_to_float_tuple(path, filename, regex)
        list_tirages = np.append(list_tirages, entry)

    nb_row = int(len(list_tirages) / 2)
    nb_col = int(len(list_tirages) / nb_row)

    # Densité d'une gaussienne centree reduite
    x = np.linspace(-5, 5, 200)
    y = [densite_normale_centree_reduite(x0) for x0 in x]

    # Affichage des tirages de Bernoulli
    nb_conteneurs = 100

    plt.title(f"Emulation de la loi gaussienne centrée réduite par tirages\nsuccessifs i.i.d. d'une loi de Bernoulli")
    for i, tuple_tirages in enumerate(list_tirages):
        # Extraction des données
        Q = tuple_tirages["Q"]
        N = tuple_tirages["N"]
        p = tuple_tirages["p"]
        tirages = tuple_tirages["tirages"]

        # Création du subplot
        plt.subplot(nb_row, nb_col, i+1)
        plt.hist(tirages, nb_conteneurs, color="b", density=True, label=f"Tirages Bernoulli ({nb_conteneurs} conteneurs)")
        plt.plot(x, y, color="red", label="Densité gaussienne centrée réduite")
        plt.title(f"Nb tirages={N} | Qualité={Q}")

    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
