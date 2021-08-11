import numpy as np
import pandas as pd
from scipy.stats import linregress
import matplotlib.pyplot as plt
from chepy.manufac_data.awg import dn

df = pd.read_csv('data.csv')
df = df[df['awg'] != 0]
x, y = df['diameter (in)'].values, df['awg'].values
x *= 1000  # to thou
m, b, *p = linregress(np.log10(x), y)
inv_found_fit = 10**((y - b)/m)

def plot_compare():
    plt.semilogx(x, y, 'o', label='data')
    plt.semilogx([x[0], x[-1]], [np.log10(x[0])*m + b, np.log10(x[-1])*m + b], '-', label='derived')
    plt.semilogx(dn(y), y, '--', label='provided')
    plt.title(f'$gauge=a\cdot log_{{10}}(l/x)$\na={-m:.0f},l={10**(-b/m):.0f}thou')
    plt.xlabel('Diameter in thou')
    plt.ylabel('Gauge')
    plt.legend()

def plot_residual_to_data():
    """
    Since dn defines gauge, this should be zero.
    """
    plt.plot(y, (x - dn(y))/x, label='definition')
    plt.plot(y, (x - inv_found_fit)/x, label='fit')
    plt.xlabel('Gauge')
    plt.ylabel('Residual (approximation - actual)')
    plt.title('residual to data')
    plt.legend()

def plot_residual_to_fit():
    plt.plot(y, (dn(y) - inv_found_fit)/dn(y))
    plt.xlabel('Gauge')
    plt.ylabel('Residual (approximation - actual)')
    plt.title('found fit residual to definition')

if __name__ == '__main__':
    plt.figure()
    plot_compare()
    plt.figure()
    plot_residual_to_data()
    plt.figure()
    plot_residual_to_fit()
    plt.show()
