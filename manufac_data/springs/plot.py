'''
Dt=wire diameter
Dm=mean diameter (coil)
Lo=unloaded length
nv=number of active coils
Ln=loaded length
Fn=spring force
sn=deflection=Lo-Ln
c=rate
Lst=solid length
Nc=number of load oscillations
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

frames = []
for i in range(1, 9):
    dfi = pd.read_csv(f'data/t{i}.tsv', delimiter='\t')
    dfi['page'] = i
    if 'Fn.1' in dfi.columns:
        dfc = dfi.drop(['Fn', 'c', 'Cat.no'], axis=1)
        dfd = dfi.drop(['Fn.1', 'c.1', 'Cat.no.1'],axis=1)
        dfc.columns = dfd.columns # rename columns, not assignment of values
        dfi = pd.concat((dfc, dfd),ignore_index=True)
    frames.append(dfi)

df = pd.concat(frames, ignore_index=True)
df = df.set_index('Cat.no')
df['k'] = df['Fn'] / df['sn']
n = len(df)

df['Di'] = df['Dm'] - df['Dt'] / 2. # Di=inner diameter (coil)
df['Do'] = df['Dm'] + df['Dt'] / 2. # Do=outer diameter (coil)

df['nt'] = df['nv'] + 2

df['cd'] = df['nt'] / df['Lo'] # may want to use nv for active coils if cd is used in force equations

df['dg'] = df['Dm']*df['cd'] # dimensionless group: diameter times coil density

# arc length of a helix
df['al'] = df['Lo']*np.pi*np.sqrt( df['dg']**2 + 1)

# solid length
df['Lst'] = df['Dt'] * df['nt']

# aspect ratio
df['ar'] = df['Lo'] / df['Dm']

# this equation is only valid under certain limiting conditions of the geometry
# k = G.d^4/(8D^3.Na)
# G = shear modulus 
df['g'] = 8*df['nv'] * df['k'] * df['Dm']**3 / df['Dt']**4

#
df['Fn_calc'] = df['Dt']**4*(df['Lo'] - df['nv']*df['Dt'])/(df['nv']*(df['Dm'] - df['Dt'])**3) # equation from Wikipedia
# coefficient undetermined is E/(16*(1+\nu)), units of 1/mm^2

# inclination of the coil
df['alpha'] = 2 * np.arctan(1/(2*df['dg'])) * 180 / np.pi # angle in deg. of 

## definition checks on data
def plot_LolessLn_sn():
    plt.xlabel('Cat. no.')
    plt.ylabel('Absolute Fractional Difference in Given and Calculated Displacement')
    y = df['Lo'] - df['Ln']
    y = (y - df['sn'] ) / df['sn']
    plt.semilogy(y.abs())

def plot_c_k():
    plt.xlabel('Maximum Force / Deflection in N/mm (calculated rate/spring constant)')
    plt.ylabel('Given Rate in N/mm')
    plt.loglog(df['k'], df['c'], 'o')

## other checks on data
def plot_Fn_Fncalc():
    plt.xlabel('Maximum Force / $(E/(16(1+\\nu)))$ as calculated, in mm^2')
    plt.ylabel('Maximum Force Provided in N')
    plt.loglog(df['Fn_calc'], df['Fn'], 'o')
    x, y = np.log(df['Fn_calc'].values), np.log(df['Fn'].values)
    slope, inter, *_ = linregress(x, y)
    ycalc = x**round(slope)*np.exp(inter)
    plt.loglog(x, ycalc, label='best fit')
    E = 16*(1+3/2)*np.exp(inter) # N/mm^2, assuming 3/2 Poisson ratio
    plt.title('$E_{calc}=$' + f'{E/1e3:.0f} GPa ' +
            'c.f. 185 GPa (EN 10270-3) and 206 GPa (EN 10270-1-SH)') # Mollifoco Modenese

def plot_g():
    plt.xlabel('Category Number')
    plt.ylabel('Calculated Shear Modulus in MPa') # 1 MPa = 1 N/mm^2
    for n, gr in df.groupby('page'):
        plt.plot(gr['g'], 'o', label=n)

    plt.plot([df.index.min(),df.index.max()], [73_000]*2, 'k-', label='G(EN 10270-3)') # Mollifico Modenese
    plt.plot([df.index.min(),df.index.max()], [81_500]*2, 'k--', label='G(EN 10270-1-SH)') # Mollifico Modenese
    plt.legend()
    plt.title('Legend is page from source or reference material')

# distributions
def _plot_dist(col):
    plt.xlabel('Sorting Index')
    plt.semilogy(range(n), sorted(df[col]))
    plt.title(f"$\mu$ = {df[col].mean():.2E}N/mm, $\sigma$ = {df[col].std():.2E}N/mm")

def plot_alpha():
    _plot_dist('alpha')
    plt.ylabel('Coil Angle to Axis in deg.')

def plot_k():
    _plot_dist('k')
    plt.ylabel('Spring Constant in N/mm')

def plot_cd():
    _plot_dist('cd')
    plt.ylabel('Coil Density (1/mm)')

def plot_Fn():
    plt.xlabel('Index (arbitrary)')
    plt.ylabel('Maximum Force in N')
    sdf = df.sort_values(by='Fn')
    sdf['sorted_index'] = range(n)
    for nn, gr in sdf.groupby('page'):
        plt.semilogy(gr['sorted_index'],gr['Fn'],'o-',label=nn)
    plt.title(f"$\mu$ = {df['Fn'].mean():.2E}/N, $\sigma$ = {df['Fn'].std():.2E}/N")

# bivariate distributions

def loglog_equalaxes(label1, label2):
    plt.loglog(df[label1], df[label2], 'o')
    # set equal axes
    minimum = min(df[label1].min(), df[label2].min())
    maximum = max(df[label1].max(), df[label2].max())
    plt.xlim((minimum, maximum))
    plt.ylim((minimum, maximum))
    plt.loglog(df[label1], df[label2], 'o')

def plot_k_sn():
    loglog_equalaxes('sn', 'k')
    plt.xlabel('Deflection in mm')
    plt.ylabel('Spring Constant in N/mm')

def plot_Lo_nv():
    plt.xlabel('Active Coils')
    plt.ylabel('Equilibrium Length in mm')
    loglog_equalaxes('nv', 'Lo')

def plot_Fn_ar():
    plt.xlabel('Aspect Ratio')
    plt.ylabel('Maximum Force in N')
    loglog_equalaxes('ar', 'Fn')

def plot_Fn_sn():
    plt.xlabel('Maximum Force in N')
    plt.ylabel('Maximum Deflection in mm')
    loglog_equalaxes('sn', 'Fn')

def plot_Lo_Dm():
    plt.xlabel('Coil Diameter in mm')
    plt.ylabel('Equilibrium Length in mm')
    loglog_equalaxes('Dm', 'Lo')

def plot_Fn_sn():
    plt.xlabel('Maximum Displacement in mm')
    plt.ylabel('Maximum Force in N')
    loglog_equalaxes('sn', 'Fn')

def plot_Dm_Dt():
    plt.xlabel('Coil diameter in mm')
    plt.ylabel('Wire thickness in mm')
    loglog_equalaxes('Dm', 'Dt')

def plot_xy_all_z(x, y, xlabel=None, ylabel=None):
    if xlabel is None:
        xlabel = x
    if ylabel is None:
        ylabel = y
    for col in df.columns:
        if col == x or col == y:
            continue 
        plt.figure()
        plt.title('Legend is ' + col)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        if df.dtypes[col] == 'float64':
            plt.scatter(np.log(df[x]), np.log(df[y]), c=df[col])
        else:
            for n, gr in df.groupby(col):
                plt.loglog(gr[x], gr[y], 'o', label=n)

def plot_Fn_alpha():
    plot_xy_all_z('alpha', 'Fn',
            xlabel='$\\alpha$ in deg.',
            ylabel='Maximum Force in N')

def plot_Fn_Dm():
    x = np.log(df['Dm'])
    y = np.log(df['Fn'])

    plt.loglog(df['Dm'], df['Fn'], 'o')

    plt.xlabel('Coil Diameter in mm')
    plt.ylabel('Maximum Force in N')

def plot_Lst_al():
    plt.xlabel('Calculated arc length')
    plt.ylabel('Approximate solid length')
    plt.loglog(df['cd'], df['al'], 'o')

# systematic

def lowest_corrs():
    # used to empirically find the design variables
    l = []
    corrs = df.corr()
    for col in corrs.columns:
        s = corrs[col].abs()
        s = s.sort_values()
        label = s.index[0]
        value = s.loc[label]
        tup = col, label, round(value, 3)
        print(*tup, sep='\t')
        l.append(tup)

    col, label, vals = zip(*l)
    s = pd.Series(label)
    print(s.value_counts())

def plot_inds():
    inds = 'Dm', 'Dt', 'Lo', 'nv'
    for i in inds:
        for j in inds:
            if i < j:
                plt.figure()
                plt.xlabel(i)
                plt.ylabel(j)
                loglog_equalaxes(i, j)

                slope, inter, r2, sigma, pval = linregress(np.log(df[i]), np.log(df[j]))
                A = np.exp(inter)
                xn, xx = df[i].min(), df[i].max()
                plt.loglog((xn, xx), (A*xn**slope, A*xx**slope), '-')
                #
                plt.title(f'$n$ = {slope:.2f}, $R^2$ = {r2:.3f}')


def definition_checks():
   ## data checks on definitions

    plt.figure()
    plot_LolessLn_sn()

    plt.figure()
    plot_c_k()

def data_checks():
    ## other data checks
    plt.figure()
    plot_g()

    plt.figure()
    plot_alpha()

    plt.figure()
    plot_Fn_Fncalc()


def distributions():
    ## distributions
    plt.figure()
    plot_k()

    plt.figure()
    plot_cd()

    plt.figure()
    plot_Fn()


def low_corrs():
    ## low correlations 
    plt.figure()
    plot_Fn_ar()

    plt.figure()
    plot_Lo_nv()

    plt.figure()
    plot_k_sn()

    plt.figure()
    plot_Fn_sn()

    plt.figure()
    plot_Fn_sn()

def high_corrs():
    ## high correlations
    plt.figure()
    plot_Lo_Dm()

    plt.figure()
    plot_Lst_al()

    plt.figure()
    plot_Fn_Dm()

    plt.figure()
    plot_Dm_Dt()
    print('average ratio coil diameter to wire thickness', round((df['Dm'] / df['Dt']).mean(), 2))

def systematic():
    ## systematic, many plot routines

    plot_Fn_alpha() # clusters in max force w.r.t alpha are unexplained except by page number
    
    plot_inds()

def tabulation():
    lowest_corrs()

if __name__ == '__main__':

    definition_checks()
    data_checks()
    distributions()
    low_corrs()
    high_corrs()
    #systematic()
    plt.show()

    tabulation()
