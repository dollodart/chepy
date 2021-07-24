import matplotlib.pyplot as plt
import pandas as pd
from operator import itemgetter

df = pd.read_csv('element-data.csv')

def plot_boiling_points():
    plt.figure()
    plt.ylabel('Boiling Point (K)')
    x, y = zip(
        *sorted(zip(df['atomicNumber'], df['boilingPoint']), key=itemgetter(1)))
    plt.xticks(x, df['symbol'], rotation=90)
    plt.plot(sorted(df['boilingPoint']), 'ko')

def plot_vdWr_v_EA():
    plt.figure()
    plt.xlabel('Electron Affinity (J)')
    plt.ylabel('van der Waals Radius (pm)')
    plt.plot(df['electronAffinity'], df['vanDelWaalsRadius'], 'ko')

def plot_electronegativity_v_IE():
    plt.figure()
    plt.xlabel('Ionization Energy (J)')
    # if this were Mulliken electronegativity then by definition the linear
    # correlation would be exact. Mulliken and Pauling electronegativities are
    # highly correlated and so the Mulliken electronegativity and ionization
    # energy are highly correlated.
    plt.ylabel('Electronegativity (Pauling)')
    plt.plot(df['ionizationEnergy'], df['electronegativity'], 'ko')

if __name__ == '__main__':
    plot_boiling_points()
    plt.show()
