import matplotlib.pyplot as plt
import numpy as np
import sys
from chepy.sci_data.chem_pot_gases import ShomatesGas
from chepy.sci_data.fundamental_constants import R

with open('data.csv', 'r') as _:
    lines = _.readlines()

Tmin = 1000000
Tmax = -Tmin
dct = dict()
for l in lines:
    try:
        solute, A, B, C, E, F, G, H, TminK, TmaxK = l.split(',')
        consts = (A, B, C, E, F, G, H)
        dct[solute] = tuple(float(c) for c in consts)
        if solute in ['O2', 'N2']: # gases of interest
            TminK, TmaxK = float(TminK), float(TmaxK)
            if TminK < Tmin:
                Tmin = TminK
            if TmaxK > Tmax:
                Tmax = TmaxK
    except ValueError:
        print('header', l)

T0 = 298.15  # K
P0 = 1  # bar

Trange = np.arange(Tmin, Tmax, 10.)

# water properties

Pc = 22.064 * 10.  # bar
Tc = 647.096  # K
rhoc = 322  # kg/m^3


def density_l(T):
    Tr = T / Tc
    tau = 1 - Tr
    b1 = 1.99274064
    b2 = 1.09965342
    b3 = -0.510839303
    b4 = -1.75493479
    b5 = -45.5170352
    b6 = -6.74694450e5
    return rhoc * (1 + b1 * tau**(1 / 3) + b2 * tau**(2 / 3) + b3 * tau **
                   (5 / 3) + b4 * tau**(16 / 3) + b5 * tau**(43 / 3) + b6 * tau**(110 / 3))


def vapor_pressure(T):
    Tr = T / Tc
    tau = 1 - Tr
    a1 = -7.85951783
    a2 = 1.84408259
    a3 = -11.7866497
    a4 = 22.6807411
    a5 = -15.9618719
    a6 = 1.80122502
    lnp = np.log(Pc) + 1 / Tr * (a1 * tau + a2 * tau**1.5 + a3 *
                                 tau**3 + a4 * tau**3.5 + a5 * tau**4 + a6 * tau**7.5)
    return np.exp(lnp)


def plot_water_properties():
    # checking properties of the solvent
    plt.figure()
    plt.xlabel('$T$/K')
    plt.ylabel(r'$\rho$/(kg/m^3)')
    plt.plot(Trange, [density_l(T) for T in Trange])
    plt.legend(['H2O'])

    plt.figure()
    plt.xlabel('$T$/K')
    plt.ylabel('$p^*$/bar')
    plt.plot(Trange, [np.log10(vapor_pressure(T)) for T in Trange])
    plt.legend(['H2O'])


def KD(T, solute):
    '''Return y/x in the dilute limit.'''
    Tr = T / Tc
    tau = 1. - Tr
    f = density_l(T) / rhoc - 1.
    q = -0.023767
    A, B, C, E, F, G, H = dct[solute]
    lnKD = q * F + E / T * f + \
        (F + G * tau**(2 / 3) + H * tau) * np.exp((T0 - T) / 100.)
    return np.exp(lnKD)


def henrys_constants(T, solute):
    lnp = np.log(vapor_pressure(T))
    Tr = T / Tc
    tau = 1. - Tr
    A, B, C, E, F, G, H = dct[solute]
    lnH = lnp + A / Tr + B * tau**0.355 / Tr + C * Tr**-.41 * np.exp(tau)
    return np.exp(lnH)


def plot_source_plots():
    """
    Reproduce the source plots (note source plots are for CO2 and H2).
    """

    MW = 1. / 18. * 1000.  # mol/kg

    plt.figure()
    plt.xlabel(r'$\rho_l(T) - \rho_{l,c}$ in mol/dm$^3$')
    plt.ylabel(r'$(T\ln K_D)$/K')
    x = [(density_l(T) - rhoc) * MW / 1.e3 for T in Trange]
    plt.xlim((0,max(x)*1.1))
    my = []
    for solute in 'CO2', 'H2':
        y = [T * np.log(KD(T, solute)) for T in Trange]
        plt.plot(x, y)
        my.append(max(y))
    plt.ylim((0,max(my)*1.1))
    plt.legend(['CO2', 'H2'])

def plot_log10_henrys():
    plt.figure()
    for solute in 'O2', 'N2':
        y = [np.log10(henrys_constants(T, solute)) for T in Trange]
        plt.plot(Trange, y)
    plt.xlabel('$T$/K')
    plt.ylabel(r'$\log_{10} y(P/bar)/x$')
    plt.legend(['O2', 'N2'])

def plot_log10_KD():
    plt.figure()
    for solute in 'O2', 'N2':
        plt.plot(Trange, [np.log10(KD(T, solute)) for T in Trange])
    plt.xlabel('$T$/K')
    plt.ylabel(r'$\log_{10}\lim_{x\to 0}y/x$')
    plt.legend(['O2', 'N2'])

