import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('std-pot.csv', delimiter=',')
df = df.sort_values(by='E0(V)')

ndf1 = df['Oxidant'].str.split('\\s\\+\\s',expand=True)
ndf2 = df['Reductant'].str.split('\\s\\+\\s',expand=True)

def plot_species(species):
    bl = ndf1[0].str.startswith(species[0]) | ndf2[0].str.startswith(species[0])
    for s in species[1:]:
        bl |= ndf1[0].str.startswith(s) | ndf2[0].str.startswith(s)

    plt.plot(range(bl.sum()), df['E0(V)'][bl])
    #names = ndf1[bl][0]
    names = df['Oxidant'][bl]
    plt.xticks(range(bl.sum()), names, rotation=90)
    plt.xlabel('Oxidation Half-Reaction')
    plt.ylabel('$E^0$/V')
    plt.tight_layout()

if __name__ == '__main__':
    plot_species(['Cu', 'Fe'])
    plt.show()
