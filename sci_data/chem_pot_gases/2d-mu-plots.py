from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import sys
from shomates import *
import numpy as np

h2 = ShomatesGas('H2')
o2 = ShomatesGas('O2')

#Tmin = max(h2.Tmin, o2.Tmin)
#Tmax = min(h2.Tmax, o2.Tmax)
#Trange = np.arange(Tmin, Tmax, 5.)
Tmin = 400.  # deg. C
Tmax = 1400.  # deg. C
Trange = np.arange(Tmin + 273.15, Tmax + 273.15, 5.)  # K

log10Pmin = -13  # bar
log10Pmax = 1  # bar
Prange = 10.**(np.arange(log10Pmin, log10Pmax, 0.2))  # bar

mu_H = np.zeros((len(Trange), len(Prange)))
mu_O = np.zeros((len(Trange), len(Prange)))

for c, T in enumerate(Trange):
    muo = o2.mu0(T)
    muh = h2.mu0(T)
    for d, P in enumerate(Prange):
        mu_O[c, d] = (muo + R*T*np.log(P/P0)) / 96.482 / 2.
        mu_H[c, d] = (muh + R*T*np.log(P/P0)) / 96.482 / 2.

x, y = np.meshgrid(Trange, np.log10(Prange), indexing='ij')

def plot_O_H_3d():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf1 = ax.plot_surface(x, y, mu_O)
    surf2 = ax.plot_surface(x, y, mu_H)
    surf1._facecolors2d = surf1._facecolors3d
    surf1._edgecolors2d = surf1._edgecolors3d
    surf2._facecolors2d = surf2._facecolors3d
    surf2._edgecolors2d = surf2._edgecolors3d
    ax.set_xlabel('$T$/K')
    ax.set_ylabel('$\mu$/eV')
    ax.legend(['O', 'H'])
    return fig, ax

def plot_O_H_contour():
    fig, axs = plt.subplots(nrows=2,ncols=2)

    #levels = np.arange(np.round(np.min(mu_O), 1), np.round(np.max(mu_O), 1), 0.1)
    levels = None
    for ax in axs[0,0], axs[1,1]:
        CS = ax.contour(x, y, mu_O, levels=levels)
        ax.clabel(CS, inline=1, fontsize=10, fmt='%1.1f')
        ax.set_title('Oxygen Chemical Potential in eV')

    #levels = np.arange(np.round(np.min(mu_H), 1), np.round(np.max(mu_H), 1), 0.1)
    levels = None
    for ax in axs[0,1], axs[1,0]:
        CS = ax.contour(x, y, mu_H, levels=levels)
        ax.clabel(CS, inline=1, fontsize=10, fmt='%1.1f')
        ax.set_title('Hydrogen Chemical Potential in eV')

    for ax in np.ravel(axs):
        ax.set_xlabel('$T$/K')
        ax.set_ylabel(r'$\log_{10} P/bar$')
        a, b = 1000. + 273.15, np.log10(1)
        ax.plot(a, b, 'ko')
        ax.text(a, b, f'T={a} deg.C, P={10**b:.2E}bar')
        a, b = 500. + 273.15, np.log10(1e-8)
        ax.plot(a, b, 'ko')
        ax.text(a, b, f'T={a} deg.C, P={10**b:.2E}bar')

    return fig, axs

def plot_contour(mcul, Tbounds, log10Pbounds, fineness=0.1):
    '''
    inputs:
    mcul: molecular formula
    Tbounds: bounds of temperature to be plotted, in K
    log10Pbounds: bounds of pressure to be plotted, in bar
    fineness: contour spacing in eV

    outputs: plot of per molecule chemical potential of gas phase
    '''

    gas = ShomatesGas(mcul)
    if Tbounds is None:
        Tmin, Tmax = gas.Tmin, gas.Tmax
    else:
        Tmin, Tmax = Tbounds
    Trange = np.arange(Tmin, Tmax, 5.)
    log10Pmin, log10Pmax = log10Pbounds
    Prange = 10.**(np.arange(log10Pmin, log10Pmax, 1))  # bar
    mu_s = np.zeros((len(Trange), len(Prange)))
    for c, T in enumerate(Trange):
        mu0 = gas.mu0(T)
        for d, P in enumerate(Prange):
            mu = (mu0 + R*T*np.log(P/P0))/96.482
            mu_s[c, d] = mu

    x, y = np.meshgrid(Trange, np.log10(Prange), indexing='ij')

    fig, ax = plt.subplots()
    levels = np.arange(np.round(np.min(mu_s), 1), np.round(np.max(mu_s), 1), fineness)
    CS = ax.contour(x, y, mu_s, levels=levels)
    ax.clabel(CS, inline=1, fontsize=10, fmt='%1.1f')
    ax.set_title('{0} Chemical Potential in eV'.format(mcul))
    ax.set_xlabel('$T$/K')
    ax.set_ylabel(r'$\log_{10} P/bar$')

    return fig, ax


if __name__ == '__main__':
    fig, ax = plot_contour('O2', [400 + 273.15, 1100 + 273.15], [-13, 1], fineness=.2)
    plt.show()
