import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import floor

import os.path as osp
f = __file__
f = osp.join(osp.dirname(f), 'T-dep-rho-data.csv')

df = pd.read_csv(f, delimiter=',', index_col=0)
temperature = np.arange(0., 3000., 5.)  # K
temperature0 = 273.15  # K

def plot_rho_v_T(elements):
    plt.figure()
    sdf = df.loc[some]
    for i in range(len(sdf)):
        resistivity0 = sdf['Resistivity'].iloc[i]
        alpha = sdf['Temperature coefficient'].iloc[i]
        resistivity = resistivity0 
        resistivity *= (1 + alpha * (temperature - temperature0))
        resistivity *= 1.e9
        plt.plot(temperature, resistivity)
    plt.xlabel('Temperature in K')
    plt.ylabel(r'Resistivity in $\Omega\cdot$nm')
    plt.legend(some)

if __name__ == '__main__':
#    plot_rho_v_T(['Tungsten'])

    df = df.sort_values(by='Resistivity')
    x = len(df) / 3.
    for i in range(3):
        some = df.index[floor(x*i):floor(x*(i+1))]
        plot_rho_v_T(list(some))
    plt.show()