# gas properties including equilibrium
o2 = ShomatesGas('O2')
n2 = ShomatesGas('N2')

mugO2 = [o2.mu0(T) for T in Trange]
mugN2 = [n2.mu0(T) for T in Trange]

HO2T0 = henrys_constants(T0, 'O2')
HN2T0 = henrys_constants(T0, 'N2')
# inverse henrys constants is solubilities, hence negatives on logarithms
# of its terms
henO2 = [-R * T * np.log(henrys_constants(T, 'O2') / HO2T0) for T in Trange]
henN2 = [-R * T * np.log(henrys_constants(T, 'N2') / HN2T0) for T in Trange]
mulO2 = [henO2[c] + mugO2[c] for c in range(len(Trange))]
mulN2 = [henN2[c] + mugN2[c] for c in range(len(Trange))]

def plot_specific_free_energies():
    plt.figure()
    plt.xlabel('$T$/K')
    plt.ylabel(r'$\mu$/(kJ/mol)')
    plt.plot(Trange, mugO2, 'b--')
    plt.plot(Trange, mulO2, 'b-')
    plt.plot(Trange, mugN2, 'g--')
    plt.plot(Trange, mulN2, 'g-')
    plt.plot(Trange, henO2, 'b-.')
    plt.plot(Trange, henN2, 'g-.')
    plt.legend([r'$\mu^\theta_{g,O_2}$',
                r'$\mu^\theta_{l,O_2}$',
                r'$\mu^\theta_{g,N_2}$',
                r'$\mu^\theta_{l,N_2}$',
                r'$-RT\ln H_{O_2}(T)/H^\ominus_{O_2}$',
                r'$-RT\ln H_{N_2}(T)/H^\ominus_{N_2}$'])


def plot_temperature_derivatives_specific_free_energies():
    plt.figure()
    plt.xlabel('$T$/K')
    plt.ylabel(r'$d\mu/dT$/(kJ/mol)')
    dT = Trange[1] - Trange[0]  # this is constant
    Trange_d = Trange[1:]
    plt.plot(Trange_d, np.diff(mugO2) / dT, 'b--')
    plt.plot(Trange_d, np.diff(mulO2) / dT, 'b-')
    plt.plot(Trange_d, np.diff(mugN2) / dT, 'g--')
    plt.plot(Trange_d, np.diff(mulN2) / dT, 'g-')
    dhenO2dT = np.diff(henO2) / dT
    dhenN2dT = np.diff(henN2) / dT
    plt.plot(Trange_d, np.diff(henO2) / dT, 'b-.')
    plt.plot(Trange_d, np.diff(henN2) / dT, 'g-.')
    plt.legend([r'$\frac{d}{dT} \mu^\theta_{g,O_2}$',
                r'$\frac{d}{dT} \mu^\theta_{l,O_2}$',
                r'$\frac{d}{dT} \mu^\theta_{g,N_2}$',
                r'$\frac{d}{dT} \mu^\theta_{l,N_2}$',
                r'$\frac{d}{dT} -RT\ln H_{O_2}(T)/H^\ominus_{O_2}$',
                r'$\frac{d}{dT} -RT\ln H_{N_2}(T)/H^\ominus_{N_2}$'])
    amin = np.argmin(abs(dhenO2dT))
    plt.plot(Trange_d[amin], dhenO2dT[amin], 'ko')
    titlestr = f'O2 inversion = {Trange_d[amin]} deg. C'
    amin = np.argmin(abs(dhenN2dT))
    plt.plot(Trange_d[amin], dhenN2dT[amin], 'ko')
    titlestr += f'\nN2 inversion = {Trange_d[amin]} deg. C'
    plt.title(titlestr)


def plot_temperature_derivatives_henrys_constants():
    H_O2 = henrys_constants(Trange, 'O2')
    H_N2 = henrys_constants(Trange, 'N2')
    dT = Trange[1] - Trange[0]
    Trange_d = Trange[1:]
    dH_O2dT = np.diff(H_O2) / dT
    dH_N2dT = np.diff(H_N2) / dT
    plt.plot(Trange_d, dH_O2dT)
    plt.plot(Trange_d, dH_N2dT)
    plt.legend(['O2', 'N2'])
    amin = np.argmin(abs(dH_O2dT))
    titlestr = f'O2 inversion = {Trange_d[amin]} deg. C'
    plt.plot(Trange_d[amin], dH_O2dT[amin], 'ko')
    amin = np.argmin(abs(dH_N2dT))
    titlestr += f'\nN2 inversion = {Trange_d[amin]} deg. C'
    plt.plot(Trange_d[amin], dH_N2dT[amin], 'ko')
    plt.ylabel('$dH/dT$ (...)')
    plt.xlabel('$T$/K')
    plt.title(titlestr)


if __name__ == '__main__':
    #plot_source_plots()
    plot_temperature_derivatives_henrys_constants()
    plot_temperature_derivatives_specific_free_energies()
    plt.show()
