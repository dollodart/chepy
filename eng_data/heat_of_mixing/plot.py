import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from scipy.integrate import simpson

hs = pd.read_csv('enthalpies-of-solution.csv', delimiter=',')
columns = hs.columns
names = [col.replace('hs', '') for col in columns]

def plot_hs():
    plt.title('Heat of Solution')
    plt.xlabel('$n_{H_2O}$ in mol')
    plt.ylabel(r'$\Delta\tilde{h}_s$ in kJ/mol solute')

    x = hs['nH2O']
    for col in columns[1:]:
        y = hs[col]
        plt.plot(x, y, 'o-')

    plt.legend(names[1:])

def plot_hm():
    plt.title('Heat of Mixing')
    plt.xlabel('$x_{i}$')
    plt.ylabel(r'$\Delta h_{mix}$ in kJ/mol solution')

    x = 1. / (1. + hs['nH2O'])
    for col in columns[1:]:
        y = hs[col] * x
        plt.plot(x, y, 'o-')

    plt.legend(names[1:])

df = pd.read_csv('koretsky-6.11-90.dat')
x = np.linspace(0, 1, 101)
interpolator = CubicSpline(df['x'], df['dhmix'])

def plot_CHCl3_CH3OH_hm():
    # reproduce Koretsky 6.11
    plt.plot(df['x'], df['dhmix'], 'o-', label='data')
    plt.plot(x, interpolator(x), label='cubic spline interp')
    plt.xlabel('$x(CHCl_3)$')
    plt.ylabel('$\Delta h_{mix}$ in J/mol')
    plt.legend()

def plot_CHCl3_CH3OH_hs():
    # derived from Koretsky 6.11

    df['n1'] = (1 - df['x'])/df['x'] # chloroform is solute (x)
    df['dhs1'] = df['dhmix']*(1 + df['n1'])
    bl1 = df['n1'] >= 1
    df['n2'] = df['x']/(1 - df['x']) # methanol is solute (1 - x)
    df['dhs2'] = df['dhmix']*(1 + df['n2'])
    bl2 = df['n2'] >= 1

    plt.plot(df['n1'][bl1], df['dhs1'][bl1], 'ko-', label='solvent=methanol')
    plt.plot(df['n2'][bl2], df['dhs2'][bl2], 'bo-', label='solvent=chloroform')
    plt.xlabel('n solvent')
    plt.ylabel('heat of solution in J/mol')

    n1 = (1 - x)/x
    dhs1 = interpolator(x)*(1 + n1)
    bl1 = n1 >= 1

    n2 = x/(1-x)
    dhs2 = interpolator(x)*(1 + n2)
    bl2 = n2 >= 1

    plt.plot(n1[bl1], dhs1[bl1], 'k--')
    plt.plot(n2[bl2], dhs2[bl2], 'b--')

    plt.legend()

def dHdnH2SO4(x):
    # isobaric, isothermal partial molar property (moles H2O are constant)
    # x is composition of acid, in kJ/mol
    # non-zero partial molar enthalpy at zero composition is expected (derivative of extensive enthalpy)
    return 1.596 - 74.40*(1-x)**2 + 83.48*x*(1-x)**2

def dHdnH2O(x):
    # isobaric, isothermal partial molar property (moles H2SO4 are constant)
    # x is composition of acid, kJ/mol
    # non-zero partial molar enthalpy at unity composition is expected (derivative of extensive enthalpy)
    return 1.591 - 74.40*x**2 + 41.74*x**2*(1-2*(1-x))

def plot_H2SO4_H2O_hpart():
    # Koretsky 6.13
    x = np.arange(0, 1, 0.02)
    y1 = dHdnH2SO4(x)
    y2 = dHdnH2O(x)
    plt.plot(x, y1, label='H2SO4')
    plt.plot(x, y2, label='H2O')
    plt.legend()
    plt.xlabel('Composition H2SO4')
    plt.ylabel('Partial Molar Enthalpy')

def approx_equal(a, b):
    a = abs(a)
    b = abs(b)
    if b < a:
        a, b = b, a 

    d = b - a
    s = a + b
    err = 2 * d / s

    if err < .0001:
        return True
    return False

