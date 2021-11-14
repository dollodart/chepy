from fits import fit_langmuir_explicit, fit_langmuirs, fit_freundlichs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def hist_t(df):
    plt.hist(np.log10(df['temperature'].drop_duplicates()))
    plt.xlabel('log10 temperature in K')

def hist_p(df):
    bl = df['pressure'] > 0
    plt.hist(np.log10(df['pressure'][bl]))
    plt.xlabel('log10 pressure in bar')

def hist_a(df):
    for n, gr in df.groupby('adsUnit'):
        plt.hist(gr['adsorption'], label=n)

def hist_tp(df):
    l = df[['temperature', 'pressure']].drop_duplicates().dropna()
    x = l['temperature']
    y = l['pressure']
    bl = y > 0
    x = np.log10(x[bl])
    y = np.log10(y[bl])
    M, x, y = np.histogram2d(x, y)
    plt.matshow(M)

def plot_a_p(df):
    # plot isotherms (in comparable y-units), contrasting different
    for n, gr in df.groupby('adsUnit'):
        plt.figure()
        plt.xlabel('pressure in bar')
        plt.ylabel(f'adsorption in {n}')
        for nn, ggr in gr.groupby('adsorbent'):
            plot = None
            for nnn, gggr in ggr.groupby('temperature'):
                if plot is None:
                    plot, = plt.loglog(gggr['pressure'], gggr['adsorption'], 'o', label=nn)
                else:
                    plt.loglog(gggr['pressure'], gggr['adsorption'], 'x', color=plot.get_color())
        plt.legend()

def plot_K_bent(df, ndf = None):
    # langmuir constants split by adsorbent (not adsorbate/temperature). gives
    # you a noisy quantification of its 'bondability' (electronegativity) 
    if ndf is None:
        ndf = fit_langmuirs(df)
    plt.semilogy(ndf['adsorbent'], ndf['K'], 'x')
    plt.xticks(rotation=90)
    plt.ylabel('log K in bar$^{-1}$')

def plot_K_T(df, ndf = None):
    # temperature dependence of adsorption constant (from which fundamental
    # parameters may be derived, provided it is a fundamental and not empirical
    # constant).  enthalpy and entropy components of the free energy of
    # adsorption are available for those data having several isotherms assuming
    # constant enthalpy and entropy, by \Delta G = \Delta H - T \Delta S for K
    # = e^{-\Delta G/(kB T}.

    if ndf is None:
        ndf = fit_langmuirs(df)
    for n, gr in ndf.groupby(['adsorbent', 'adsorbate']):
        if len(gr) <= 3:
            continue
        slope, inter, *_ = linregress(np.log(gr['temperature']), np.log(gr['K']))
        plt.loglog(gr['temperature'], gr['K'], 'o-', label=f'delH/kB={inter:.3f}, delS/kB={-slope:.3f}')
    plt.legend()

def plot_all_isotherms(df):
    # produced a figure for every isotherm
    for n, gr in df.groupby(['doi', 'adsorbent', 'temperature']):
        plt.figure()
        plt.plot(gr['pressure'], gr['adsorption'], label=n[1])
        plt.xlabel('pressure in ' + gr['pressUnit'].iloc[0])
        plt.ylabel('adsorption in ' + gr['adsUnit'].iloc[0])

if __name__ == '__main__':
    from read_data import read_isotherm_data
    df = read_isotherm_data()

    #plot_K_T(df)
    #plot_a_p(df)
    #plt.show()
