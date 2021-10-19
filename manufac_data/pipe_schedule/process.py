import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fractions import Fraction
from scipy.stats import linregress

df = pd.read_csv('ASME-pipe-schedules.csv', delimiter=',')
headers = df.columns
df['NPS'] = df['NPS'].map(lambda x:eval(x.replace(' ', '+')))
# (NPS is nominal pipe size in proper fraction form and not)
schedules = headers[2:] 
invu = 32
df_m = df * invu
umults = df_m.applymap(np.round)

def round2unit(x, invu):
    # floats are considered nan so a conditional on the element being a float
    # is not sufficient the Series method has a nan instance argument, but the
    # dataframe apply and applymap methods do not, requiring it to be defined
    # in the function

    if not math.isnan(x):
        f = Fraction(x)
        f = f.limit_denominator(invu)
        return f
    return float('nan')

fraction_approximations = (umults / invu).applymap(lambda x:round2unit(x, invu))
remainder = (df_m - umults) / invu
error = remainder * 1000.

df_fa = df.copy()
df_fa[schedules] = fraction_approximations[schedules]
df_e = df.copy()
df_e[schedules] = error[schedules]


def plot_checkgeo():

    deltas = np.log(df['NPS'].values[1:])- np.log(df['NPS'].values[0])
    deltas = deltas / deltas.max()

    x = np.linspace(0, 1, len(deltas))
    s, i, r2, sigma, p = linregress(x, deltas)
    plot, = plt.plot(x, deltas, 'o', label=f'NPS s={s:.2f} r2={r2:.2f}') # in sorted values
    plt.plot(x, tuple(s*x + i for x in x), color=plot.get_color())

    deltas = np.log(df['OD'].values[1:]) - np.log(df['OD'].values[0])
    deltas = deltas / deltas.max()

    s, i, r2, sigma, p = linregress(x, deltas)
    plot, = plt.plot(x, deltas, 'o', label=f'OD s={s:.2f} r2={r2:.2f}') # in sorted values
    plt.plot(x, tuple(s*x + i for x in x), color=plot.get_color())

    plt.plot((0, 1), (0,1), 'k-') # black line

    plt.xlabel('Sorted Index (normalized to 0--1)')
    plt.ylabel('Logarithmic Difference to Reference (normalized to 0--1)')

    plt.legend()

def plot_od_nps():
    plt.loglog(df['NPS'], df['OD'], 'o')
    plt.loglog((0,max(df['NPS'])), (0, max(df['OD'])))
    plt.xlabel('NPS in in.')
    plt.ylabel('OD in in.')
 
def plot_annularratio_nps():
    x = df['NPS']
    miny = 1.00
    maxy = 0.00
    for i in schedules:
        y = 2*df[i] / df['OD']
        plt.semilogx(x, y, 'o', label=i)
        miny = min(y.min(), miny)
        maxy = max(y.max(), maxy)

    print(f'maximum and minimum annular ratios = {maxy}, {miny}')
    plt.xlabel('NPS in in.')
    plt.ylabel('Annular Ratio')
    plt.title('Legend Schedule')
    plt.legend()

def plot_schedule_nps():
    xa = df['NPS']
    bl = xa < 28.
    x = xa[bl]
    subset = ['30', '40', '60', '80', '100', '120', '140', '160']
    for i in subset:
        y = df[i][bl]
        fitbl = (~x.isna()) & (~y.isna())
        n, c, r2, sigma, pval = linregress(np.log(x[fitbl]), np.log(y[fitbl]))
        plot, = plt.loglog(x, y, 'o', label=i + f' R^2={r2:.3f}')
        plt.loglog(x[fitbl], np.exp(c)*x[fitbl]**n, plot.get_color())

    plt.legend()
    plt.xlabel('NPS in in.')
    plt.ylabel('Thickness in in.')
    plt.title('Legend Schedule (some schedules omitted)')

def plot_error_nps():
    x = df['NPS']
    for i in schedules:
        plt.plot(x, df_e[i], 'o')
    plt.legend(schedules)
    plt.xlabel('NPS in in.')
    plt.ylabel(f'Error Using 1/{invu}" Approximation')
    plt.title('Legend Schedule')

def plot_avgerror_nps():
    y = df_e[schedules].abs().mean(axis=1)
    plt.plot(df_e['NPS'], y, 'o')
    plt.xlabel('NPS in in.')
    plt.ylabel(f'Average Absolute Error Using 1/{invu}" Approximation')

if __name__ == '__main__':


    plt.figure()
    plot_checkgeo()

    plt.figure()
    plot_od_nps()

    plt.figure()
    plot_annularratio_nps()

    plt.figure()
    plot_schedule_nps()

    plt.figure()
    plot_error_nps()
    plt.figure()
    plot_avgerror_nps()

    plt.show()

    # outputs
    #df_fa.to_latex(buf='fraction_approximations.latex', na_rep='', index=False)
    #df_e.to_latex(buf='error.latex', na_rep='', index=False)
