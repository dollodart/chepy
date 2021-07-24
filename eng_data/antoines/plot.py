import numpy as np
import matplotlib.pyplot as plt
import csv

with open('antoines.csv', mode='r') as infile:
    names = []
    aparams = {}
    gparams = {}
    vrange = {}
    # formula, name, MW, Tc, Pc, omega, A, B, C, Tmin, Tmax
    lines = tuple(line for line in csv.reader(infile))
    for line in lines[1:]:
        formula = line[0]
        name = line[1]
        names.append(name)
        a = [float(line[6]), float(line[7]), float(line[8])]  
        g = [float(line[2]), float(line[3]), float(line[4])]
        v = [float(line[9]), float(line[10])]
        aparams.update(dict.fromkeys([formula, name], a))
        gparams.update(dict.fromkeys([formula, name], g))
        vrange.update(dict.fromkeys([formula, name], v))


def psat(T, params):
    return np.exp(params[0] - params[1] / (T + params[2]))


def single_plot(species):
    trange = np.linspace(vrange[species][0], vrange[species][1], 100)
    plt.xlabel('Temperature in K')
    plt.ylabel('Vapor pressure in bar')
    plt.plot(trange, psat(trange, aparams[species]))
    plt.title(f'{species}')

def corresponding_states():
    """
    Note that vapor pressure is a thermodynamic property of the liquid.  Hence
    generally one doesn't expect a law of corresponding states to apply.
    However, frequently the law of corresponding states does apply to liquid
    properties. See, e.g., doi:10.1002/aic.690010208, which states some
    corrections are needed for correlating critical properties to liquid
    surface tensions.
    """
    for n in names:
        mw, tc, pc = gparams[n]
        Tmin, Tmax = vrange[n]
        T = np.linspace(Tmin, Tmax, 100)
        pr = psat(T, aparams[n]) / pc
        Tr = T / tc
        plt.loglog(Tr, pr, label=n)
    plt.legend()
    plt.xlabel('$T/T_c$')
    plt.ylabel('$p/p_c$')

if __name__ == '__main__':
#    single_plot('m-Xylene')
    corresponding_states()
    plt.show()
