import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

df = pd.read_csv('screws.csv', delimiter=',')

def plot_mdb_dist():
    sdf = df.drop_duplicates('Major Diameter Basic')
    for n, gr in sdf.groupby('Class Thread'):
        y = [0]*len(gr)
        #y = np.random.random(size=len(gr))
        plt.semilogx(gr['Major Diameter Basic'], y , 'o', label=n)

    plt.ylim(-10, 10)
    plt.legend()
    plt.xlabel('Log10 Major Diameter Basic in in.')
    plt.yticks([])
    plt.ylabel('Jittered Coordinate (arbitrary)')
    plt.title('Distribution Major Diameter Basic')

def plot_deltamdb_dist():
    sdf = df.drop_duplicates('Major Diameter Basic')
    for n, gr in sdf.groupby('Class Thread'):
        y = gr['Major Diameter Basic'].values
        y = np.sort(y)
        plt.plot(y[1:] - y[:-1], 'o-', label=n)

    plt.legend()
    plt.ylabel('Logarithmic Differences Major Diameter Basic, $y[i+1] - y[i]$')
    plt.xlabel('Sorted index $i$')

def plot_diameter_deltas():
    for n, gr in df.groupby('Class Thread'):
        mdx = gr['Major Diameter Max']
        mdb = gr['Major Diameter Basic']
        mdn = gr['Major Diameter Min']

        pdx = gr['Pitch Diameter Max']
        pdn = gr['Pitch Diameter Min']

        x = range(len(gr))

        plt.figure(f'Class {n}-normalized')
        plt.title(f'Class {n}')
        plt.xlabel('Increasing Size Index')
        plt.ylabel('Normalized Diameter Delta')
        plt.plot(x, (mdx - mdn)/mdb, label='(max - min)/basic')
        plt.plot(x, (mdx - mdb)/mdb, label='(max - basic)/basic')
        plt.plot(x, (mdb - mdn)/mdb, label='(basic - min)/basic')
        plt.plot(x, 2*(pdx - pdn)/(pdx + pdn), label='2(pmax - pmin)/(pmax + pmin)')
        plt.legend()

        plt.figure(f'Class {n}-nonnormalized')
        plt.title(f'Class {n}')
        plt.xlabel('Increasing Size Index')
        plt.ylabel('Diameter Delta')
        plt.plot(x, mdx - mdn, label='max - min')
        plt.plot(x, mdx - mdb, label='max - basic')
        plt.plot(x, mdb - mdn, label='basic - min')
        plt.plot(x, pdx - pdn, label='pmax - pmin')
        plt.legend()

        x = mdb
        y = mdx - mdn
        slope, inter, *_ = linregress(np.log(x), np.log(y))
        plt.figure(f'Class {n}-correlation')
        plt.loglog(x, y, 'o')
        plt.loglog(x, np.exp(inter)*x**slope)
        plt.xlabel('Logarithm Major Diameter Basic in in.')
        plt.ylabel('Logarithm Diameter Delta in in.')
        plt.title(f'exponent={slope:.2f}')

def corr_tables():
    ldf = df[df.columns[df.dtypes == 'float64']]
    d1 = ldf - ldf.mean()
    d1c = d1.corr()
    ldft = ldf.transpose()
    d2 = (ldft - ldft.mean()).transpose()
    d2c = d2.corr()
    return df.corr(), d1c, d2c

if __name__ == '__main__':
    print(
            df.groupby('Class Thread').agg(['mean', 'std']).transpose()
            )

    print(corr_tables())

    plt.figure()
    plot_mdb_dist()
    plt.figure()
    plot_deltamdb_dist()

    plot_diameter_deltas()

    plt.show()
