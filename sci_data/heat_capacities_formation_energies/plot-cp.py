import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from chepy.sci_data.fundamental_constants import R

df = pd.read_csv('heat-capacities.csv')
df['B'] = df['B'] / 1e3 # constant factors
df['C'] = df['C'] / 1e6
df['D'] = df['D'] / 1e-5
df['E'] = df['E'] / 1e9

def cp(T, A, B, C, D, E):
    return R * (A + B * T + C * T**2 + D * T**(-2) + E * T**3)

def cpl(T, A, B):
    return R * (A + B * T)

def plot_heat_capacity(formula):
    bl = df['formula'] == formula
    row = df[bl]
    trange = np.linspace(row['Tmin'],row['Tmax'],100)
    hc = cp(trange, row['A'].values[0], 
                row['B'].values[0], 
                row['C'].values[0], 
                row['D'].values[0], 
                row['E'].values[0])
    plt.figure()
    plt.xlabel('Temperature in K')
    plt.ylabel('Heat Capacity / R')
    plt.plot(trange, hc / R)
    plt.title(row['formula'].values[0] + '-' + row['phase'].values[0])

def test_kopps_rule():
    # this correlation to number of atoms is excllent, but can be corrected for by using kopp's rule module
    # that is limited, though, in the number of atoms it uses
    from chepy.utils.string2symbols import string2symbols

    sdf = df[df['formula'] != 'air']
    sdf['natoms'] = sdf['formula'].map(string2symbols).map(len)

    tot = []
    for n, gr in sdf[sdf['phase'] == 'g'].groupby('natoms'):
        if n == 0: # not a chemical formula
            continue
        count = cpstd = 0
        for ind, row in gr.iterrows():
            A,B,C,D,E,Tmin,Tmax = row[2:9]
            if Tmin <= 298 and Tmax >= 298:
                cpstd += cp(298, A,B,C,D,E)
                count += 1
        if count > 0:
            tot.append((n, cpstd/count))

    x,y = zip(*tot)
    plt.plot(x,y)
    plt.xlabel('N Atoms')
    plt.ylabel('$C_p(T=298K)/R$ averaged over compounds')
    plt.title('Pearson Correlation Coefficient={:.2f}'.format(pd.Series(y).corr(pd.Series(x))))

    return tot

if __name__ == '__main__':
    plot_heat_capacity('PH3')
    #test_kopps_rule()
    plt.show()
