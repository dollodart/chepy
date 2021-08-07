from thermo import Chemical
import matplotlib.pyplot as plt

Tstd = 273.15
Pstd = 1.e5

def annotate_(text, x, y):
    for i in range(len(text)):
        plt.annotate(text[i], (x[i], y[i]))

def plot_mu_sigma_compare():
    from chemsets import eng_toolbox_data as data
    chemicals, visc, surft = zip(*data)
    visc = [float(i)/1000. for i in visc] # cP -> Pa.s
    surft = [float(i) for i in surft]

    x, y = visc, surft
    plt.loglog(x, y, 'x', label='eng toolbox')
    plt.xticks(rotation=90)
    annotate_(chemicals, x, y)

    plot_mu_sigma([Chemical(id) for id in chemicals])

    plt.xlabel('Viscosity in Pa*s')
    plt.ylabel('Surface Tension in N/m')
    plt.legend()

def plot_mu_sigma(chemicals):
    xy = []
    for chemical in chemicals:
        mu = chemical.ViscosityLiquid(Tstd, Pstd)
        sigma = chemical.SurfaceTension(Tstd)
        if mu is not None and sigma is not None:
            xy.append([chemical.name, mu, sigma])
        else:
            print(f"couldn't find mu-sigma data for {chemical.name}")

    ids, x, y = zip(*xy)
    plt.loglog(x, y, 'x')
    plt.xlabel('Viscosity in Pa*s')
    plt.ylabel('Surface tension in N/m')
    annotate_(ids, x, y)

def plot_mu_pstar(chemicals):
    xy = []
    for chemical in chemicals:
        mu = chemical.ViscosityLiquid(Tstd, Pstd)
        pstar = chemical.VaporPressure(Tstd)
        if mu is not None and pstar is not None:
            xy.append([chemical.name, mu, pstar])
        else:
            print(f"couldn't find mu-pstar data for {chemical.name}")

    ids, x, y = zip(*xy)
    plt.loglog(x, y, 'x')
    plt.xlabel('Viscosity in Pa*s')
    plt.ylabel('Vapor Pressure in Pa')
    annotate_(ids, x, y)


def plot_sigma_pstar(chemicals):
    xy = []
    for chemical in chemicals:
        sigma = chemical.SurfaceTension(Tstd)
        pstar = chemical.VaporPressure(Tstd)
        if sigma is not None and pstar is not None:
            xy.append([chemical.name, sigma, pstar])
        else:
            print(f"couldn't find sigma-pstar data for {chemical.name}")

    ids, x, y = zip(*xy)
    plt.loglog(x, y, 'x')
    plt.xlabel('Surface tension in N/m')
    plt.ylabel('Vapor Pressure in Pa')
    annotate_(ids, x, y)

def plot_mu_sigma_pstar(chemicals):
    plt.figure()
    plot_mu_sigma(chemicals)
    plt.figure()
    plot_mu_pstar(chemicals)
    plt.figure()
    plot_sigma_pstar(chemicals)

def plot_x_y(chemicals, xstr, ystr, xlabel=None, ylabel=None):
    xy = []
    for chemical in chemicals:
        try:
            x = getattr(chemical, xstr)(Tstd)
        except TypeError:
            x = getattr(chemical, xstr)(Tstd, Pstd)
        try:
            y = getattr(chemical, ystr)(Tstd)
        except TypeError:
            y = getattr(chemical, ystr)(Tstd, Pstd)
        if x is not None and y is not None:
            xy.append([chemical.name, x, y])
        else:
            print(f"couldn't find {x}-{y} data for {chemical.name}")

    ids, x, y = zip(*xy)
    plt.loglog(x, y, 'x')
    if xlabel is None:
        plt.xlabel(f'{xstr}')
    else:
        plt.xlabel(f'{xlabel}')
    if ylabel is None:
        plt.ylabel(f'{ystr}')
    else:
        plt.ylabel(f'{ylabel}')
    annotate_(ids, x, y)

if __name__ == '__main__':
    #plot_mu_sigma_compare()
    from chemsets import *
    #plot_mu_sigma_pstar([Chemical(id) for id in butanes])
    #plot_mu_sigma_pstar([Chemical(id) for id in alkanes])
    plot_x_y([Chemical(f) for f in common_chemicals],
             'VolumeLiquid',
             'SurfaceTension',
             'Number Density in mol/m^3',
             'Surface Tension in N/m')
    plt.show()
