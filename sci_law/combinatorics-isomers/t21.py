import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
n = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 40])
i = np.array([1, 1, 1, 2, 3, 5, 9, 18, 35, 75, 4347, 366319, 62491178805831])

plt.figure()
plt.xlabel('number of atoms')
plt.ylabel('log number of isomers')
plt.semilogy(n, i, 'o', label='data')
s, intcpt, r2, sigma, pval = linregress(n, np.log(i))
label = f'{np.exp(intcpt):.2E}*{np.exp(s):.2E}^n'
plt.semilogy(n, np.exp(s)**n * np.exp(intcpt), '-', label=label)
plt.title(f'$R^2$ = {r2:.2f}')
plt.legend()

plt.figure()
plt.xlabel('log number of atoms')
plt.ylabel('log number of isomers')
plt.loglog(n, i, 'o', label='data')
s, intcpt, r2, sigma, pval = linregress(np.log(n), np.log(i))
label = f'{np.exp(intcpt):.2E}*n^{s:.2f}'
plt.loglog(n, np.exp(intcpt)*n**s, '-', label=label)
plt.title(f'$R^2$ = {r2:.2f}')
plt.legend()

plt.show()
