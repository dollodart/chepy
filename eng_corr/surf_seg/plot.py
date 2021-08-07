import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('surface-segregation.csv', delimiter=',', encoding='utf-16')
df['delta'] = df['surface tension'] - df['energy of mixing']
# boolean values for solvent, solute, and no segregating component
bl1 = df['solvent'] == df['segregating component']
bl2 = df['solute'] == df['segregating component']
bl3 = ~ (bl1 | bl2)
df.loc[:, 'color'] = 'b'
df.loc[bl2, 'color'] = 'k'
df.loc[bl3, 'color'] = 'g'
color2val = dict(k="solute", b="solvent", g="none")

num = len(df)
# note: a parameter is here the ratio of the respective quantities in the pure components

def plot_ordered():
    for i in ['bond strength', 'size', 'surface tension', 'energy of mixing']:
        df = df.sort_values(by=i)
        plt.figure()
        plt.scatter(range(num), df[i], c=df['color'])
        plt.xticks(
            range(num),
            df['solvent'] + '(' + df['solute'] + ')',
            rotation=90)
        plt.xlabel('Solvent(Solute)')
        plt.ylabel(i)
        plt.savefig('plots/' + i)

def plot_(x, y):
    plt.scatter(df[x], df[y], c=df['color'])
    xmin = df[x].min()
    xmax = df[x].max()
    ymin = df[y].min()
    ymax = df[y].max()
    lower = .9*min(xmin, ymin)
    upper = 1.1*max(xmax, ymax)
    plt.plot([1,1], [.99, 1.01], 'k-')
    plt.plot([.99,1.01], [1,1], 'k-')
    plt.xlim(lower, upper)
    plt.ylim(lower, upper)
    plt.legend()

def plot_corr(x, y):
    """
    Plot correlation with least squares fit. There are several interpretations
    for least squares fit, including a projection interpretation which comes
    from direct minimization of the square error with linear algebra on the
    resulting derivative. There is also, however, the following statistical
    definition of the least square slope: the covariance of X and Y divided by
    the variance of X. This requires setting the coordinate system at the mean
    of the data set.
    """
    for n, gr in df.groupby('color'):
        r = gr[x].corr(gr[y], method='pearson')
        sx = gr[x].std()
        sy = gr[y].std()
        m = r*sy/sx
        # alternatively, since r = sxy/(sx*sy), m = sxy/sx^2
        print( abs(m - gr[x].cov(gr[y]) / gr[x].std()**2) )
        #assert 0.001 > abs(m - gr[x].cov(gr[y]) / gr[x].std()**2)
        #m = gr[x].cov(gr[y]) / gr[x].std()**2
        x0, x1 = gr[x].min(), gr[x].max()
        y0, y1  = gr[gr[x] == x0][y], gr[gr[x] == x1][y]
        xm = gr[x].mean()
        ym = gr[y].mean()
        plt.plot([x0, x1], [(x0 - xm)*m + ym, (x1 - xm)*m + ym], c=n, label=color2val[n] + f' {r:.2f}')
    plot_(x, y)


from scipy.spatial import ConvexHull
def plot_convex(x, y):
    # note that there exist particularly elegant and simple algorithms for convex hull in 2-D
    for n, gr in df.groupby('color'):
        points = gr[[x, y]].dropna().values
        ch = ConvexHull(points)
        plt.plot(points[ch.vertices,0],
                 points[ch.vertices,1],
                 c=n,
                 label=color2val[n] + f' {ch.area:.2f}-{ch.volume:.2f}')
        plt.plot([points[ch.vertices[0]][0], points[ch.vertices[-1]][0]], 
                 [points[ch.vertices[0]][1], points[ch.vertices[-1]][1]],
                 c=n, label=color2val[n] + f' {ch.area:.2f}-{ch.volume:.2f}')
    plot_(x, y)

def plot_sigma_epsilon():
    """Fig. 6 of the paper."""
    plt.figure()
#    plot_corr('size', 'bond strength')
    plot_convex('size', 'bond strength')
    plt.xlabel(r'$\sigma^*$')
    plt.ylabel(r'$\epsilon^*$')
    plt.savefig('plots/size-bond strength')

def plot_sigma_gamma():
    """Fig. 7 of the paper."""
    plt.figure()
#    plot_corr('size', 'surface tension')
    plot_convex('size', 'surface tension')
    plt.xlabel(r'$\sigma^*$')
    plt.ylabel(r'$\gamma^*$')
    plt.savefig('plots/size-surface tension')

def plot_sigma_gamma_minus_delta_gamma():
    """Fig. 8 of the paper."""
    plt.figure()
#    plot_corr('size', 'delta')
    plot_convex('size', 'delta')
    plt.xlabel(r'$\sigma^*$')
    plt.ylabel(r'$\gamma^*-\delta\gamma^*_m$')
    plt.savefig('plots/size-surface tension minus energy of mixing')

def plot_epsilon_gamma():
    """
    It is natural to complete all the correlations given the data the paper
    gives, here ratio of bond strengths (solute over solvent) and ratio of surface tensions (solute over solvent).
    """
    plt.figure()
#    plot_corr('bond strength', 'surface tension')
    plot_convex('bond strength', 'surface tension')
    plt.xlabel(r'$\epsilon^*$')
    plt.ylabel(r'$\gamma^*$')
    plt.savefig('plots/bond strength-surface tension')


if __name__ == '__main__':
#    plot_sigma_epsilon()
#    plot_sigma_gamma()
#    plot_epsilon_gamma()
    plot_sigma_gamma_minus_delta_gamma()
    plt.show()

    # segregating components
#    df['segregating'] = df['color'].rename('segregating')
#    df['segregating'] = df['segregating'].map(color2val)
#    stats = df.groupby('segregating').agg(['mean', 'std'])
#    print(df.groupby('segregating').agg('count')['solvent'].rename('sample sizes'))
#    print(stats.round(3))
