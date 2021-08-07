import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('thermal_expansion.csv', delimiter=',')
# convert from inverse difference Fahrenheit to inverse difference Kelvin
df['Lower'] = pd.to_numeric(df['Lower']) * (1. / (5. / 9))
df = df.sort_values(by='Lower')

def plot_distribution():
    plt.figure()
    plt.xlabel('Log10 Thermal Expansion Coefficient in ppm/K')
    plt.ylabel('Percentile')
    plt.title('CDF (arbitrary set of materials--Polymer-Ceramic-Metal-Composite)')
    color = df['Class'].map({'Polymer':0,'Ceramic':1,'Metal':2,'Composite':3}).values
    plt.scatter(np.log10(df['Lower']), np.linspace(0, 100, len(df)), c=color)

def plot_select(materials):
    sdf = df[df['Material'].isin(materials)]
    x = range(len(materials))

    plt.figure()
    plt.bar(x, sdf['Lower'])
    plt.xlabel('')
    plt.xticks(x, sdf['Material'], rotation=90.)
    plt.ylabel('Thermal Expansion in $10^{-6} K^{-1}$')


if __name__ == '__main__':

    # plot distribution
    plot_distribution()
    table = df.groupby('Class')['Lower'].agg(['mean', 'std'])
    print(table.sort_values(by='mean').round(2))

    select = ['Copper',
              'Quartz',
              'Glass-hard',
              'Glass-Pyrex',
              'Glass-plate',
              'Iron']

    plot_select(select)

    plt.show()
