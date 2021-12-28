# volume mixing data taken from some problem set on google images for H2SO4/H2O
# it is only for purposes of estimating
import numpy as np
x = np.linspace(0.01, 0.99, 100)
dVmix = -13.1*x*(1-x) - 2.25*x**2*(1-x)
dVmix /= 1e6 # to m^3/mol
mx = np.argmin(dVmix)
mdVmix = dVmix[mx]

mwa = 98.079  # g/mol
rhoa = 1.8255 * 1e6 # g/m^3
mww = 18. # g/mol
rhow = 1. * 1e6 # g/m^3

nw = 1
na = x/(1-x)*nw

V = 1/mwa

va = mwa / rhoa # m^3/mol
vw = mww / rhow # m^3/mol

vi = va + vw
vf = vi + mdVmix
P = 101325. # Pa
W = P*(vf - vi)
print(f'x = {100*x[mx]:.1f}%',
      f'vol % change = {(vf/vi - 1)*100:.1f}',
      f'PV work = {W:.2f} J/mol',
      sep='|')
