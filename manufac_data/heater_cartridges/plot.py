import matplotlib.pyplot as plt
import pandas as pd
from chepy.manufac_data.heater_cartridges import df

def plot_x_y(x, y):
    plt.loglog(df[x], df[y], 'o')
    plt.xlabel(x)
    plt.ylabel(y)

def plot_x_y_g(x, y, g):
    g = df.groupby(g)
    for n, gr in g:
        plt.loglog(gr[x], gr[y], 'x', label=f'{n:.4f}')
    plt.xlabel(x)
    plt.ylabel(y)
    plt.legend()

def plot_current_areaoverlength():
    plot_x_y('Length/Area (1/in)', 'Current at 120 VAC single phase (A)')
    plt.title('Ohm\'s law test')

def plot_power_volume():
    plot_x_y('Volume (in^3)', 'Power (W)') 

def plot_power_current():
    """
    Since current is at fixed (RMS) voltage, by P = IV, the power must be linear with current.
    """
    plot_x_y('Current at 120 VAC single phase (A)', 'Power (W)')

def plot_power_current_density():
    plot_x_y('Current at 120 VAC single phase (A)', 'Power Density (W/in^2)')

def plot_powerdensity_length():
    plot_x_y('Element Length (in)', 'Power Density (W/in^2)')


def plot_power_volume_groupby_diameter():
    plot_x_y_g('Volume (in^3)', 'Power (W)', 'Element Diameter (in)')
    plt.title('Legend Diameter/in')

def plot_power_volume_groupby_length():
    plot_x_y_g('Volume (in^3)', 'Power (W)', 'Element Length (in)')
    plt.title('Legend Length/in')

def plot_power_volume_groupby_area():
    plot_x_y_g('Volume (in^3)', 'Power (W)', 'Area (in^2)')
    plt.title('Legend Area/in^2')

def plot_power_length_groupby_diameter():
    plot_x_y_g('Element Length (in)', 'Power (W)', 'Element Diameter (in)')
    plt.title('Legend Diameter/in')

def plot_distributions(*columns):
    """
    Plot the (cumulative) distributions.
    """
    for col in columns:
        plt.figure(col)
        plot_distributions_overlapping(col)

def plot_distributions_overlapping(*columns):
    for col in columns:
        plot, = plt.plot(df[col].sort_values(), range(len(df)), label=col)
        plt.plot([df[col].mean()]*2, [0, len(df)], plot.get_color())
        plt.plot([df[col].mean() + df[col].std()]*2, [0, len(df)], plot.get_color())
        plt.plot([df[col].mean() - df[col].std()]*2, [0, len(df)], plot.get_color())
    plt.legend()

def plot_distributions_overlapping_normalized(*columns):
    for col in columns:
        norm = df[col].max()
        plot, = plt.plot(df[col].sort_values()/norm, range(len(df)), label=col)
        plt.plot([df[col].mean()/norm]*2, [0, len(df)], plot.get_color())
        plt.plot([df[col].mean()/norm + df[col].std()/norm]*2, [0, len(df)], plot.get_color())
        plt.plot([df[col].mean()/norm - df[col].std()/norm]*2, [0, len(df)], plot.get_color())
    plt.legend()

if __name__ == '__main__':
    #plot_power_current()
    #plot_power_length_groupby_diameter()
    #plot_power_volume_groupby_diameter()
    #plot_power_volume_groupby_area()
    #plot_power_volume_groupby_length()
    #plot_power_current_density()
    #plot_current_areaoverlength()

    #plot_x_y('Heat Flux (W/in^2)', 'Power Density (W/in^2)')
    #plot_x_y('Current Density (A/in^2)', 'Power Density (W/in^2)')
    #plot_distributions_overlapping('Current Density (A/in^2)', 'Power Density (W/in^2)')
    #plot_distributions_overlapping_normalized('Heat Flux (W/in^2)', 'Power Density (W/in^2)')
    #plot_distributions_overlapping_normalized('Volumetric Heat Rate (W/in^3)', 'Power Density (W/in^2)')
    plot_distributions_overlapping_normalized('Linear Power Density (W/in)', 'Power Density (W/in^2)')

    #plot_distributions('Volumetric Heat Rate (W/in^3)')

    #plot_distributions(*df.columns)
    plt.show()
