import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

# data
df = pd.read_csv('grits.csv') # from Wikipedia, in um
df2 = pd.read_csv('surf-rough.csv') # from Hanningfield, in um

df['label'] = df['iso']
df['specification'] = 'iso'

bl = df['iso'].isna()
df['specification'].loc[bl] = 'cami'
df['label'].loc[bl] = df['cami'].loc[bl].astype(str)

df['numeric_grit'] = df['label'].str.lstrip('P').astype('float64')

dfm = df.merge(df2,how='inner',on='cami')

def plot_diam_grit():
    plt.ylabel('Average Diameter (micrometers)')
    plt.semilogy(df['label'], df['diam'])
    plt.xticks(rotation=90)

def plot_diam_numgrit():
    for n, gr in df.groupby('specification'):
        x = gr['numeric_grit']
        y = gr['diam']
        slope, inter, r2, sigma, pval = linregress(np.log(x), np.log(y))
        plot, = plt.loglog(x, y, 'o', label=n + f':n={slope:.2f},r2={r2:.3f},A={np.exp(inter):.3f}/um')
        plt.loglog(x, np.exp(inter)*x**slope, '-', color=plot.get_color())

    plt.xlabel('Numeric Grit')
    plt.ylabel('Diameter (um)')

    x = 10, 3000.
    y = tuple(2e4/x for x in x)
    plt.loglog(x, y, 'k-', label='$y=2\cdot 10^4/x$')
    plt.legend()


def plot_sr_cami():
    plt.xlabel('CAMI Grit')
    plt.ylabel('Surface Roughness in um')
    plt.semilogy(df2['cami'], df2['surface roughness'], 'ko-', label='data')
    xmax = df2['cami'].max()
    plt.plot([0, xmax], [0.40]*2, 'b-', label='Blue Light Limit')
    plt.plot([0, xmax], [0.75]*2, 'r-', label='Red Light Limit')
    plt.legend()

def plot_sr_diam():
    x = dfm['diam']
    y = dfm['surface roughness']
    plt.plot(x, y, 'o-')
    slope, inter, *_ = linregress(x, y)
    plt.plot(x, x*slope + inter)
    plt.xlabel('Diameter (um)')
    plt.ylabel('Surface Roughness (um)')
    plt.title(f'slope={slope:.4f}, inter={inter:.2f} um')

def loglog_sr_diam(): 
    x = dfm['diam']
    y = dfm['surface roughness']
    plt.loglog(x, y, 'o-')
    slope, inter, *_ = linregress(np.log(x), np.log(y))
    plt.loglog(x, np.exp(inter)*x**slope)
    plt.xlabel('Log Diameter (um)')
    plt.ylabel('Log Surface Roughness (um)')
    plt.title(f'exponent={slope:.2f}')

if __name__ == '__main__':
    plt.figure()
    plot_diam_grit()

    plt.figure()
    plot_diam_numgrit()

    plt.figure()
    plot_sr_cami()

    plt.figure()
    plot_sr_diam()

    plt.figure()
    loglog_sr_diam()

    plt.show()
