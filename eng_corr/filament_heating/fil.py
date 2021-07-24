import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from chepy.sci_data.fundamental_constants import stefan_boltzmann_constant as sigma
from chepy.eng_data.metals_resistivities import df

# all quantities in SI units
epsilon = 1.
voltage = 1.
length = 10.e-2
resistivity0, conductivity0, alpha = df.loc['Tungsten']  # in SI units
temperature0 = 293.

def iter_solve_I_T(D):
    condition = True
    temperature = temperature_old = temperature0 = 293.
    while condition:
        resistivity = resistivity0 * (1 + alpha * (temperature - temperature0))
        # it's likely the linear approximation for temperatue dependent
        # resistivity fails in which case a polynomial function fit to data
        # should be used (see metals-resistivities)
        area = np.pi * D**2 / 4.
        resistance = resistivity * length / area
        current = voltage / resistance
        power = voltage**2 / resistance
        area = np.pi * D * length
        temperature = (power / (area * sigma * epsilon) +
                       temperature0**4)**(1 / 4)

        condition = abs((temperature_old - temperature) / temperature) > 0.02
        condition = condition.all()
        temperature_old = temperature
    return current, temperature


def plot_D_vs_I_T(diam=np.arange(1, 100., 0.01) * 1e-6):
    current, temperature = iter_solve_I_T(diam)
    plt.figure()
    plt.plot(diam * 1.e6, current, 'k-')
    plt.xlabel('$D$/um')
    plt.ylabel('$I$/A')
    plt.title(
        r'$\sigma=${0:.2E},$\varepsilon=${1:.2E},$\Delta V=${2:.2E},$L=${3:.2E},$\rho_0$={4:.2E}'.format(
            sigma,
            epsilon,
            voltage,
            length,
            resistivity0))
    plt.figure()
    plt.plot(diam * 1.e6, temperature, 'k-')
    plt.xlabel('$D$/um')
    plt.ylabel('$T$/K')
    plt.title(
        r'$\sigma=${0:.2E},$\varepsilon=${1:.2E},$\Delta V=${2:.2E},$L=${3:.2E},$\rho_0$={4:.2E}'.format(
            sigma,
            epsilon,
            voltage,
            length,
            resistivity0))


def plot_D_vs_R(diam=np.linspace(1.e-6, 1000.e-6, 100)):
    plt.figure()
    resistance = resistivity0 * length / (np.pi * diam**2 / 4)
    plt.plot(diam * 1.e6, np.log10(resistance))
    resistivity = resistivity0 * (1 + alpha * (2000. - temperature0))
    resistance = resistivity * length / (np.pi * diam**2 / 4)
    plt.plot(diam * 1.e6, np.log10(resistance))
    plt.legend(['T=298K', 'T=2000K'])
    plt.xlabel('$D$/um')
    plt.ylabel(r'$\log_{10} R$/Ohm')
    plt.title('$l=10$cm')


def solve_I_T(power, D):
    """Advantage to specifying just voltage is that the temperature is found
    only by the power. Then the resistance is calculated by the temperature
    found by heat balance. From here, there are two equations in two unknowns
    for current and voltage, P=IV and V=IR. Then I and V may be solved for
    independently and no loop is needed."""
    condition = True
    temperature = (power / (np.pi * D * length * sigma *
                            epsilon) + temperature0**4)**(1 / 4)
    resistivity = resistivity0 * (1 + alpha * (temperature - temperature0))
    area = np.pi * D**2 / 4.
    resistance = resistivity * length / area
    current = (power / resistance)**(1 / 2)
    voltage = current * resistance
    return current, temperature


def plot_P_vs_T(D=1.e-3, power=np.linspace(0., 50. * 5., 100)):
    plt.figure()
    current, temperature = solve_I_T(power, D)
    plt.plot(power, temperature)
    plt.xlabel('Power in W')
    plt.ylabel('Temperature in K')
    plt.title(f'D={D:.2E}')


if __name__ == '__main__':
#    plot_D_vs_I_T()
    plot_P_vs_T()
    plt.show()