def check_tdpath_invar(na_final, nw_final):

    xaf = na_final / (na_final + nw_final)
    xwf = 1 - xaf

    # path 1: add acid to water
    xa1 = np.linspace(.01, xaf, 200)
    na1 = xa1/(1-xa1) * nw_final
    dQdna1 = dHdnH2SO4(xa1)
    Q1 = simpson(dQdna1, na1)
    n1 = nw_final + na1

    # path 2: add water to acid
    xw2 = np.linspace(.01, xwf, 200)
    nw2 = xw2/(1-xw2) * na_final
    dQdnw2 = dHdnH2O(1-xw2) # both functions of xa
    Q2 = simpson(dQdnw2, nw2)
    n2 = na_final + nw2

    if not approx_equal(n1[-1], n2[-1]):
        raise Exception('end number of moles different', n1[-1], n2[-1])
    if not approx_equal(na1[-1], na_final):
        raise Exception('for path 1 end number of acid incorrect', na1[-1], na_final)
    if not approx_equal(n1[-1] - na1[-1], nw_final):
        raise Exception('for path 1 end number of water incorrect', n1[-1] - na1[-1], nw_final)
    if not approx_equal(nw2[-1], nw_final):
        raise Exception('for path 2 end number of water incorrect', nw2[-1], nw_final)
    if not approx_equal(n2[-1] - nw2[-1], na_final):
        raise Exception('for path 2 end number of acid incorrect', n2[-1] - nw2[-1], na_final)
    if not approx_equal(xa1[-1], xaf):
        raise Exception('composition for path 1 incorrect', xa1[-1], xaf)
    if not approx_equal(xw2[-1], xwf):
        raise Exception('composition for path 2 incorrect', xw2[-1], xwf)
    if not approx_equal(Q1, Q2):
        raise Exception(f'heats evolved differ, {Q1:.2E} kJ/mol != {Q2:.2E} kJ/mol')

def plot_td_path(nw_final, na_final):

    # add acid to water
    xfinal = na_final / (na_final + nw_final)
    x = np.linspace(.01, xfinal, 200)
    na = x/(1-x) * nw_final
    sa = np.argsort(na)
    x = x[sa]
    na = na[sa]
    dn = na[1:] - na[:-1]
    dQ = dHdnH2SO4(x[1:]) * dn
    Q1 = np.cumsum(dQ)
    n1 = nw_final + na[1:]

    # add water to acid
    xfinal = nw_final / (na_final + nw_final)
    x = np.linspace(.01, xfinal, 200)
    #nw = (1-x)/x * na_final
    nw = x/(1-x) * na_final
    sa = np.argsort(nw)
    x = x[sa]
    nw = nw[sa]
    dn = nw[1:] - nw[:-1]
    #dQ = dHdnH2O(x[1:]) * dn
    dQ = dHdnH2O(1 - x[1:]) * dn
    Q2 = np.cumsum(dQ)
    n2 = na_final + nw[1:]

    error = abs(2*(Q1[-1] - Q2[-1])/(Q1[-1] + Q2[-1]))
    plt.plot(n1, Q1 / n1, label='da->w')
    plt.plot(n2, Q2 / n2, label='dw->a')
    plt.legend()
    plt.xlabel('moles of solution')
    plt.ylabel('accumulated heat per mole of solution')
    plt.title(f'error in end heats for process = {error*100:.1f}%')

def plot_gibbsduhem_consistency():
    """
    Gibbs-Duhem test for thermodynamic consistency of homogeneous thermodynamic functions.
    """
    dx = .01
    x = np.arange(0, 1, dx)
    y1 = dHdnH2SO4(x) 
    dy1dx = (y1[1:] - y1[:-1]) / dx
    y2 = dHdnH2O(x)
    dy2dx = (y2[1:] - y2[:-1]) / dx
    plt.plot(x[1:], dy1dx * x[1:], label='xH2SO4*d(dHdnH2O)/dxH2SO4')
    plt.plot(x[1:], -1*dy2dx * (1 - x[1:]), label='-xH2O*d(dHdnH2O)/dxH2SO4')
    plt.xlabel('xH2SO4')
    plt.ylabel('term in Gibbs-Duhem equation')
    plt.legend()

def plots_tables():
    #
    plt.figure()
    plot_hs()
    #
    plt.figure()
    plot_hm()

def plots_examples():
    #
    plt.figure()
    plot_CHCl3_CH3OH_hm()
    #
    plt.figure()
    plot_CHCl3_CH3OH_hs()
    #
    plt.figure()
    plot_H2SO4_H2O_hpart()

comp_space = ((9, 1), (1, 1), (1, 9)) # (na, nw)

def plots_paths():
    for na, nw in comp_space:
        plt.figure()
        plot_td_path(na, nw)

def numeric_td_check():
    for na, nw in comp_space:
        try:
            check_tdpath_invar(na, nw)
        except Exception as e:
            print('failed assertion', e)

if __name__ == '__main__':
    numeric_td_check()
    plots_tables()
    plots_examples()
    plots_paths()
    plt.figure()
    plot_gibbsduhem_consistency()
    plt.show()
