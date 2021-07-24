import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('oxides-mp.csv', delimiter=',')
df['MP'] = df['MP'] + 273.15
df['Oxide MP'] = df['Oxide MP'] + 273.15
df = df.sort_values(by='Element')
rng = range(len(df))

def plot_univar():
    plt.figure()
    plt.xlabel('Chemical Symbol')
    plt.ylabel('Melting Point in Kelvin')
    plt.xticks(rng, df['Element'])
    plt.plot(rng, df['MP'])
    plt.plot(rng, df['Oxide MP'])
    plt.legend(['Element', 'Oxide'])
    plt.ylim((0,None))

def plot_bivar():
    fig, ax = plt.subplots()
    ax.set_title(f'Pearson Corr. Coeff. {df["MP"].corr(df["Oxide MP"]):.2f}')
    plt.xlabel('Element MP in Kelvin')
    plt.ylabel('Oxide MP in Kelvin')
    ax.scatter(df['MP'], df['Oxide MP'])
    for i, txt in enumerate(df['Element']):
        ax.annotate(txt, (df['MP'].iloc[i], df['Oxide MP'].iloc[i]))
    ax.set_xlim((0,None))
    ax.set_ylim((0,None))

def plot_bivar_split():
    fig, ax = plt.subplots()
    plt.xlabel('Element MP in Kelvin')
    plt.ylabel('Oxide MP in Kelvin')
    bl = df['Element'].isin(['Zn','Al','Ce','Ca','Mg'])
    ax.set_title(f'Pearson Corr. Coeff. ' + 
                 f'{df["MP"][bl].corr(df["Oxide MP"][bl]):.2f} ' + 
                 f'{df["MP"][~bl].corr(df["Oxide MP"][~bl]):.2f}')

    ax.scatter(df['MP'][bl], df['Oxide MP'][bl])
    ax.scatter(df['MP'][~bl], df['Oxide MP'][~bl])

    for i, txt in enumerate(df['Element']):
        ax.annotate(txt, (df['MP'].iloc[i], df['Oxide MP'].iloc[i]))
    ax.set_xlim((0,None))
    ax.set_ylim((0,None))

if __name__ == '__main__':
#    plot_univar()
#    plot_bivar()
    plot_bivar_split()
    plt.show()
