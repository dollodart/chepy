import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar

df = pd.read_csv('mvp-dat.csv', 
        delimiter=',', 
        skiprows=[1],
        index_col=0)
df['T(melt)'] = df['T(melt)'].astype('float64')
df_solid = df[df['state'] == 'solid']
df_liquid = df[df['state'] == 'liquid']

def log10p(T, A, B, C, D):
    return A + B / T + C * np.log10(T) + D / T**3


def log10pobj_lb(T, A, B, C, D):
    return abs(np.log10(1.e-15) - log10p(T, A, B, C, D))


def log10pobj_ub(T, A, B, C, D):
    return abs(np.log10(1.e-3) - log10p(T, A, B, C, D))


def solve_press_bounds(coeffs):
    lb = minimize_scalar(
        log10pobj_lb, args=coeffs, bounds=(
            0., 3500.), method='bounded')
    ub = minimize_scalar(
        log10pobj_ub, args=coeffs, bounds=(
            0., 3500.), method='bounded')
    return lb, ub

def plot_vapor_pressures(lst_species, relative = False):
    for i in lst_species:
        element = df_solid.loc[i]
        coeffs = tuple(element[1:5])
        Tm = df_solid.loc[i]['T(melt)']
        lb_soln, ub_soln = solve_press_bounds(coeffs)
        if Tm < ub_soln.x and ub_soln.success and lb_soln.success: #prevents unconverged solutions
            T = np.arange(lb_soln.x, ub_soln.x, 1.)
            log10ps = log10p(
                T,
                coeffs[0],
                coeffs[1],
                coeffs[2],
                coeffs[3]) + np.log10(760.)
            log10pm = log10p(Tm, coeffs[0], coeffs[1], coeffs[2], coeffs[3]) + np.log10(760.)
            if relative:
                plt.plot(T/Tm,log10ps - log10pm) # else use liquid correlation
            else:
                plt.plot(T, log10ps)

    if relative:
        plt.xlabel('$T/T_m$')
        plt.ylabel('$\log_{10} p/p_m$')
    else:
        plt.xlabel('$T/K$')
        plt.ylabel('$\log_{10} p/torr$')
    plt.legend(lst_species)
    plt.show()

if __name__ == '__main__':
    lst_species = ['Fe', 'Cu']
    #lst_species = df_solid.index
    plot_vapor_pressures(lst_species)
