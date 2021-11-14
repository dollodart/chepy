from read_data import read_isotherm_data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def fit_langmuir_explicit(p, Sigma):
    """
    Simply invert the analytical form to get an explicit equation for the
    parameter. Then take the mean value. Because it has to be in pairwise
    comparison form, it is pairwise done here.
    """

    Klst = []

    for i in range(len(p)):
        Sigma0 = Sigma[i]
        p0 = p[i]
    
        bl = p != p0

        pi = p[bl]
        Sigmai = Sigma[bl]

        g1 = Sigmai/Sigma0
        g2 = pi*p0

        K = (g1*p0 - pi)/(g2*(1. - g1))
        bl = (~np.isnan(K)) & (~np.isinf(K) & (K>0)) # this should prevent bad data points from being included
        m = K[bl].mean()
        if not np.isnan(m) and not np.isinf(m) and m > 0:
            Klst.append(m)

    # may want to impose some maximum residual on the data to only return results which have meaningful fits

    Kmean = np.array(Klst).mean() 

    return Kmean # K[~np.isnan(K)].mean()

def fit_freundlich(p, Sigma):
    bl = p > 0
    n, inter, r2, sigma, pval = linregress(np.log(p[bl]), np.log(Sigma[bl]))
    if pval < 0.02:
        return n
    return np.nan

def _fit(df, func, colname = 'K'):
    xy = []
    for n, gr in df.groupby(['doi', 'adsorbent', 'adsorbate', 'temperature']):
        try:
            K = fit_langmuir_explicit(gr['pressure'].values, gr['adsorption'].values)
            xy.append((n[0], n[1], n[2], n[3], K))
        except RunTimeWarning:
            pass
    return pd.DataFrame(xy, columns = ['doi', 'adsorbent', 'adsorbate', 'temperature', colname])

def fit_langmuirs(df):
    return _fit(df, fit_langmuir_explicit, 'K')

def fit_freundlichs(df):
    return _fit(df, fit_freundlich, 'n')
