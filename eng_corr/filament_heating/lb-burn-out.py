import matplotlib.pyplot as plt
import numpy as np
from chepy.sci_data.fundamental_constants import mp, kB

m = 32*mp
p = 10.**np.arange(-8., 0.)  # Pa
r = 10.**np.arange(-6., -1.)  # m
L = 1.  # basis, m
T = 300.  # K
rho = 19.3 * 1.e3  # kg/m^3
MW = 183.84 * 1.e3 / 6.022e23  # kg
t = []

for rr in r:
    A = 2 * np.pi * rr * L
    V = np.pi * rr**2 * L
    nW = V * rho / MW
    for pp in p:
        J = pp / np.sqrt(2 * np.pi * m * kB * T)
        ndotO2 = J * A
        t.append(nW / ndotO2)

t = np.array(t).reshape(len(r), len(p))
p, r = np.meshgrid(p, r)


fig, ax = plt.subplots()
ax.set_xlabel(r'$\log_{10} P$/torr')
ax.set_ylabel(r'$\log_{10} r$/cm')
ax.set_title('Min. Oxidation Time in Seconds')
CS = ax.contour(np.log10(p) - np.log10(760.), np.log10(r) +
                2, np.log10(t), levels=np.arange(-3, 5, 1))
ax.clabel(CS, inline=1, fontsize=10, fmt='%1.1f')
plt.show()
