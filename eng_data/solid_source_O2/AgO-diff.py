import numpy as np
import matplotlib.pyplot as plt
from chepy.sci_data.fundamental_constants import kB, e, R
kB /= e # J -> eV
theta = 76.
B = 0.620
Dp = np.exp(-1.22)
Td = 225.
#
thickness = 1.3e-4


def lnD(T):
    s = np.log(Dp)
    s += np.log(1 - np.exp(-theta / T))
    s -= np.log(1 - np.exp(-Td / T))
    s -= 1. / 2. * np.log(2 + theta / T)
    s += theta / (2 * T)
    s -= B / (kB * T)
    return s


Trange = np.arange(298., 798., 10.)


def plot_logD():
    """
    Diffusion coefficient versus temperature, in typical Arrhenius form.
    """
    plt.xlabel('$T$/K')
    plt.ylabel(r'$\log_{10}D/(cm^{-2} \cdot s^{-1})$')
    plt.plot(Trange, 1. / np.log(10) * lnD(Trange))


def plot_logtau():
    """
    Time constant for diffusion through a given thickness as a function of
    temperature.  Derived from tau = delta^2/D where x is the thickness (more
    usually presented as delta = sqrt(D*tau) as a penetration depth).
    """
    plt.figure()
    plt.xlabel('$T$/K')
    plt.ylabel(r'$\log_{10}\tau$/s')
    plt.plot(Trange, 1. / np.log(10) * (2 * np.log(thickness) - lnD(Trange)))


def plot_log10rate():
    """Rate of oxygen liberation in packed bed. Depends on many parameters of
    the vessel geometry, catalyst density and molecular weight, and most
    difficult to measure and get accurately empirical rate constants or activation energies.
    Parameters taken from literature. """
    Router = 1.5e-3
    L = (6.5 * 2 + 3.) * 1.e-3
    V = np.pi * Router**2 / L
    packing_fraction = 0.5
    density = 7.14 / 1000.  # kg/m^3
    MW = 231.735 / 1000.  # kg/mol
    Tref = 603.  # K
    rate_constant_0 = 1.2e-3  # s^-1 at 603 K
    # kappa=(Router-thickness)/Router
    EA = np.average(
        np.array([133, 149, 118, 121, 180, 121, 151, 120]) * 1000.)  # J
    rate_constant = rate_constant_0 * np.exp(-EA / R * (1 / Trange - 1 / Tref))
    conc = packing_fraction * density / MW
    rate = V * conc * rate_constant

    plt.figure()
    plt.xlabel('$T$/K')
    plt.ylabel('Log10 Rate in mL(stp)/s')
    plt.plot(Trange, np.log10(rate) + np.log10(22.4) + 3)  # mol -> mL(stp)/s


if __name__ == '__main__':
    # plot_logD()
    # plot_logtau()
    plot_log10rate()
    plt.show()
