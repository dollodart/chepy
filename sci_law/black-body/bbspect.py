import numpy as np
import matplotlib.pyplot as plt
from chepy.sci_data.fundamental_constants import h, kB, c
from math import floor

alpha = 2 * h / c**2  # J*s/(m/s)^2=J*s^3/m^2 = kg*s
beta = h / kB  # J*s/(J/K) = K*s

#print(f'alpha={alpha:.2E}kg*s\n' + 
#      f'beta={beta:.2E}K*s')

def blterm(nuoverT):
    if beta * nuoverT > 5:
        return beta * nuoverT * np.log10(np.exp(1.))
    return np.log10(np.exp(beta * nuoverT) - 1.)

blterm = np.frompyfunc(blterm, 1, 1) # creates numpy ufunc

def logB(nu, T):
    return np.log10(alpha) + 3 * np.log10(nu) - blterm(nu/T)

lmbds = np.arange(380., 740., 10.) * 1.e-9  # m
nus = c / lmbds

# quantify these entry and exit points of visibility based on retina sensitivity 
# see color-per

# the two different formulaes reported for the spectral intensity are
# different, hence subscripting, that is, B_nu != B_lambda, by a factor of
# the speed of light
Tlb = 300. + 273.15
Tub = 1500. + 273.15
Trange = np.linspace(Tlb, Tub, 20)

Trange, nus = np.meshgrid(Trange, nus, indexing='ij')
# T varies along col (const. along row), nu varies along row (const. along col)

y1 = logB(nus, Trange)
y = 10**(y1 - np.log10(h * nus) + np.log10(c))
dx = lmbds[1:] - lmbds[:-1]
integral = y[:,:-1] @ dx 
# col sum (=sum of columns), usual matrix operation, integrating with respect to nu (which varies along row)
# ensure correct units (and integration variable), but oom and trends appear as expected

def plot_spectrum():
    Bnu_format = r'$B_\nu/(m^{-2}\cdot s^{-1}\cdot Hz^{-1})$'

    fig, ax = plt.subplots()
    ax.set_title('Spectrum at Different Temperatures')
    ax.set_xlabel('Wavelength in nm')
    ax.set_ylabel(Bnu_format)
    ax.semilogy(lmbds*1.e9,y.transpose())
    ax.legend(tuple(f'{x:.0f}' for x in Trange[:,0]))

def plot_integrated_spectrum():
    Bnu_integral_fmt = r'$\int_{\nu_r}^{\nu_b} \tilde{B}_\nu \, d\nu / (m^{-2}\cdot s^{-1})$'
    # I didn't integrate with respect to frequency according to the definition of B_\nu
    # but with respect to wavelength

    fig, ax = plt.subplots()
    ax.set_title('Integrated Spectrum over Visible Range versus Temperature')
    ax.set_xlabel('Temperature in K')
    ax.set_ylabel(Bnu_integral_fmt)
    ax.semilogy(Trange[:,0], integral, 'b-')
    ax.semilogy([798, 798], [min(integral), max(integral)], 'k-', label='draper point')
    ax.legend()

def plot_spectrum_contour():

    fig, ax = plt.subplots()
    # W / (m^2 * s * Hz) = 10^(3 - 4 + 12) mW / (cm^2 * s * TH)
    CS = ax.contour(nus / 1.e12, Trange - 273.15, y1 + 13)
    ax.clabel(CS, inline=1, fmt='%1.1f')
    ax.set_xlabel('Frequency in THz')
    ax.set_ylabel('Temperature in deg. C')
    ax.set_title('Base-10 Logarithm Black Body Intensity in $mW/(cm^2\cdot s \cdot THz)$')

def verify_Draper_point():
    """Use the photon sensitivity of the eye to demonstrate the empirical
    Draper point.  5 to 9 photons must arrive within 0.1 s for the brain to
    register a color, from Julie Schanpg "How photoreceptors respond to light",
    Scientific American, April 1987.  However, this is in the absence of other
    light sources, and daylight is very intense relative to this. Note you
    might see something, if not perceive a color, at a significantly lower
    photon rate."""

    T = Trange[:, 0]
    i = np.argmin( (T - 798.)**2 ) # the Draper point is 798 K
    retina_area = 1094 * 1.e-6  # m^2,taken from medical school of Utah
    imp = integral[i] * retina_area
    Fsol = 4.3e21  # s^-1/m^2
    impsol = Fsol * retina_area
    print(f'Required Photon Rate on Retina for Color Perception = {5/.1:.0f}--{9/.1:.0f}/s')
    print(f'Black-Body Photon Rate on Retina @ Draper Point={imp:.2E}/s')
    print(f'Ratio Black-Body @ Draper Point to Required = {imp/(5/.1):.2f}--{imp/(9/.1):.2f}')
    print(f'Solar Spectrum Photon Rate on Retina={impsol:.2E}/s')
    print(f'Ratio Black-Body @ Draper Point to Solar={imp/impsol:.2E}')

if __name__ == '__main__':
    verify_Draper_point()
    plot_spectrum_contour()
    plot_integrated_spectrum()
    plt.show()
