import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

# nCnHn+2 + (2n+1)O2 -> nCO2 + (n+1)H2O
delHfH2O = -68.31 # kcal/mol
delHfCO2 = -94.24 # kcal/mol

df1 = pd.read_csv('straight-aliphatic.csv')
df2 = pd.read_csv('paper-data.csv')
dsources = {0:'libretext', 1:'paper'}

def test_agreement():
    df = df1.merge(df2, how='inner', on='n')
    y1f = -1*df['delHf(kcal/mol)']
    y2f = df['delHc(kcal/mol)'] - df['n']*delHfCO2 - (df['n']+1)*delHfH2O
    print(y1f, y2f)
    df['disagreement'] = 2*(y1f - y2f)/(y1f + y2f)
    print(f'mean disagreement between data sets = {df["disagreement"].abs().mean()*100:.2f} %')

x1 = df1['n']
y1 = df1['delHf(kcal/mol)']
x2 = df2['n']
y2 = df2['delHc(kcal/mol)']
y2 = y2 - df2['n']*delHfCO2 - (df2['n'] + 1)*delHfH2O
y2 = -1*y2

def plot_H_n():
    fig, ax = plt.subplots(nrows=1)

    st = ''
    for c, (x, y) in enumerate(((x1, y1), (x2, y2))):
        plot, = ax.plot(x, -1 * y, 'o-', label=f'{dsources[c]} mol spec.')
        ax.plot(x, -1 * y / x, 'o-', color=plot.get_color(), label=f'{dsources[c]} c-unit spec.')
        bl = x > 5
        s, i = alt_fit(x[bl], -y[bl])
        st += f'data source {dsources[c]}; slope, inter $-\Delta H_{{f}}(n>5)$ = {s:.2f}, {i:.2f} kcal/mol\n'

    ax.set_xlabel('$n$-ane')
    ax.set_ylabel('$-\Delta_f H^\ominus$/(kcal/mol)')
    ax.set_ylim((0, None))
    ax.set_xlim((0, 15))
    ax.set_title(st)
    ax.legend()

def plot_H_invn():
    fig, ax = plt.subplots(nrows = 1)

    st = ''
    for c, (x, y) in enumerate(((x1, y1), (x2, y2))):
        plot, = ax.plot(1/x, -1. * y/x, 'o', label=f'{dsources[c]}')
        bl = x > 5
        s, i = alt_fit(1/x[bl], -1*y[bl]/x[bl])
        ax.plot(1/x, s/x + i, color=plot.get_color())
        st += f'data source {dsources[c]}; lim $N\\to\infty,\Delta H_{{f}}/N$ = -{i:.2f}kcal/mol\n'

    ax.set_xlabel('$1/n$')
    ax.set_ylabel(f'$-\Delta_f H^\ominus/n$/(kcal/mol)')
    ax.set_ylim((0, None))
    ax.set_title(st)
    ax.legend()

def alt_fit(x, y):
    """
    Don't overweight points by the magnitude, convert to a logarithmic scale.
    """
    slope0, *_ = linregress(x, y)
    while True:
        # find the best fit intercept, provided a slope
        inter = (y - slope0 * x).mean() # vector of b values
        # find the best fit slope, subtracting off the intercept
        _, loginter, *_ = linregress(np.log(x), np.log(y - inter))
        slope = np.exp(loginter)
        if (slope - slope0) / slope < .05:
            break

    return slope, inter

def test_alt_fit():
    for x, y in ((x1, y1), (x2, y2)):
        s1, i1, *_ = linregress(1/x, -1*y/x)
        s2, i2 = alt_fit(1/x, -1*y/x)
        print('param, linregress, alt_fit, diff/%')
        print(f'slope, {s1:.3f}, {s2:.3f}, {100*(s1 - s2)/s1:.1f}')
        print(f'inter, {i1:.3f}, {i2:.3f}, {100*(i1 - i2)/i1:.1f}')

def fit_bond_energies():
    # a0 = C-H in CH4
    # a1 = C-H in CH3R
    # a2 = C-H in CH2RR'
    # b0 = C-C in CH3CH3
    # b1 = C-C in RCH2CH3
    # b2 = C-C in RCH2CH2R'

    coeffs = np.array([
            #a0,a1,a2,b0,b1,b2
            [4,0,0,0,0,0], #methane
            [0,6,0,1,0,0], #ethane
            [0,6,2,0,2,0], #propane
            [0,6,4,0,2,1], #butane
            [0,6,6,0,2,2], #pentane
            [0,6,8,0,2,3], #hexane
            [0,6,10,0,2,4], #heptane
            [0,6,12,0,2,5], #octane
            [0,6,14,0,2,6], #nonane
            [0,6,16,0,2,7], #decane
            ])

    arr1 = df1['delHf(kcal/mol)'].values[:10]
    arr2 = df2['delHc(kcal/mol)'].values[:10]
    x1, residuals, rank, s = np.linalg.lstsq(coeffs, arr1)
    x2, residuals, rank, s = np.linalg.lstsq(coeffs, arr2)
    return x1, x2

def tests():
    test_alt_fit()
    test_agreement()
        
def plots():
    plot_H_n()
    plot_H_invn()

if __name__ == '__main__':
    tests()

    be1, be2 = fit_bond_energies()
    for c, label in enumerate((
        'a0 = C-H in CH4',
        'a1 = C-H in CH3R',
        'a2 = C-H in CH2RR',
        'b0 = C-C in CH3CH3',
        'b1 = C-C in RCH2CH3',
        'b2 = C-C in RCH2CH2R')):
        print(f'{label} {be1[c]:.2f} {be2[c]:.2f}')

    plots()
    plt.show()
