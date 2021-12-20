from affichage_qualites import csv_filename_to_float_tuple, densite_normale_centree_reduite
import numpy as np
import matplotlib.pyplot as plt


def main():
    path = "C:/Users/thoma/Documents/MEGAsync/Cours/Maths/10_1_IP/Projet/data/Bernoulli/"
    filename = "Bernoulli_Q10000_N10000_p0.5.csv"
    regex = r"Bernoulli_Q(\d+)_N(\d+)_p([0-9\.]+).csv"

    tuple_tirages = csv_filename_to_float_tuple(path, filename, regex)

    # Extraction des données
    Q = tuple_tirages["Q"]
    N = tuple_tirages["N"]
    p = tuple_tirages["p"]
    tirages = tuple_tirages["tirages"]

    # Densité d'une gaussienne centree reduite
    x = np.linspace(-5, 5, 200)
    y = [densite_normale_centree_reduite(x0) for x0 in x]

    # Affichage des tirages de Bernoulli
    list_nb_conteneurs = [10, 50, 100, 500, 1000, 5000]

    nb_row = 3
    nb_col = 2

    for i, nb_conteneurs in enumerate(list_nb_conteneurs):
        # Création du subplot
        plt.subplot(nb_row, nb_col, i+1)
        plt.hist(tirages, nb_conteneurs, color="b", density=True, label=f"Tirages Bernoulli")
        plt.plot(x, y, color="red", label="Densité gaussienne centrée réduite")
        plt.title(f"Nb conteneurs={nb_conteneurs}")

    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
