import pandas as pd
import matplotlib.pyplot as plt

df34 = pd.read_csv('Mn3_O4-td.csv', delimiter=',')
df23 = pd.read_csv('Mn2_O3-td.csv', delimiter=',')
df12 = pd.read_csv('Mn_O2-td.csv', delimiter=',')

long_names = df34.columns
short_names = ['T', 'Cp0', 'H0T', 'S0T', 'G0T', 'nDelfH0', 'nDelfG0']
dct = {}
for i in range(len(long_names)):
    dct[long_names[i]] = short_names[i]

# df.rename(index=str,columns=dct)
# doesn't recognize replacement
# df=pd.DataFrame(df,columns=['T','Cp0','H0T','S0T','G0T','nDelfH0','nDelfG0'])
# gives NaN

sdf34 = pd.DataFrame()
sdf23 = pd.DataFrame()
sdf12 = pd.DataFrame()
for i in long_names:
    sdf34[dct[i]] = df34[i]
    sdf23[dct[i]] = df23[i]
    sdf12[dct[i]] = df12[i]


def plot_free_energies():
    plt.figure()
    plt.xlabel('$T$/K')
    plt.ylabel('$(G^0(T) - H^0(T_{STP}))$/(kJ/mol)')  # see long column names
    plt.plot(sdf34['T'], sdf34['T'] * sdf34['G0T'] / 1000.)
    plt.plot(sdf23['T'], sdf23['T'] * sdf23['G0T'] / 1000.)
    plt.plot(sdf12['T'], sdf12['T'] * sdf12['G0T'] / 1000.)
    plt.legend(['$Mn_3O_4$', '$Mn_2O_3$', '$MnO_2$'])


def plot_formation_free_energies():
    plt.figure()
    plt.xlabel('$T$/K')
    plt.ylabel(r'-$\Delta G_f^0$/(kJ/mol)')
    plt.plot(sdf34['T'], sdf34['nDelfG0'])
    plt.plot(sdf23['T'], sdf23['nDelfG0'])
    plt.plot(sdf12['T'], sdf12['nDelfG0'])
    plt.legend(['$Mn_3O_4$', '$Mn_2O_3$', '$MnO_2$'])


if __name__ == '__main__':
    #plot_free_energies()
    plot_formation_free_energies()
    plt.show()
