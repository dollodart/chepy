import numpy as np
# all in SI

pi = np.pi
mp = proton_mass = 1.6726218e-27
me = electron_mass = 9.10938356e-31
e = electron_charge = 1.60217662e-19
h = plancks_constant = 6.6066e-34
hbar = reduced_plancks_constant = h / 2 * pi
R = gas_constant = 8.314
N = avogadros_number = 6.0221409e23
F = faradays_constant = N * e
kB = boltzmanns_constant = R / N
eps0 = vacuum_permittivity = 8.854187817e-12
k = coulombs_constant = 1 / (4 * pi * eps0)
mu0 = vacuum_permeability = 1.257e-6
c = speed_of_light = 299792458
G = gravitational_constant = 6.67408e-11
sigma = stefan_boltzmann_constant = 5.670367e-8

# unit conversion
# since I can never recall if the factors are to be multiplied or divided, these are functions 

def J2eV(x):
    return x / electron_charge

def eV2J(x):
    return x * electron_charge

def mol2num(x):
    return x * avogadros_number

def num2mol(x):
    return x / avogadros_number

def kJpermole2eV(x):
    return J2eV(x) / mole2num(1)
