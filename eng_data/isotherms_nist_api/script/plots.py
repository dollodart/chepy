from chepy.eng_data.isotherms_nist_api import load_isotherm_data
from chepy.eng_data.isotherms_nist_api import (fit_langmuir_explicit,
        fit_langmuirs, fit_freundlichs)
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

def plot_a_p_shape(df):
    # scale all isotherms to vary in both x and y axes from 0 to 1
    # label by adsorbates, which are much less numerous than adsorbents
    plt.figure()
    plt.xlabel('$p / p_{max}$')
    plt.ylabel('$\Sigma / \Sigma_{max}$')
    #
    for n, gr in df.groupby(['doi', 'adsorbent', 'adsorbate']):
        plot = None
        for nn, ggr in gr.groupby('temperature'):
            ggr = ggr.sort_values(by='pressure')
            x = ggr['pressure'] / ggr['pressure'].max()
            y = ggr['adsorption'] / ggr['adsorption'].max()
            if plot is None:
                plot, = plt.loglog(x, y, 'o-', label=n[-1])
            else:
                plt.loglog(x, y, 'x-', color=plot.get_color())

    plt.legend()

def plot_a_T_shape(df):
    plt.figure()
    plt.xlabel('$ (T - \langle T \\rangle) / (T_{max} - T_{min})$')
    plt.ylabel('$\Sigma / \Sigma_{max}$, allowing $p/p_{max} \in [.45, .55]$')
    #
    for n, gr in df.groupby('adsorbate'):
        x = (gr['temperature'] - gr['temperature'].mean()) / (gr['temperature'].max() - gr['temperature'].min())
        y = gr['adsorption'] / gr['adsorption'].max()
        blx = gr['pressure'] / gr['pressure'].max()
        bl = (blx > .45) & (blx < .55)
        plt.plot(x[bl], y[bl], 'o', label=n)
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
        gr = gr.dropna()
        if len(gr) <= 3 or (gr['K'] < 0).any() or (gr['temperature'] < 0).any():
            continue
        x = 1/gr['temperature']
        y = np.log(gr['K'])
        slope, inter, *_ = linregress(x, y)
        print(x, y, slope, inter, sep='\n')
        plot, = plt.plot(x, y, 'o', label=f'$-\Delta H/kB$={slope:.3f}, $\Delta S/kB$={inter:.3f}')
        plt.plot((x.min(), x.max()),
                 (y.min(), y.max()),
                 '-', color = plot.get_color())
    plt.xlabel('$1/T$ in 1/K')
    plt.ylabel('Log Langmuir Constant in 1/bar')
    plt.legend()

def plot_n_T(df, ndf=None):
    if ndf is None:
        ndf = fit_freundlichs(df)
    for n, gr in ndf.groupby(['adsorbent', 'adsorbate']):
        if len(gr) <= 3:
            continue
        slope, inter, *_ = linregress(np.log(gr['temperature']), np.log(gr['n']))
        plt.loglog(gr['temperature'], gr['n'], 'o-', label=f'slope={slope:.3f}')
    plt.xlabel('Log Temperature in K')
    plt.ylabel('Log Freundlich Isotherm Exponent')
    plt.legend()

def plot_all_isotherms(df):
    # produced a figure for every isotherm
    for n, gr in df.groupby(['doi', 'adsorbent', 'temperature']):
        plt.figure()
        plt.plot(gr['pressure'], gr['adsorption'], label=n[1])
        plt.xlabel('pressure in ' + gr['pressUnit'].iloc[0])
        plt.ylabel('adsorption in ' + gr['adsUnit'].iloc[0])

if __name__ == '__main__':
    df = load_isotherm_data()
    bl = (df['adsorption'] > 1e-14) & (df['pressure'] > 1e-14)
    df = df[bl]

    plot_K_T(df)
    #plot_a_p(df)
    #plot_a_p_shape(df)
    #plot_a_T_shape(df)
    #plot_n_T(df)
    plt.show()
