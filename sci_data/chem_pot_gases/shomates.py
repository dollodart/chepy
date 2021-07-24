import os
import csv
import numpy as np
from scipy.special import erf
from chepy.sci_data.fundamental_constants import R

#energies in kJ/(mol*K), pressure in bar, temperature in K
R /= 1000. # J -> kJ
# standard conditions
P0 = 1.0  # bar
T0 = 298.15  # K

def read_in(datafile):
    """Reads in the data file with temperature ranges in the first row
    and columns of parameters corresponding to the Shomate equation."""
    with open(datafile, mode='r') as infile:
        f = csv.reader(infile, delimiter=',')
        names = []
        t = []
        tt = []
        for c, i in enumerate(f):
            if c == 0:
                tranges = [trange.split('-') for trange in i]
                tranges = [[float(trange[0]), float(trange[1])]
                           for trange in tranges]
            else:
                l = len(i)  # line length should be the same
                tt = []
                for c in range(len(i)):
                    if c == 0:
                        tt.append(i[0])
                    else:
                        tt.append(float(i[c]))
                t.append(tt)
    res = list(zip(*t))
    return [tranges, res[1:]]

data_dir = os.path.join(os.path.dirname(__file__), 'data')
def get_data(symbol):
    try:
        data_filename = os.path.join(data_dir, symbol + '-dat.csv')
        return read_in(data_filename)
    except FileNotFoundError:
        raise Exception('Data not available for ' + symbol)

class ShomatesGas:
    """
    Note the temperature look-up for different parameters in different
    temperature intervals can be vectorized, like done in the black-body
    radiation module, using a numpy ufunc.
    """
    def __init__(self, symbol):
        data = get_data(symbol)
        self.Tranges, self.parameters = data
        Tmin, Tmax = 1000000,-100000
        for Tlb, Tub in self.Tranges:
            if Tlb < Tmin:
                Tmin = Tlb
            if Tub > Tmax:
                Tmax = Tub
        self.Tmin = Tmin
        self.Tmax = Tmax

    def get_parameters(self, T):
        """
        Interval tree can be used if speed is a concern.
        """
        for c, (lb, ub) in enumerate(self.Tranges):
            if lb <= T <= ub:
                return self.parameters[c]

    def cp(self, T):
        p = self.get_parameters(T)
        T = T / 1000.
        A = p[0]
        B = p[1]
        C = p[2]
        D = p[3]
        E = p[4]
        return 1 / 1000. * (A + B * T + C * T**2 + D * T**3 + E * T**-2)


    def h0(self, T):
        p = self.get_parameters(T)
        T = T / 1000.
        A = p[0]
        B = p[1]
        C = p[2]
        D = p[3]
        E = p[4]
        F = p[5]
        G = p[6]
        H = p[7]
        enth = A * T + B / 2 * T**2 + C / 3 * T**3 + D / 4 * T**4 - E / T + F - H # divide by 1000?
        return enth # don't divide by 1000

    def h(self, T, P):
        """
        Ideal gas contribution is PV, which is just equal to NRT for an
        ideal gas by its mechanical equation of state.
        """
        return h0(T) + N*R*T 

    def s0(self, T):
        # T in K
        # returns in kJ/(mol*K)
        p = self.get_parameters(T)
        T = T / 1000.
        A = p[0]
        B = p[1]
        C = p[2]
        D = p[3]
        E = p[4]
        F = p[5]
        G = p[6]
        ent = A * np.log(T) + B * T + C / 2 * T**2 + \
            D / 3 * T**3 - E / 2 * T**-2 + G
        return ent / 1000.0

    def s(self, T, P):
        return s0(T) - R*np.log(P/P0)

    def g0(self, T):
        return self.h0(T) - T*self.s0(T)

    def g(self, T, P):
        return self.h(T, P) - T * self.s(T, P)

    def mu0(self, T):
        return self.g0(T)

    def mu(self, T, P):
        return self.g(T, P)

    def delmu0(self, T, P):
        """Pressure in bar, temperature in K.
        Defined for oxygen and other diatomic species."""
        return self.mu(T, P) / 2. - 1. / 2. * self.mu(T0, P0)


def erfc(x):
    return 1. - erf(x)

class SulfurUniversalChemPot:
    """
    Sulfur chemical potential.

    Due to the many allotropes of sulfur, a universal chemical potential
    is required which uses statistical mechanics to find the equilibrium
    distribution of all sulfur atoms between allotropes in an ideal gas
    phase. This requires the vibrational, rotational, and electronic
    modes for each species be calculated by simulation (the translational
    partition functions are ideal in the ideal gas region), so that the
    partition functions may be calculated. See Dill's text on statistical
    thermodynamics for a derivation of the principles of statistical
    mechanics applied to a gas phase.

    Reference:  Jackson, Adam J., Davide Tiana, and Aron Walsh. "A
    universal chemical potential for sulfur vapours." Chemical science 7.2
    (2016): 1082-1092.

    See also errata and supplementary information.
    """

    b = 10.  # K
    c = 80.  # sqrt(K)
    w = 100.  # K

    # polynomial coefficients
    xS8 = [7.352e4, -2.370e2, -3.871e-1, 1.744e-4, -3.676e-8]
    xS2 = [1.165e5, -1.783e2, -8.265e-2, 3.860e-5, -8.350e-9]
    xTtr = [5.077e2, 7.272e1, -8.295e0, 1.828e0]
    xa = [1.414e3, -2.042e2, 6.663e1]


    def Ttr(self, P):
        res = 0.
        for i, xTtri in enumerate(self.xTtr):
            res += xTtri * (np.log10(P) + 5)**i  # P in bar -> pascals 
        return res


    def a(self, P):
        res = 0.
        for i, xai in enumerate(self.xa):
            res += xai * (np.log10(P) + 5)**i  # P in bar -> pascals
        return res

    def mus8(self, T, P):
        res = R * T * np.log(P / P0)
        for i, xS8i in enumerate(self.xS8):
            res += xS8i * T**i
        return res


    def mus2(self, T, P):
        res = R * T * np.log(P / P0)
        for i, xS2i in enumerate(self.xS2):
            res += xS2i * T**i
        return res

    def mu(self, T, P):
        ttr = self.Ttr(P)
        Tnd = (T - ttr) / self.w
        s = .5*erfc(Tnd) * self.mus8(T,P) / 8.
        s += .5*(erf(Tnd) +1.) * self.mus2(T,P) / 2.
        s -= self.a(P) * np.exp(-(T - ttr + self.b)**2 / (2.*self.c**2))
        return s

if __name__ == '__main__':
    T = 500. # celsius
    T += 273.15 # K
    p = 5.e-6  # torr
    p /= 760.  # bar
    fracH2 = 1.e-4
    pO2 = (1 - fracH2) * p
    pH2 = fracH2 * p

    h2 = ShomatesGas('H2')
    o2 = ShomatesGas('O2')
    print(f'muH={h2.mu(T, p)/96.482/2.:.3f}eV')
    print(f'muO={o2.mu(T, p)/96.482/2.:.3f}eV')
