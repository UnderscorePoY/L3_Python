import random

import numpy as np
from matplotlib import animation
from numpy.fft import fft, ifft
import matplotlib.pyplot as plt


class HeatEquationFFT:
    """
    A class that performs the theta-scheme on the homogeneous heat equation, without boundary conditions.
    The approximation is obtained through FFT.
    """
    def __init__(self, D, T, Nt, Nx, theta, f0=None):
        ### Logic - members at the bottom
        times, dt = np.linspace(0, T, Nt + 2, endpoint=True, retstep=True)
        xs, dx = np.linspace(0, 1, Nx + 2, endpoint=True, retstep=True)
        s = D * dt/(dx ** 2)

        CFL = 2. * (1 - 2 * theta) * s
        is_CFL = CFL <= 1

        print(f"{dt=}, {dx=}")
        print(f"{s=}, {theta=}")
        print(f"{CFL=}, {is_CFL=}")

        # Initial condition
        if f0 is None:
            f0 = lambda x: np.sin(2 * np.pi * x)
        u0_v = f0(xs[1:-1])

        # s vector
        s_v = np.zeros(Nx)
        s_v[0], s_v[1], s_v[-1] = -2. * s, s, s

        ### Members
        self.D = D
        self.T = T
        self.Nt = Nt
        self.Nx = Nx
        self.theta = theta
        self._times = times
        self.dt = dt
        self._xs = xs
        self.dx = dx
        self.s = s
        self.CFL = CFL
        self.is_CFL = is_CFL
        self.u0_v = u0_v
        self.u_v = u0_v
        self.u_fft_v = fft(u0_v)
        self.s_v = s_v
        self.s_fft_v = fft(self.s_v)

    def update(self, skip_step=1):
        """ Calculates the vector for the next time-iteration, by batches of `skip_step` iterations. """
        for _ in range(skip_step):
            self.u_fft_v *= (1. + (1. - self.theta) * self.s_fft_v) / (1. - self.theta * self.s_fft_v)

        self.u_v = np.real_if_close(ifft(self.u_fft_v))
        return self.u_v

    @property
    def xs(self):
        return self._xs[1:-1]

    @xs.setter
    def xs(self, xs):
        self._xs = xs

    @property
    def times(self):
        return self._times[1:]

    @times.setter
    def times(self, times):
        self._times = times


class Animator:
    """
    A wrapper class to animate the approximate solution of the heat equation.
    The animation starts as paused, and on-click events are supported to pause and resume it.
    """
    def __init__(self, heat_eqn: HeatEquationFFT, skip_step=1):
        self.anim = None
        self.paused = True
        self.time = 0.
        self.skip_step = skip_step
        self.heat_eqn = heat_eqn
        self.fig, self.ax = plt.subplots()
        self.time_text = self.ax.text(0.05, 0.95, '', horizontalalignment='left',
                                      verticalalignment='top', transform=self.ax.transAxes)
        self.line, = self.ax.plot(self.heat_eqn.xs, self.heat_eqn.update())
        self.ax.set_ylim(-1.2, 1.2)
        self.ax.set_xlabel('Position')
        self.ax.set_ylabel('Temperature')

        # On-click pause
        self.fig.canvas.mpl_connect('button_press_event', self.toggle_pause)

    def update(self, data):
        self.line.set_ydata(data)
        return self.line,

    def time_step(self):
        while self.time < self.heat_eqn.times[-1]:
            self.time_text.set_text('Elapsed time: {:6.2f} s'.format(self.time))
            if self.paused:
                yield self.heat_eqn.u_v
            else:
                self.time += self.heat_eqn.dt * self.skip_step
                yield self.heat_eqn.update(self.skip_step)

    def animate(self):
        self.anim = animation.FuncAnimation(
            self.fig, self.update, self.time_step, interval=1, blit=False, repeat=False)

    def toggle_pause(self, *args, **kwargs):
        self.paused = not self.paused


def condition(D, T, Nt, Nx, theta, f0=None, rand=False):
    dic = {
        "D": D,
        "T": T,
        "Nt": Nt,
        "Nx": Nx,
        "theta": theta
    }
    if f0 is not None:
        dic["f0"] = f0
    elif rand:
        dic["f0"] = lambda x: [random.uniform(-1.5, 1.5) for _ in x]

    return dic


def no_CFL(rand=False):
    """ Provides an unstable setup for the theta-scheme of the heat equation. """
    return condition(D=0.01093, T=15., Nt=2_000, Nx=100, theta=0.2, rand=rand)


def CFL(rand=False):
    """ Provides a stable setup for the theta-scheme of the heat equation. """
    return condition(D=0.01080, T=15., Nt=2_000, Nx=100, theta=0.2, rand=rand)


def CFL_reg(rand=False):
    """ Provides a stable setup for the theta-scheme of the heat equation. """
    return condition(D=0.01080, T=15., Nt=2_000, Nx=100, theta=0.7, rand=rand)


def main():
    random.seed(0xA1957)
    conditions = no_CFL(rand=False)
    heat_eqn = HeatEquationFFT(**conditions)
    animator = Animator(heat_eqn, skip_step=5)
    animator.animate()
    plt.show()


if __name__ == "__main__":
    main()
