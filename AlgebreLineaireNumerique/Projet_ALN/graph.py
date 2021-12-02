import matplotlib.pyplot as plt
import numpy as np

h = 0.01
N = int(5.0/h)

l = [i*h for i in range(N)]

plt.plot(l, [x*x for x in l])
for i in range(5):
    x_rect = [i, i, i+1, i+1, i] # abscisses des sommets
    y_rect = [0   , ((2*i+1)/2)**2, ((2*i+1)/2)**2  , 0     , 0   ] # ordonnees des sommets
    plt.plot(x_rect, y_rect,"r")
plt.show()
