import numpy as np
import matplotlib.pyplot as plt


def rho(T):
    """Gives the resistivity of tantalum in Ohm*nanometers."""
    return (-1.03e-8 + 5.1923e-10 * T - 6.3911e-14 *
            T**2 + 5.1236e-18 * T**3) * 1.e9


T = np.arange(300., 2300., 10.)
lb = 298.
ub = 305.
lin_approx = (rho(ub) - rho(lb)) / (ub - lb) * (T - lb) + rho(lb)

plt.figure()
plt.xlabel('$T$/K')
plt.ylabel(r'$\rho/(\Omega\cdot nm)$')
plt.plot(T, rho(T))
plt.plot(T, lin_approx)
plt.plot([300., 2300.], 2 * [300.],'k')
plt.plot([300., 2300.], 2 * [600.],'k')
plt.plot([1400. + 273.15] * 2, [min(rho(T)), max(rho(T))],'k')

plt.figure()
plt.xlabel('$T$/K')
plt.ylabel(r'% error lin approximation')
plt.plot(T, 100.*(rho(T) - lin_approx)/rho(T))

plt.show()
