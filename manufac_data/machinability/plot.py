import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

frames = []
for i in range(1, 7):
    frames.append(pd.read_csv('t' + str(i) + '.csv', delimiter=','))
df = pd.concat(frames)
df1 = df[['MATERIAL', 'MR']].copy()
df2 = pd.DataFrame(columns=['MATERIAL', 'MR', 'BHN'])
df2[['MATERIAL', 'MR', 'BHN']] = df[['MATERIAL.1', 'MR.1', 'BHN.1']].copy()
dfn = pd.concat([df1, df2])

def plot_MR():
    dfn = dfn.sort_values(by='MR')
    plt.plot(dfn['MR'], range(len(dfn)))
    plt.xlabel('MR')
    plt.ylabel('ascending index')

def plot_BHN():
    dfn = dfn.sort_values(by='BHN')
    plt.plot(dfn['BHN'], range(len(dfn)))
    plt.xlabel('BHN')
    plt.ylabel('ascending index')

def plot_MR_BHN():
    from scipy.stats import linregress
    dfnn = dfn.dropna()
    s, i, *_ = linregress(np.log(dfnn['BHN'].values), np.log(dfnn['MR'].values))
    y = dfnn['BHN']**s * np.exp(i)
    plot, = plt.loglog(dfnn['BHN'], y, '-')
    plt.loglog(dfn['BHN'], dfn['MR'], 'x', color = plot.get_color())

    for c, row in dfn.iterrows():
        plt.annotate(row['MATERIAL'], (row['BHN'], row['MR']))

    plt.xlabel('BHN')
    plt.ylabel('MR')
    plt.title(f'$MR = BHN^{{{s:.3f}}} e^{{{i:.3f}}}$')

if __name__ == '__main__':
    plt.figure()
    plot_MR_BHN()
    plt.show()
