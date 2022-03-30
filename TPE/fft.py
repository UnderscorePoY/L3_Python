import numpy as np


def one_vector(size):
    u0 = np.ones(size)

    return u0


def s_vector(s, size):
    v = np.zeros(size)
    v[0], v[-2], v[-1] = s, s, -2*s

    return v


def main():
    D = 0.001
    T = 1.
    Nt = 20  # Number of inner points in ]0,T[
    Nx = 20  # Number of inner points in ]0,1[
    theta = 0.5
    u0 = one_vector(Nx)  # Initial condition

    dt = T/(Nt + 1)
    dx = 1/(Nx + 1)
    s = D * dt/(dx ** 2)

    # FFT
    s_vec = s_vector(s, Nx)
    s_fft_vec = np.fft.fft(s_vec)
    print(s_vec)
    print(s_fft_vec)
    print([-4*s*np.sin(2*j*np.pi/Nx) for j in range(1,Nx+1)])
    u_vec = np.fft.fft(u0)

    for _ in range(Nt):
        u_vec = (1+(1-theta)*s_vec)*(1-theta*s_vec)*u_vec
        #print(np.real(np.fft.ifft(u_vec)))


if __name__ == "__main__":
    main()




