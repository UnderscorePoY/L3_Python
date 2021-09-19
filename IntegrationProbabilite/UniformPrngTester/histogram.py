import numpy as np
import math
import random as rd

import matplotlib.pyplot as plt
import matplotlib.animation as animation

# SETTINGS
DRAW_NB = 10_000
SUBDIVISION_NB = 10

# Code copied from https://matplotlib.org/stable/gallery/animation/animated_histogram.html

# Fixing bin edges
HIST_BINS = np.linspace(0, 1, SUBDIVISION_NB + 1)

# histogram our data with numpy
draws = [rd.uniform(0.0, 1.0) for _ in range(DRAW_NB)]
n, _ = np.histogram(draws[0:0], HIST_BINS)


def prepare_animation(bar_container):
    def animate(frame_number):
        if frame_number == 0:
            return bar_container.patches

        # simulate new data coming in
        n, _ = np.histogram(draws[0:frame_number], HIST_BINS)
        for count, rect in zip(n, bar_container.patches):
            rect.set_height(count / frame_number)

        return bar_container.patches

    return animate


fig, ax = plt.subplots()
_, _, bar_container = ax.hist(draws, HIST_BINS, lw=1,
                              ec="blue", fc="purple", alpha=0.5)
ax.set_ylim(top=2.0 / SUBDIVISION_NB)  # set safe limit to ensure that all data is visible.
ani = animation.FuncAnimation(fig, prepare_animation(bar_container), DRAW_NB, interval=1,
                              repeat=False, blit=True)

plt.show()
