from scipy.misc import derivative
from scipy.stats import linregress
from scipy.optimize import fsolve
import numpy as np
import matplotlib.pyplot as plt

c0 = -1.7600413686e1
c1 = 3.8921204975e1
c2 = 1.8558770032e-2
c3 = -9.9457592874e-5
c4 = 3.1840945719e-7
c5 = -5.6072844889e-10
c6 = 5.6075059059e-13
c7 = -3.2020720003e-16
c8 = 9.7151147152e-20
c9 = -1.2104721275e-23
c = [c0, c1, c2, c3, c4, c5, c6, c7, c8, c9]
a0 = 1.185976e2
a1 = -1.183432e-4


def v(t):
    """Valid for 0 to 1372 deg C, temperature in deg C and thermovoltage in uV."""
    res = a0 * np.exp(a1 * (t - 127.9686)**2)
    for i in range(len(c)):
        res += c[i] * t**i
    return res


c0a = 0.000
c0b = 0.000
c0c = -1.318058e2
c1a = 2.5173462e-2
c1b = 2.508355e-2
c1c = 4.830222e-2
c2a = -1.1662878e-6
c2b = 7.860106e-8
c2c = -1.646031e-6
c3a = -1.0833638e-9
c3b = -2.503131e-10
c3c = 5.464731e-11
c4a = -8.9773540e-13
c4b = 8.315270e-14
c4c = -9.650715e-16
c5a = -3.7342377e-16
c5b = -1.228034e-17
c5c = 8.802193e-21
c6a = -8.6632643e-20
c6b = 9.804036e-22
c6c = -3.110810e-26
c7a = -1.0450598e-23
c7b = -4.413030e-26
c8a = -5.1920577e-28
c8b = 1.057734e-30
c9b = -1.052755e-35
cb = [c0b, c1b, c2b, c3b, c4b, c5b, c6b, c7b, c8b, c9b]
cc = [c0c, c1c, c2c, c3c, c4c, c5c, c6c]


def t_cjc(voltage, t_cj):
    def obj_func(t):
        return voltage - v(t) + v(t_cj)
    return fsolve(obj_func, t_cj)


def plot_cjt():
    """
    Thermovoltages only result from temperature differences, so does cold
    junction compensation only require you add the reference temperature?
    No, the Seebeck coefficient (the derivative of thermovoltage
    with respect to temperature) is not constant with temperature
    generally. For the k-type thermocouple it is very nearly constant.
    """
    plt.figure()
    cjc_temps = np.arange(0., 250., 10.)
    #t_vals=[t_cjc(10000.,cjc_temp) for cjc_temp in cjc_temps]
    # print(len(cjc_temps),len(t_vals))
    # print(cjc_temps,t_vals)
    t_vals = t_cjc(10000., cjc_temps)
    plt.xlabel('Cold Junction Temperature')
    plt.ylabel('Thermocouple temperature given thermovoltage 10 mV')
    s, i, r, p, sigma = linregress(cjc_temps, t_vals)
    print(f's={s:.2E},i={i:.2E},r={r:.2E},p={p:.2E},sigma={sigma:.2E}')
    plt.plot(cjc_temps, [s * cjc_temp + i for cjc_temp in cjc_temps], 'b-')
    plt.plot(cjc_temps, t_vals, 'bo')



def t(v):
    """Valid for 0 to 1372 deg C, Temperature in deg. C and thermovoltage in uV."""
    res = 0
    if 0. < v < 20644.:
        for i in range(len(cb)):
            res += cb[i] * v**i
    elif 20644. < v < 54886.:
        for i in range(len(cc)):
            res += cc[i] * v**i
    else:
        return None
    return res


def plot_tv_v_t():
    plt.figure()
    thermovoltages = np.arange(1., 54885., 1.)
    temps = [t(tv) for tv in thermovoltages]
    plt.plot(thermovoltages, temps)
    plt.xlabel('Thermovoltage in uV')
    plt.ylabel('Temperature in deg. C')

def plot_S_v_tv():
    plt.figure()
    temps = np.arange(0., 1372., 1.)
    seebeck = [derivative(v, temp, dx=0.1) for temp in temps]
    plt.plot(temps, seebeck, 'b-')
    plt.ylim(0, max(seebeck) + 5.)
    plt.plot([temps[0], temps[-1]], [sum(seebeck) / len(seebeck)] * 2, 'k-')
    plt.xlabel('Thermovoltage in uV')
    plt.ylabel('Seebeck Coefficient in uV/deg. C')

def plot_Svar_v_tv():
    plt.figure()
    temps = np.arange(0., 1372., 1.)
    seebeck = [derivative(v, temp, dx=0.1) for temp in temps]
    plt.plot(temps, 100. * (-sum(seebeck) / len(seebeck) + seebeck) / seebeck)
    plt.xlabel('Thermovoltage in uV')
    plt.ylabel(r'$\dfrac{(S(V)-\langle S\rangle)}{S(V)}$ in %')

if __name__ == '__main__':
    #plot_cjt()
    #plot_tv_v_t()
    #plot_S_v_tv()
    plot_Svar_v_tv()
    plt.show()
