import numpy as np
import pandas as pd
from scipy.stats import linregress
from scipy.optimize import minimize

def fit_langmuir_explicit(p, Sigma):
    bl = p > 0
    Sigma = Sigma[bl]
    p = p[bl]

    def residual(Ka, p, Sigma):
        K, a = Ka
        Kp = K*p
        r = (np.log(Sigma) + np.log(a) - np.log(Kp) + np.log(1 + Kp))**2
        r = sum(r)
        return r

    K0 = 1
    a0 = 1
    x0 = np.array([K0, a0])

    res = minimize(residual, x0, args=(p, Sigma), bounds=((1e-6, None), (1e-6, None)))
    # parameters must be positive
    if res.success:
        return res.x[0]


def fit_langmuir_explicit_pairwise(p, Sigma):
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
        if not np.isnan(m) and not np.isinf(m) and m > 0 and len(bl) - bl.sum() > 5: # minimum 5 data points
            Klst.append(m)

    # may want to impose some maximum residual on the data to only return results which have meaningful fits

    Kmean = np.array(Klst)
    Kmean = Kmean[Kmean < np.inf] # equivalent to isna
    Kmean = Kmean.mean()

    return Kmean # K[~np.isnan(K)].mean()

def fit_freundlich(p, Sigma):
    bl = p > 1e-6 # microbar
    n, A, r2, sigma, pval = linregress(np.log(p[bl]), np.log(Sigma[bl]))
    if pval < 0.02 and abs(r2) > .5:
        return n
    return np.nan

def _fit(df, func, colname = 'K'):
    xy = []
    for n, gr in df.groupby(['doi', 'adsorbent', 'adsorbate', 'temperature']):
        try:
            K = func(gr['pressure'].values, gr['adsorption'].values)
            xy.append((n[0], n[1], n[2], n[3], K))
        except Exception as e:#RunTimeWarning:
            print(e, type(e))
            import sys; sys.exit()
            pass
    return pd.DataFrame(xy, columns = ['doi', 'adsorbent', 'adsorbate', 'temperature', colname])

def fit_langmuirs(df):
    return _fit(df, fit_langmuir_explicit, 'K')

def fit_freundlichs(df):
    return _fit(df, fit_freundlich, 'n')

def scipy_form_arrhenius_ssr(x, K, T):
    return arrhenius_sum_square_residual(x[0], x[1], K, T)

def arrhenius_sum_square_residual(delH_kB, delS_kB, K, T):
    # uses ratio form

    K = K.sort_values()
    T = T.sort_values()
    med = len(T) // 2
    K0 = K.iloc[med]
    T0 = T.iloc[med]

    y = np.log(K / K0)
    yapprox = -delH_kB*(1/T-1/T0) + delS_kB*(1+T/T0)

    r = y - yapprox
    sr = r**2
    ssr = sum(sr)
    return ssr

def fit_vanthoft(T, K, delH_kB0 = -1000, delS_kB0 = -25):
    res = minimize(scipy_form_arrhenius_ssr,
            x0=[delH_kB0, delS_kB0],
            args=(K, T),
            method='Powell',
            bounds=[(None, 0), (None, 0)])
    if res.success:
        return res.x

if __name__ == '__main__':
    T = np.linspace(250, 350, 100)
    delH_kB = -1100
    delS_kB = -25
    K = np.exp(-delH_kB*1/T + delS_kB)

    T = pd.Series(T)
    K = pd.Series(K)

    params = fit_vanthoft(T, K)
    print(params)
