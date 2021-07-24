import numpy as np
import matplotlib.pyplot as plt
from shomates import SulfurUniversalChemPot

sulf = SulfurUniversalChemPot()
Trange = np.arange(50., 1000., 10.)
# supports vectorized operations

plt.figure()
plt.xlabel('$T$/K')
plt.ylabel(r'$\mu_{\rm S}$/eV')
log10Prange = np.arange(-1., 2., .1)

for log10P in log10Prange:
    P = 10**log10P
    plt.plot(Trange, sulf.mu(Trange, P) / 96.485)
legend = [r'$\log_{10}P=$' + str(log10P) for log10P in log10Prange]
plt.legend(legend)
plt.show()

# TODO: sulfur chemical potential fails test
