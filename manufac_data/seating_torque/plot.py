import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

df = pd.read_csv('data.csv', index_col=0)
columns = df.columns

x, y = zip(*df.columns.str.split('.').to_list())
min_strength = [int(x)*100 for x in x]
yield_point = [int(y[i])/10*min_strength[i] for i in range(len(min_strength))]

df['diam'] = [float(v.replace('M', '')) / 25.4 for v in df.index]

def plot_st_od():
    for col in reversed(columns[1:]):
        x = df['diam']
        y = df[col] * 8.8
        bl = ~y.isna()
        slope, inter, *_ = linregress(np.log(x[bl]), np.log(y[bl]))
        plot, = plt.loglog(x, y, 'o', label=f'g={col},n={slope:.2f}')
        plt.loglog(x, np.exp(inter)*x**slope, color=plot.get_color())

    plt.xlabel('O.D. in in.')
    plt.ylabel('Seating Torque in lb*in.')
    plt.title('Legend is grade')
    plt.legend()

dft = df.transpose()

def plot_st_yp():
    for c, col in enumerate(dft.columns):
        if col == 'diam':
            continue
        plt.semilogy(yield_point, 1000.*dft.drop('diam')[col] / dft.loc['diam'][col]**3, label='M' + str(col))
    plt.legend()
    plt.xlabel('Yield Stress in N/mm^2') 
    plt.ylabel('Seating Torque / Diameter^3 in N/mm^2')
    plt.title('Legend is M$x$')

def plot_K():
    diam = df['diam']
    area = np.pi * diam**2
    for c, col in enumerate(df.drop('diam', axis=1).columns):
        torque = df[col]
        pre_load = yield_point[c] * area
        nut_factor = torque / (pre_load * diam)
        plt.plot(nut_factor, label=col)

    plt.xlabel('M$x$')
    plt.ylabel('Nut Factor')
    plt.title('Legend is grade')

    plt.legend()

if __name__ == '__main__':
    plt.figure()
    plot_st_od()
#    plot_st_yp() # made redundant by nut_factor

    plt.figure()
    plot_K()

    plt.show()
