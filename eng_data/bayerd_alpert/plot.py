import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    'bayerd-alpert-sensitivity-crc.csv',
    delimiter=',',
    index_col=0)

def plot_sens_by_form():
    plt.figure()
    plt.xlabel('Molecular Formula')
    plt.ylabel('RSF')
    plt.xticks(rotation=90)
    plt.plot(df['Mol. Form.'], y, 'ko')

def plot_sens_v_mw():
    plt.figure()
    plt.xlabel('Molecular Weight (g/mol)')
    plt.ylabel('RSF')
    x = df['Mol. Wt.']
    plt.plot(x, y, 'ko')
    rho = x.corr(y) 
    plt.title(f'{rho:.2f}')
    for i in range(len(df)):
        plt.annotate(df['Mol. Form.'].iloc[i], (x.iloc[i], y.iloc[i]))

from chepy.utils.string2symbols import string2symbols

def plot_sens_v_avg_am():
    plt.figure()
    plt.xlabel('Average Atomic Mass')
    plt.ylabel('RSF')
    df['Num. Atoms'] = df['Mol. Form.'].map(string2symbols)
    x = df['Mol. Wt.'] / df['Num. Atoms']
    plt.plot(x, y, 'bo')
    rho = x.corr(y)
    plt.title(f'{rho:.2f}')

    for i in range(len(df)):
        plt.annotate(df['Mol. Form.'].iloc[i], (x.iloc[i], y.iloc[i]))
        
# filters hydrocarbon
def is_hydrocarbon(s):
    if s[-2:] == 'CH' and s[:-2].isdigit():
        return True
    return False

df['is hydrocarbon'] = df['Mol. Form.'].map(sorted).map(''.join).map(is_hydrocarbon)
df['is noble gas'] = df['Mol. Form.'].isin(['Ar','He','Ne','Xe','Kr'])

def apply_filter(fltr):
    sdf = df[df[fltr]]
    sy = sdf['Relative sensitivity to N2']
    return sdf, sy

if __name__ == '__main__':
    #df, y = apply_filter('is noble gas')
    #df, y = apply_filter('is hydrocarbon')
    y = df['Relative sensitivity to N2']

#    plot_sens_v_avg_am()
    plot_sens_v_mw()
    plt.show()
