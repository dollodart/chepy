import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('tungsten-drawn-wire-mechanical-properties.csv')
df['mod e'] = df['modulus of elasticity (psi)'] / 1.e6
df['mod r'] = df['modulus of rigidity (psi)'] / 1.e6
df['ts'] = df['tensile strength (psi)'] / 1.e6
df['wd'] = df['wire diam (mm)'] * 1000.
df['ys'] = df['ts'] / df['mod e'] * 1.02 # this is yield stress

def log_fit(x, y):
    coeffs = np.polyfit(np.log(x), np.log(y), 1)
    xf = np.linspace(min(x), max(x), 100)
    yf = np.exp(coeffs[1])*xf**coeffs[0]
    return coeffs[0], coeffs[1], xf, yf

def _plot_logarithmic(x, y):
    n, A, xf, yf = log_fit(x, y)
    plt.loglog(x, y, 'bo')
    plt.loglog(xf, yf, 'b-', label=f'n={n:.2f}')
    plt.legend()
    #mn = min(min(xf), min(yf)) 
    #mx = max(max(xf), max(yf))
    #plt.xlim((mn, mx))
    #plt.ylim((mn, mx))

def parabola_fit(x, y):
    coeffs = np.polyfit(x, y, 2)
    xf = np.linspace(min(x), max(x), 100)
    yf = coeffs[0] * xf ** 2 + coeffs[1] * xf + coeffs[2]
    return coeffs[0], coeffs[1], coeffs[2], xf, yf

def _plot_parabola(x, y):
    *_ , xf, yf = parabola_fit(x, y)
    plt.plot(x, y, 'bo')
    plt.plot(xf, yf, 'b-')
    plt.ylim((0, None))
    plt.xlim((0, None))

def plot_ts_wd():
    bl = df['ts'].isna()
    x = df['wd'][~bl]
    y = df['ts'][~bl]
    _plot_logarithmic(x, y)
    plt.xlabel('Wire Diameter in um')
    plt.ylabel('Yield Stress in Million psi')

def plot_me_wd():
    bl = df['mod e'].isna()
    x = df['wd'][~bl]
    y = df['mod e'][~bl]
    _plot_parabola(x, y)
    plt.xlabel('Wire Diameter in um')
    plt.ylabel('Modulus of Elasticity in Million psi')

def plot_mr_wd():
    bl = df['mod r'].isna()
    x = df['wd'][~bl]
    y = df['mod r'][~bl]
    #_plot_parabola(x, y)
    _plot_logarithmic(x, y)
    plt.xlabel('Wire Diameter in um')
    plt.ylabel('Modulus of Rigidity in Million psi')

def plot_ys_wd():
    bl = df['ys'].isna()
    x = df['wd'][~bl]
    y = df['ys'][~bl]
    _plot_parabola(x, y)
    plt.xlabel('Wire Diameter in um')
    plt.ylabel('Yield Strain')

if __name__ == '__main__':
    #
    sdf = df[['wd', 'ts', 'mod e', 'ys', 'mod r']]
    mx = sdf.max(axis=0)
    mn = sdf.min(axis=0)
    print('max / min')
    print((mx / mn).round(2))
    plt.figure()
    plot_ts_wd()
    plt.figure()
    plot_me_wd()
    plt.figure()
    plot_mr_wd()
    plt.figure()
    plot_ys_wd()
    plt.show()
