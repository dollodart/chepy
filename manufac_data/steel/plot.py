import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('tabula-Enghandbook.csv')

sdf = df.set_index('AISI Type')
sdf = sdf.drop('UNS', axis=1)
sdf = sdf.drop('Crystal Phase', axis=1)

chems = 'Cr,Ni,C,Mn,Si,P,S,Mo,N'.split(',')

mdf = pd.DataFrame()
for chem in chems:
    l = sdf[chem + '_l']
    h = sdf[chem + '_h']
    mdf[chem] = (l + h) / 2.

def atomic_comp():

    sdf = mdf.cumsum(axis=1)
    sdf['avg'] = sdf.sum(axis=1)
    sdf = sdf.sort_values(by='avg')
    sdf = sdf.drop('avg', axis=1)

    for col in sdf.columns:
        plt.plot(sdf[col], 'x-', label=col)

    plt.legend()
    plt.xlabel('AISI Type')
    plt.ylabel('Cumulative Composition Atomic % (balance Fe)')
    plt.ylim((0, sdf.max().max() * 1.1))


if __name__ == '__main__':
    print('average compositions')
    print(mdf.mean(axis=0).sort_values())
    atomic_comp()
    plt.show()
