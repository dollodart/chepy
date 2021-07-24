import pandas as pd
import matplotlib.pyplot as plt

df1 = pd.read_csv('work-functions.csv')
df2 = pd.read_csv('metals-fermi-levels.csv')

def plot_work_funcs():
    df = df1.sort_values(by='Min/Exact')
    plt.xticks(range(len(df)), df['Element'], rotation=90)
    for i in range(len(df)):
        a = df.iloc[i]
        if str(a['Max']) == 'nan':
            plt.plot(i, a['Min/Exact'], 'ko')
        else:
            plt.plot([i, i], [a['Min/Exact'], a['Max']], 'k-')
    # plt.plot(range(len(df)),df['Min/Exact'],'o')
    # plt.plot(range(len(df)),df['Max'],'o')
    plt.ylabel(r'$\phi$/eV')
    plt.xlabel('Element')

def plot_fermi_levels():
    df = df2.sort_values(by='Fermi Energy eV')
    x = range(len(df))
    plt.plot(x, df['Fermi Energy eV'], 'o')
    plt.xticks(x, df['Element'])
    plt.xlabel('Element')
    plt.ylabel('$E_f$/eV')

def plot_fermi_work(exclude_relativistic_metals=False):
    df = df1.merge(df2,how='inner',on='Element')
    ax = df.plot(x='Min/Exact',y='Fermi Energy eV',kind='scatter')
    #ax2 = df2.plot(x='Max',y='Fermi Energy eV',kind='scatter')
    for i in range(len(df)):
        a = df.iloc[i]
        plt.annotate(a['Element'], (a['Min/Exact'],a['Fermi Energy eV']))
    ax.set_xlim((0,None))
    ax.set_ylim((0,None))

    from scipy.stats import linregress
    if exclude_relativistic_metals:
        relativistic = ['Cu','Au','Ag','Hg','Cs']
        df = df[~df['Element'].isin(relativistic)]
        title = 'excluding relativistic:' + ','.join(relativistic) + '\n'
    else:
        title = ''
    x = df['Min/Exact'].tolist()
    y = df['Fermi Energy eV'].tolist()
    s, i, r2, sigma, p = linregress(x, y)
    ax.plot([0, max(x)], [i, s*max(x) + i], 'k-')
    title += f'$R^2$ = {r2:.2f}'
    ax.set_title(title)

if __name__ == '__main__':
    #plot_work_funcs()
    #plot_fermi_levels()
    plot_fermi_work(exclude_relativistic_metals=True)
    #plot_fermi_work()
    plt.show()
