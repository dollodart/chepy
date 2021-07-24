import numpy as np
from shomates import *
import matplotlib.pyplot as plt

gas = ShomatesGas('O2')
Trange = np.linspace(gas.Tmin, gas.Tmax, 100)

def plot_cp():
    plt.figure()
    plt.xlabel('temperature in K')
    #plt.ylabel('heat capacity in kJ/(mol K)') # not pressure dependent
    plt.ylabel('heat capacity in gas constants') # not pressure dependent
    cp = [gas.cp(T)/R for T in Trange]
    plt.plot(Trange, cp)
    plt.show()

def plot_s():
    plt.figure()
    plt.xlabel('temperature in K')
    #plt.ylabel('standard (1 bar) entropy in kJ/(mol K)')
    plt.ylabel('standard (1 bar) entropy in gas constants')
    s = [gas.s0(T)/R for T in Trange]
    plt.plot(Trange, s)
    plt.show()

def plot_h():
    plt.figure()
    plt.xlabel('temperature in K')
    #plt.ylabel('standard (1 bar) enthalpy in kJ/mol')
    plt.ylabel('standard (1 bar) enthalpy in kelvin/(5/2*R)')
    plt.title('temp needed to raise monatomic gas to same energy, though note arb. ref. state for enthalpy')
    s = [gas.h0(T)/(5*R/2) for T in Trange]
    plt.plot(Trange, s)
    plt.show()

def plot_g():
    plt.figure()
    plt.xlabel('temperature in K')
    plt.ylabel('standard (1 bar) Gibbs free energy in eV')
    g = [gas.g0(T)/96.485 for T in Trange]
    plt.plot(Trange, g)
    plt.show()

def plot_mu():
    plot_g() # g = mu, a remarkable fact because of the extensivity, partial G/partial N = g. but only problem is with state function 
    plt.ylabel('standard (1 bar) chemical potential in eV')
#    plt.figure()
#    plt.xlabel('temperature in K')
#    plt.ylabel('standard (1 bar) chemical potential in eV')
#    mu = [gas.mu0(T)/96.485 for T in Trange]
#    plt.plot(Trange, mu)
#    plt.show()

def plot_mu_diff_O():
    """Only accurate for oxygen, since the tabulated literature values are for
    oxygen, but good to show difference between gases."""
    # literature source = ??
    plt.figure()
    plt.xlabel('temperature in K')
    plt.ylabel('difference in standard (1 bar) atomic oxygen chemical potential from literature in %')
    Trange = np.array([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])  # K
    mu_lit = np.array([-0.08, -0.17, -0.27, -0.38, -0.50, -0.61, -0.73, -0.85, -0.98, -1.10])  # eV
    mu = np.array([gas.mu0(T)/96.485 for T in Trange])
    print(mu)
    print(mu_lit)
    diff = (mu / 2 - mu_lit) / mu_lit * 100.0
    plt.plot(Trange, diff, 'bo-')
    plt.show()

#plot_mu_diff()

def plot_mu_Oatom():
    plt.figure()
    plt.xlabel('$T$/K')
    plt.ylabel('$\Delta \mu_O$/eV')
    for log10pressure in np.arange(-10.,5.):
        y = [gas.delmu0(T, 10**(log10pressure))/96.485 for T in Trange]
        plt.plot(Trange, y)
    plt.legend([str(i) for i in range(-10,5,2)])
    
    plt.figure()
    plt.xlabel('$T$/K')
    plt.ylabel('$\Delta \mu_O$/eV')
    Trange2 = np.arange(500.+273.,800.+273.,1.)
    for pressure in [1.e-4*1.01325/760.,1.e-5*1.01325/760.,1.e-6*1.01325/760.]: # in bars
        y = [gas.delmu0(T, pressure)/96.485 for T in Trange2]
        plt.plot(Trange2, y)
    plt.legend(['{0:.2E} torr'.format(i) for i in [1.e-4,1.e-5,1.e-6]])
    
    plt.show()

if __name__ == '__main__':
    #plot_cp()
    #plot_s()
    #plot_h()
    #plot_g()
    #plot_mu()
#    plot_mu_diff_O()
    #plot_mu_Oatom()
