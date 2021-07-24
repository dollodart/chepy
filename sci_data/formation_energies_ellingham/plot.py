import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('data-clean.csv')
df = df.sort_values(by='dGf0 (kJ/mol)')

def plot(bl):
    plt.plot(df['chemical formula'][bl], df['dGf0 (kJ/mol)'][bl], 'o')
    plt.xticks(rotation=90)
    plt.xlabel('Oxide')
    plt.ylabel('$\Delta G_f^\ominus$')

if __name__ == '__main__':
    bl = df['phase'] == 'solid'
    #bl &= df['species'].str.contains('Oxide')
    plot(bl)
    bl = df['phase'] == 'aqueous'
    #bl &= df['species'].str.contains('Oxide')
    plot(bl)
    plt.legend(['solid','aqueous'])
    plt.tight_layout()
    plt.show()
