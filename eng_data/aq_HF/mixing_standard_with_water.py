import numpy as np
import matplotlib.pyplot as plt

MW_HF = 20.01
MW_H2O = 18.01

V = 1.  # mL,basis
rho_1 = 1.17  # g/mL, data for 49 wt% HF
rho_2 = rho_H2O = 1.00
vfrac1 = np.arange(0, 1, 0.01)
vfrac2 = 1 - vfrac1
m1 = rho_1 * V * vfrac1
m2 = rho_H2O * V * vfrac2
mtot = m1 + m2
o1 = m1 / mtot
o2 = m2 / mtot
rho_final = (o1 / rho_1 + o2 / rho_2)**(-1)

o_HF_final = 0.49 * o1

plt.figure(1)
plt.xlabel('Volume Fraction 49 wt% HF in H2O')
plt.ylabel('Resulting wt% HF when mixed with pure H2O')
plt.grid(axis='both', which='both')
plt.plot(vfrac1, o_HF_final)
plt.plot(vfrac1, 0.49 * vfrac1)
plt.title('Standard Temperature and Pressure')
plt.legend(['Exact', 'Linear Interpolation'])
plt.show()
