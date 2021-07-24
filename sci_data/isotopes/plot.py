import pandas as pd
import matplotlib.pyplot as plt
from numpy import log

df = pd.read_csv('cleaned-isotope-data.csv')
mhaves = ['atomic number', 'symbol', 'isotope number']
df[mhaves] = df[mhaves].fillna(method='ffill')
df['diff'] = df['ramu'] - df['isotope number']
index = df['diff'].idxmin()
x = df['isotope number'].iloc[index]
y = df['diff'].iloc[index]

def proton_number_approximation():
    plt.figure()
    plt.plot(df['isotope number'], df['diff'])
    plt.xlabel('$Q$')
    plt.ylabel('$m-Qm_p$ in amu')
    plt.plot(x, y, 'o')
    plt.text(x, y, df['symbol'].iloc[index])
    plt.show()

def scatter_plot_composition():
    plt.figure()
    plt.xlabel('Chemical')
    plt.xticks(rotation=90)
    plt.ylabel('Isotope Compositions')
    plt.ylim(0, 100)
    #
    plt.plot(df['symbol'].iloc[:100], df['comp'].iloc[:100], 'o')
    for i, txt in enumerate(df['isotope number']):
        plt.annotate(txt, (df['symbol'].iloc[i], df['comp'].iloc[i]))
    plt.show()

def stacked_bar_plot_composition():
    # specify subset to avoid crowding
    plt.figure()
    plt.xlabel('Chemical')
    plt.xticks(rotation=90)
    plt.ylabel('Isotope Compositions')
    plt.ylim(0, 100)
    #
    subset = ['Ac', 'Zn', 'Br', 'Kr']
    for el, gr in df[df['symbol'].isin(subset)].groupby('symbol'):
        gr = gr.sort_values(by='comp', ascending=False)
        val = 0
        for d in range(len(gr)):
            per = 100 * gr['comp'].iloc[d]
            plt.plot([el] * 2, [val, val + per], linestyle='-',
                     linewidth=4, c=str( d/len(gr) + 0.1 ) )
            plt.annotate(gr['isotope number'].iloc[d], (el, val + per/2 ) )
            val += per
    plt.show()


def entropy_measure(x):
    return -(x*log(x)).sum()
res = df.groupby('symbol')['comp'].agg(entropy_measure).sort_values(ascending=False) 
# series retains column name on aggregate transform
# from here on comp means entropy, not composition
sdf = df[['symbol','atomic number']].drop_duplicates().merge(res.reset_index(),how='inner',on='symbol')

def isotope_entropy():
    """A measure of how spread out or varied the isotopes for an element are in natural abundance."""
    plt.figure()
    plt.plot(sdf['atomic number'],sdf['comp']) 
    plt.xlabel('Atomic Number')
    plt.ylabel('Isotope Entropy = $-\sum_i x_i \ln x_i$')
    plt.show()

def isotope_entropy_by_period_group():
    """A measure of how spread out or varied the isotopes for an element are in
    natural abundance, correlated to the period or group of the element."""
    from orbit import dct
    plt.figure()
    for i in 's','p','d','f','period','group':
        sdf[i] = sdf['atomic number'].map(dct).map(lambda x:x[i])
        r = sdf.groupby(i)['comp'].agg('mean')
        plt.plot(r.index, r.values,label=i)

    plt.xlabel('Number')
    plt.ylabel('Mean Isotope Entropy = $-\sum_i x_i \ln x_i$ over Elements')
    plt.xticks(range(19))
    plt.legend()
    sdf['odd_group'] = sdf['group'].map(lambda x: x % 2) 
    r = sdf.groupby('odd_group')['comp'].agg(['mean','std']).round(2)
    print(r)
    plt.show()

if __name__ == '__main__':
    #proton_number_approximation()
    stacked_bar_plot_composition()
