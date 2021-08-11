import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

df = pd.read_csv('allen-keys.csv', delimiter=',')
df = df.iloc[:-1] # remove outlier
outlier = df.iloc[-1]['mm']

def plot_data():
    plt.plot(df['mm'], 'ko-', label='data')
    plt.plot([len(df)], [outlier], 'ko', label='data (outlier)')
    plt.xlabel('Ordered Numeric Label')
    plt.ylabel('Edge-to-Edge in mm')

def plot_data_loglog():
    plt.loglog(df['mm'], 'ko-', label='data')
    plt.loglog([len(df)], [outlier], 'ko', label='data (outlier)')
    plt.xlabel('Ordered Numeric Label')
    plt.ylabel('Edge-to-Edge in mm')

def plot_linfits():
    c = 8 
    n = len(df) - c
    s, i, r2, p, sigma = linregress(range(n), df['mm'].values[:n])
    plt.plot([0,n], [i, s*n + i], label='fit 1')
    str1 = f'$y/mm = {s:.3f} x + {i:.3f}$ with $R^2={r2:.2f}$'

    s, i, r2, p, sigma = linregress(range(n, n + c), df['mm'].values[n:])
    plt.plot([n,n+c], [i + s*n, s*(n+c) + i], label='fit 2')
    str2 = f'$y/mm = {s:.3f} x + {i:.3f}$ with $R^2={r2:.2f}$'

    plt.title(str1 + '\n' + str2)

    plt.legend()
    plt.show()

def plot_power_loglog():
    x = np.arange(1, len(df) + 1)
    xlog = np.log(x)
    ylog = np.log(df['mm'].values)
    s, i, r2, p, sigma = linregress(xlog, ylog)
    plt.loglog([x[0],x[-1]], [x[0]**s*np.exp(i), x[-1]**s*np.exp(i)], label='fit 1')
    plt.title(f'slope={s:.2f}, $R^2={r2:.2f}$')

if __name__ == '__main__':
    plt.figure()
    plot_data_loglog()
    plot_power_loglog()
    plt.figure()
    plot_data()
    plot_linfits()
    plt.show()
