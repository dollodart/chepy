import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.cm import rainbow

df = pd.read_csv('liq-n2-visc.csv'
        ,skiprows=[1]
        ,dtype={'T':'float64'
                ,'P':'float64'
                ,'eta':'float64'})

df['P'] = df['P'] * .1 # to MPa
Tmax = df['T'].max()
df['Tscale'] = df['T']/Tmax

def plot_eta_P():
    plt.figure()
    for temp, gr in df.groupby('Tscale'):
        x = gr['P']
        y = gr['eta']
        plt.plot(x, y, c=rainbow(temp),label=temp*Tmax)
    plt.xlabel('Pressure/MPa')
    plt.ylabel('Viscosity/uPa*s')
    plt.title('Legend Temperature in K')
    plt.legend()

# (linear) interpolation is needed for pressure which wasn't a held variable but which varies fractionally slightly
# to make isobars, a simpler but less precise alternative is to simply round to the nearest pressure
df['P'] = df['P'].round() # round to nearest MPa
Pmax = df['P'].max()
df['Pscale'] = df['P']/Pmax

def plot_eta_T():
    plt.figure()
    for press, gr in df.groupby('Pscale'):
        x = gr['T']
        y = gr['eta']
        plt.plot(x, y, c=rainbow(press),label=press*Pmax)
    plt.xlabel('Temperature/K')
    plt.ylabel('Viscosity/uPa*s')
    plt.title('Legend Pressure in MPa')
    plt.legend()

if __name__ == '__main__':
    plot_eta_P()
    plt.show()
