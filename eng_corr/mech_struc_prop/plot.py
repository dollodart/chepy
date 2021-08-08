import pandas as pd
import numpy as np

dtype = {'name':str,
         'class':str,
         'low':'float64',
         'high':'float64'}

import os.path as osp
data_dir = osp.join(osp.dirname(__file__), 'data')

df_d = pd.read_csv(osp.join(data_dir, 'densities.csv'),dtype=dtype)
df_ft = pd.read_csv(osp.join(data_dir, 'fracture-toughness.csv'),dtype=dtype)
df_mp = pd.read_csv(osp.join(data_dir, 'melting-points.csv'),dtype=dtype)
df_mp['low'] = df_mp['low'] + 273.15 # to K
df_mp['high'] = df_mp['high'] + 273.15 # to K
df_ym = pd.read_csv(osp.join(data_dir, 'youngs-modulus.csv'),dtype=dtype)
df_ysts = pd.read_csv(osp.join(data_dir, 'yield-stress-tensile-strength.csv'),
        dtype={'name':str,'class':str,
               'yield stress low':'float64',
               'yield stress high':'float64',
               'tensile strength low':'float64',
               'tensile strength high':'float64'})
# for ceramics, this is actually compressive strength
# and so renamed "strength"
# class,name,yield stress low,yield stress high,tensile strength low,tensile strength high
df_ys = df_ysts[['class','name','yield stress low', 'yield stress high']]
df_ys.columns = ['class', 'name', 'low', 'high']
df_s = df_ysts[['class','name','tensile strength low','tensile strength high']]
df_s.columns = ['class', 'name', 'low', 'high']

for n, df in (('density', df_d), 
                ('fracture toughness', df_ft),
                ('melting point', df_mp),
                ('youngs modulus', df_ym),
                ('yield stress', df_ys),
                ('strength', df_s)):

    df['name'] = (df['name'].str.replace('(*)','', regex=False)
                 .str.replace('\([a-z]\)','',regex=True)
                 .str.replace('\([A-Z]\)', '', regex=True)
                 .str.strip())
    table = df.groupby('class').agg(['mean','std'])
#    print(n)
#    print(table.sort_values(by=('low','mean')))

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

cdct = dict(Metal=(1,0,0),Ceramic=(0,1,0),Polymer=(0,0,1))

def plot_join(df1, df2, ax):
    df3 = df1.merge(df2, how='inner', on=['name','class'])
    for i,r in df3.iterrows():
        ax.annotate(r['name'], (np.log10(r['high_x']), np.log10(r['low_y'])))
        x = (np.log10(r['low_x']) + np.log10(r['high_x'])) / 2
        y = (np.log10(r['low_y']) + np.log10(r['high_y'])) / 2
        width = np.log10(r['high_x']) - np.log10(r['low_x'])
        height = np.log10(r['high_y']) - np.log10(r['low_y'])
        e = Ellipse(xy = (x,y), width=width, height=height, angle=0)
        e.set_facecolor(cdct[r['class']])
        ax.add_artist(e)

def reproduce_source():
    fig, axs = plt.subplots(nrows=2,ncols=2)
    ax = axs[0,0]
    plot_join(df_d, df_ym, ax)
    ax.set_xlabel('Log10 Density in g/cm$^3$')
    ax.set_ylabel('Log10 Young\'s Modulus in MPa')
    ax.set_xlim(-1, 3)
    ax.set_ylim(-3, 3)

    ax = axs[1,0]
    plot_join(df_d, df_s, ax)
    ax.set_xlabel('Log10 Density in g/cm$^3$')
    ax.set_ylabel('Log10 Strength in MPa')
    ax.set_xlim(-1, 3)
    ax.set_ylim(1, 4)

    ax = axs[0,1]
    plot_join(df_s, df_ym, ax)
    ax.set_xlabel('Log10 Strength in MPa')
    ax.set_ylabel('Log10 Young\'s Modulus in MPa')
    ax.set_xlim(1, 4)
    ax.set_ylim(-3, 3)

    ax = axs[1,1]
    plot_join(df_s, df_ft, ax)
    ax.set_xlabel('Log10 Strength in MPa')
    ax.set_ylabel('Log10 Fracture Toughness in MPa$*$m$^{1/2}$')
    ax.set_xlim(1, 4)
    ax.set_ylim(-2, 3)

if __name__ == '__main__':
    #reproduce_source()

    # other correlations
    fig, ax = plt.subplots(nrows=1,ncols=1)
    plot_join(df_mp, df_d, ax)
    ax.set_xlim(2, 4)
    ax.set_ylim(-1, 3)
    ax.set_xlabel('Log10 Temperature in K')
    ax.set_ylabel('Log10 Density in g/cm$^3$')

    fig, ax = plt.subplots(nrows=1,ncols=1)
    plot_join(df_s, df_ys, ax)
    plt.plot([1, 4], [1,4], 'k-')
    ax.set_xlabel('Log10 Strength in MPa')
    ax.set_ylabel('Log10 Yield Stress in MPa')
    ax.set_xlim(1, 4)
    ax.set_ylim(1, 4)
    
    # yield stress (yield strain divided by youngs modulus)
    # young's modulus is reported in GPa, strength in MPa
    # spurious numeric index matching when using "casting" operations
    # merge on columns
    df = df_ys.merge(df_ym, how='inner', on=['class','name'])
    s_usl = df['low_x'] / (df['low_y']*1e3) # ultimate strain
    s_ush = df['high_x'] / (df['high_y']*1e3)
    df_us = df_s.copy()
    df_us['low'] = s_usl
    df_us['high'] = s_ush

    #print(df_us.groupby('class').agg(['mean','std']))

    fig, ax = plt.subplots(nrows=1,ncols=1)
    plot_join(df_d, df_us, ax)
    ax.set_xlabel('Log10 Density in g/cm$^3$')
    ax.set_ylabel('Log10 Yield Strain')
    ax.set_xlim(-1, 3)
    ax.set_ylim(-3,1)
    plt.show()
