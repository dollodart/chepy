import pandas as pd
import matplotlib.pyplot as plt
dfKLL = pd.read_csv('KLL.csv', delimiter=',')
dfLMM = pd.read_csv('LMM.csv', delimiter=',')
dfMNN = pd.read_csv('MNN.csv', delimiter=',')

dfKLL['type'] = 'KLL'
dfLMM['type'] = 'LMM'
dfMNN['type'] = 'MNN'
df = pd.concat([dfKLL, dfLMM, dfMNN])

def plot_auger_spectral():
    plt.figure()
    plt.plot(dfKLL['E'], dfKLL['Z'], 'ko')
    plt.plot(dfLMM['E'], dfLMM['Z'], 'ko')
    plt.plot(dfMNN['E'], dfMNN['Z'], 'ko')

def plot_proton_number_approx():
    plt.figure()
    plt.plot(dfKLL['E'], dfKLL['Z'].apply(lambda x: round(x)), 'ro')
    plt.plot(dfLMM['E'], dfLMM['Z'].apply(lambda x: round(x)), 'ro')
    plt.plot(dfMNN['E'], dfMNN['Z'].apply(lambda x: round(x)), 'ro')


#from ase.data import atomic_names
#df['Zround'] = df['Z'].apply(lambda x: round(x))
#df['atom'] = res['Zround'].apply(lambda x: atomic_names[x])

def identify(energy):
    """Takes the (mean) energy of the spectrum in eV and sorts the list of KLL, LMM, and MNN
    spectral lines to determine the identity of the element.  Returns a list of
    10 most likely elements in descending order."""

    df['|E-E0|'] = abs(df['E'] - energy)
    return df.sort_values(by='|E-E0|')

def plot_identify(energy):
    plot_auger_spectral()
    res = identify(energy)
    res = res.round(0)
    res = res.set_index('Z')
    plt.plot([energy] * 2, [0, df['Z'].max()])
    plt.title(res.iloc[:3].__str__() + '\nE = {} eV'.format(energy))
    plt.xlabel('Energy (eV)')
    plt.ylabel('Atomic Number')
    plt.tight_layout()

if __name__ == '__main__':
    plot_identify(400)
    plt.show()
