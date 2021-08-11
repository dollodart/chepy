import numpy as np
import pandas as pd
from scipy.stats import linregress
from scipy.optimize import minimize_scalar
import matplotlib.pyplot as plt

df = pd.read_csv('flanges.csv', delimiter=',')

def plot_fits_(x, y):
    s, i, *_ = linregress(x, y)
    plt.plot(x, s*x + i, '-', label="fit with intercept")

    def residual(m):
        return sum(pow(y - m*x, 2))

    res = minimize_scalar(residual, bracket=(y.min()/x.mean(),y.mean()/x.mean(),y.max()/x.mean()))
    m = res.x
    plt.plot(x, m*x, '-', label="fit without intercept")

    plt.title(f'slope={s:.2f} intercept={i:.2f}in or slope={m:.2f}in')


def plot_tube_v_flange():
    """Flange size (diameter) versus nominal tube diameter."""
    plt.figure('Nominal Tube Diameter')
    plt.plot(df['Flange Size'], df['Nominal Tube Diameter'], 'o')
    plt.xlabel('Flange Size (in)')
    plt.ylabel('Nominal Tube Diameter (in)')

    x = df['Flange Size'].values
    y = df['Nominal Tube Diameter'].values

    plot_fits_(x,y)

    plt.xlim((0, None))
    plt.ylim((0, None))

    plt.legend()

def plot_holes_v_flange():
    plt.figure('Holes')
    x = df['Flange Size']
    y = df['Number of Holes']
    plt.plot(x, y, 'o')
    plot_fits_(x,y)
    plt.xlabel('Flange Size (in)')
    plt.ylabel('Number of Holes')
    plt.yticks(range(2, 25, 2))

def plot_hole_separation():
    plt.figure('Separation')

    angle_sep = 2. * np.pi / df['Number of Holes']  # in radians
    circ = np.pi * df['Bolt Circle Diameter']  # circumfrence
    arc_sep = angle_sep / (2 * np.pi) * circ
    line_sep = 2. * (df['Bolt Circle Diameter'] / 2.) * np.sin(angle_sep / 2.)

    plt.xlabel('Flange Size (in)')
    plt.ylabel('Hole Separation (in)')
    plt.plot(df['Flange Size'], arc_sep, 'o', label='Arc')
    plt.plot(df['Flange Size'], line_sep, 'o', label='Line')
    plt.legend()

if __name__ == '__main__':
    plot_tube_v_flange()
    plot_holes_v_flange()
    plot_hole_separation()
    plt.show()
