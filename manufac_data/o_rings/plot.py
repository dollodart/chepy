import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

df = pd.read_csv('o-rings.csv')

def sig_fig_round(x, n):
    l10 = np.log10(x)
    m, c = l10 // 1, l10 % 1
    return round(10**c, n) * 10 ** m

from math import floor

def sig_fig_floor(x, n):
    l10 = np.log10(x)
    m, c = l10 // 1, l10 % 1
    assert n <= m
    return floor(10**(c+n)) * 10 **(m-n)

df['series'] = df['size'].apply(lambda x:sig_fig_floor(x, 0))
df['geometric invariant'] = df['O.D. (in.)'] - df['I.D. (in.)']-2*df['thickness (in.)']

def plot_thickness_size():
    # this shows the O.D. is grouped into 5 series, 100, 200, 300, 400, and 900
    # these series
    plt.plot(df['size'], df['thickness (in.)'])
    plt.xlabel('size')
    plt.ylabel('thickness in inches')
    plt.xticks([10,20,30,40,100,200,300,400,500,900])


def _plot_dist(col):
    sdf = df.drop_duplicates(col)
    sdf = sdf.sort_values(by=col)
    plt.semilogy(range(len(sdf)), sdf[col])

def plot_geometric_invariant():
    _plot_dist('geometric invariant')
    plt.xlabel('ascending index')
    plt.ylabel('$O.D. - I.D. - 2t$ in inches')

def plot_thickness():
    _plot_dist('thickness (in.)')
    plt.xlabel('ascending index')
    plt.ylabel('thickness in inches')

def plot_ID():
    _plot_dist('I.D. (in.)')
    plt.xlabel('ascending index')
    plt.ylabel('I.D. in inches')

def _plot_fractional_steps(col):
    sdf = df.drop_duplicates(col)
    sdf = sdf.sort_values(by=col)
    y = sdf.iloc[1:][col].values / sdf.iloc[:-1][col].values
    plt.plot(y - 1)
    plt.xlabel(f'ascending index (of {col})')
    plt.ylabel('fractional change ($s[i+1]/s[i] - 1$)')

def plot_fractional_steps_ID():
    _plot_fractional_steps('I.D. (in.)')

def plot_fractional_steps_thickness():
    _plot_fractional_steps('thickness (in.)')

# bivariate plots
def plot_thickness_ID():
    plt.loglog(df['I.D. (in.)'], df['thickness (in.)'], 'o')
    plt.xlabel('I.D. in inches (= $O.D. - 2t$)')
    plt.ylabel('Thickness in inches')

# bivariate groupby 
def plot_OD_size_by_series():
    for n, gr in df.groupby('thickness (in.)'):
        # group by thickness to ignore series which don't have uniform thickness (< 100 series)
        if len(gr) < 3 or gr['series'].nunique() > 1:
            continue
        x = (gr['size'] - gr['size'].min()).values
        y = gr['O.D. (in.)'].values
        plot, = plt.semilogy(x, y, 'o', label=gr['series'].unique()[0])
        s, i, *params = linregress(x, np.log(y))
        abs_frac_err = abs((np.exp(i + x*s) - y)/y)
        label = f'abs_frac_err(mean,max)={abs_frac_err.mean():.2f},{abs_frac_err.max():.2f} frac_incr={100*(np.exp(s) - 1):.1f}%'
        plt.semilogy(x, np.exp(i + x*s), color=plot.get_color(), label=label)

    plt.legend()

def print_series_const_thickness():
    for n, gr in df.groupby('series'):
        if gr['thickness (in.)'].nunique() == 1 and len(gr) > 1:
            print('series', n, 'has thickness', gr['thickness (in.)'].drop_duplicates())

def print_duplicates():
    print()
    print('sizes with duplicate I.D.') 
    for n, gr in df.groupby('I.D. (in.)'):
        if len(gr) > 1:
            print(n, tuple(gr['size']))
    print()
    print('sizes with duplicate O.D.') 
    for n, gr in df.groupby('O.D. (in.)'):
        if len(gr) > 1:
            print(n, tuple(gr['size']))


def print_nuniques():
    print('column nunique')
    for col in df.columns:
        print(col, df[col].apply(lambda x: sig_fig_round(x, 3)).nunique()) 

if __name__ == '__main__':

    assert (df['O.D. (in.)'] > 2*df['thickness (in.)']).all()

    for n, gr in df.groupby('thickness (in.)'):
        assert gr['O.D. (in.)'].nunique() == len(gr)
        assert gr['I.D. (in.)'].nunique() == len(gr)

    print_nuniques()
    print_duplicates()
    print_series_const_thickness()

    plt.figure()
    plot_geometric_invariant()
    plt.figure()
    plot_thickness_ID()
    plt.figure()
    plot_ID()
    plt.figure()
    plot_thickness()
    plt.figure()
    plot_fractional_steps_ID()
    plt.figure()
    plot_fractional_steps_thickness()
    plt.show()
    plt.figure()
    plot_thickness_size()
    plt.show()
    plt.figure()
    plot_OD_size_by_series()
    plt.show()
