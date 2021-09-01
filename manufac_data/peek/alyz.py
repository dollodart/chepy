import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('init-data.csv')
df = df.sort_values(by='Tubing ID')
df['Fractional Tolerance'] = df['Tolerance'] / df['Tubing ID']
ul2in3 = .000061 # factor for uL to inch^3
in2cm = 2.54
df['Area'] = df['Tubing ID']**2 / 4. * np.pi
flow_rate = 10. * ul2in3 
g = 9.81  # m/s^2
Cd = 1.10

def color_t(color_str):
    if color_str.lower() == 'orange':
        return 'm'
    elif color_str.lower() == 'black':
        return 'k'
    else:
        return color_str[0].lower()

# superficial velocity (by material balance)
df['Superficial Velocity'] = flow_rate / df['Area']
# Hagen-Poiseulle Equation
df['Pressure Drop'] = (flow_rate / ul2in3 / 1e9) * 8 * \
    0.001 / (np.pi * (df['Tubing ID'] / in2cm / 100) ** 4 / 16)

def plot_diameter():
    # test geometric series
    plt.xlabel('PEEK Color')
    plt.ylabel('$\log_2$ Tubing ID - min($\log_2$ Tubing ID)')
    y = np.log2(df['Tubing ID'])
    plt.bar(df['Color'], y - y.min())

def plot_fractional_tolerance():
    plt.bar(df['Color'], df['Fractional Tolerance'] * 100)
    plt.xlabel('PEEK Color')
    plt.ylabel('Fractional Tolerance in %')

def _plot_x_y_groupby_color(x, y):
    for n, gr in df.groupby('Color'):
        plt.loglog(gr[x], gr[y], 'o', color=color_t(n), label=n)

def plot_fractional_tolerance_diameter():
    _plot_x_y_groupby_color('Tubing ID', 'Fractional Tolerance')
    plt.xlabel('Tubing ID in inches')
    plt.legend()
    plt.ylabel('Fractional Tolerance in %')

def plot_superficialvelocity():
    _plot_x_y_groupby_color('Tubing ID', 'Superficial Velocity')
    plt.xlabel('Tubing ID in inches')
    plt.ylabel('Superficial Velocity in in/min')
    plt.title('Flow Rate = {:.2f} ul/min'.format(flow_rate / ul2in3))
    plt.legend()

def plot_hagen_poiseulle():
    _plot_x_y_groupby_color('Tubing ID', 'Pressure Drop')
    plt.xlabel('Tubing ID in inches')
    plt.ylabel('Pressure Drop in kPa/in')
    plt.title('Flow Rate = {:.2f} ul/min'.format(flow_rate / ul2in3))
    plt.legend()

# free fall discharge equation
def plot_discharge():
    ymax = .1
    for n, gr in df.groupby(['Color', 'Area']):
        c, a = n
        s = flow_rate / a * 2.54 / 1000  # to SI
        xmax = np.sqrt(2 * ymax / g) * s / Cd
        x = np.arange(0, xmax, 0.001)  # m
        y = g * (Cd * x / s)**2 / 2  # parabolic free fall
        # why is Cd included?
        plt.plot(100. * x, 100. * y, color_t(c), label=c)

    plt.xlabel('Horizontal Distance in cm')
    plt.ylabel('Vertical Distance in cm')
    plt.title('Flow Rate = {:.2f} ul/min'.format(flow_rate / ul2in3))
    plt.legend()

if __name__ == '__main__':
    plt.figure()
    plot_diameter()
    plt.figure()
    plot_fractional_tolerance_diameter()
    plt.figure()
    plot_fractional_tolerance()
    plt.figure()
    plot_superficialvelocity()
    plt.figure()
    plot_hagen_poiseulle()
    plt.figure()
    plot_discharge()
    plt.show()
