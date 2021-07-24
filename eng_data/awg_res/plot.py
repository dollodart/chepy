import numpy as np
import matplotlib.pyplot as plt

def dn(n):
    """
    The algebraic form for the geometric sequence was provided by Wikipedia.
    """
    return .127 * 92 ** ((36 - n) / 39)

rho = dict()
with open('resistivities.csv', 'r') as _:
    lines = _.readlines()
    for line in lines[1:]:
        a, b = line.rstrip('\n').split(',')
        rho[a] = float(b)

# since the gauge and R/L are linear in log coordinates
# only two points are needed to calculate and plot them
nmin = 0
nmax = 30
dmin = dn(nmin)
dmax = dn(nmax)
pi = 3.14159
amin = pi * dmin**2 / 4
amax = pi * dmax**2 / 4

for key in rho:
    RoLmin =  rho[key] / amin
    RoLmax = rho[key] / amax
    plt.loglog([dmin, dmax], [RoLmin / 100, RoLmax / 100], label=key)

plt.xlabel('diameter in mm')
plt.ylabel('R/L in Ohm/cm')
plt.title('At 20 deg. C')
plt.legend()
plt.show()
