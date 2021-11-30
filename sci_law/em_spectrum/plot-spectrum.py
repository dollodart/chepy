import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from chepy.sci_data.fundamental_constants import c, h, e

def setup(ax):
    # setup a plot to only have the bottom spine show
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.yaxis.set_major_locator(ticker.NullLocator())
    ax.spines['top'].set_color('none')
    ax.tick_params(which='major', width=1.00)
    ax.tick_params(which='major', length=5)
    ax.tick_params(which='minor', width=0.75)
    ax.tick_params(which='minor', length=2.5)
    ax.patch.set_alpha(0.0)


def plot_scale(ax, a, b, label):

    setup(ax)
    if a > b:
        ax.set_xlim(b, a)

        start = b // 1 + 1
        if a < 0:
            end = a // 1 + 1
        else:
            end = a // 1
        xticks = np.hstack( ([b], np.arange(start, end, 1.), [a]) )
        xticklabels = [''] + [f'{x}' for x in xticks[::-1][1:-1]] + ['']
    else:
        ax.set_xlim(a, b)

        start = a // 1 + 1
        if b < 0:
            end = b // 1 + 1
        else:
            end = b // 1
        xticks = np.hstack( ([a], np.arange(start, end, 1.), [b]) )
        xticklabels = [''] + [f'{x}' for x in xticks[1:-1]] + ['']

    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels)

    #if mnm % 1 != 0:
    #    xticks = [mnm]
    #    xticks = xticks + [mnm // 1 + i for i in range(int(mxm // 1) - int(mnm // 1))]
    #    xticks.append(mxm // 1)
    #else:
    #    xticks = [mnm + i for i in range(int(mxm) - int(mnm))]

    ax.text(0.0, 0.1, label,
            fontsize=15, transform=ax.transAxes)

divisions = [('gamma', np.nan, 1e-12),
   ('hx', 1e-12, 1e-11),
   ('sx', 1e-11, 1e-9),
   ('euv', 1e-9, 124e-9),
   ('uvc', 100e-9, 280e-9),
   ('uvb', 280e-9, 315e-9),
   ('uva', 315e-9, 400e-9),
   ('vis', 400e-9, 700e-9),
   ('nir', 700e-9, 700e-8),
   ('mir', 700e-8, 700e-7),
   ('fir', 700e-7, 700e-6),
   ('ehf', 700e-6, 1e-2),
   ('shf', 1e-2, 1e-1),
   ('uhf', 1e-1, 1e0),
   ('vhf', 1e0, 1e1),
   ('hf', 1e1, 1e2),
   ('mf', 1e2, 1e3),
   ('lf', 1e3, 1e4),
   ('vlf', 1e4, 1e5),
   ('ulf', 1e5, 1e6),
   ('slf', 1e6, 1e7),
   ('elf', 1e7, 1e8)]

if __name__ == '__main__':
    fig, axes = plt.subplots(nrows=5, ncols=1, figsize=(16, 6))

    c = np.log10(c)  # m/s
    h = np.log10(h / e) # in eV*s

    lmin = np.log10(divisions[0][2]) # base 10 orders of magnitude, SI units (meters)
    lmax = np.log10(divisions[-1][2])

    lab, lb, ub = zip(*divisions)

    # SI scales
    #setup(axes[0])
    #axes[0].set_xticks([np.log10(x) for x in ub], labels=lab, rotation=90)
    #plot_scale(axes[1], lmin, lmax, "$\lambda/m$")
    #plot_scale(axes[2], c - lmin, c - lmax, "$\omega/Hz$")
    #plot_scale(axes[3], h + c - lmin, h + c - lmax, "$E/eV$")
    #plot_scale(axes[4], -lmin, -lmax, "$1/\lambda/(m^{-1})$")

    # non-SI scales
    setup(axes[0])
    axes[0].set_xticks([np.log10(x) + 6 for x in ub], labels=lab, rotation=90)
    plot_scale(axes[1], lmin + 6, lmax + 6, "$\lambda/\mu m$")
    plot_scale(axes[2], c - lmin - 9, c - lmax - 9, "$\omega/GHz$")
    plot_scale(axes[3], h + c - lmin, h + c - lmax, "$E/eV$")
    plot_scale(axes[4], -lmin - 2, -lmax - 2, "$1/\lambda/(cm^{-1})$")

    plt.show()
