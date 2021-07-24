from spectrum import *


def plot_all_modes():
    """Plot all the modes for a given bond type"""
    for p in (('C=O', (1900, 1500)),
              ('C-H', (4000, 500)),
              ('O-H', (4000, 500))):
        plt.figure(p[0])
        plt.xlim(p[1])
        sb = df[df['atom pair'] == p[0]]
        for c in range(len(sb)):
            x1 = sb['min wavenumber'].iloc[c]
            x2 = sb['max wavenumber'].iloc[c]
            z = sb['functional group'].iloc[c]
            plt.plot([x1, x2], [c] * 2, '|-', label=z)
        plt.yticks([])
        plt.xlabel(r'$1/\lambda$ in cm$^{-1}$')
        plt.title(p[0])
        plt.legend()


def plot_stretching_bending():
    """Plot stretching and bending modes for all bonds for comparison."""
    fig, axs = plt.subplots(nrows=2, ncols=1)
    for i, ax in (('stretching', axs[0]), ('bending', axs[1])):
        ax.set_xlim((4000, 500))
        sb = df[df['mode'] == i]
        for c in range(len(sb)):
            x1 = sb['min wavenumber'].iloc[c]
            x2 = sb['max wavenumber'].iloc[c]
            z = sb['functional group'].iloc[c]
            ax.plot([x1, x2], [c] * 2, '|-', label=z)
        ax.set_yticks([])
        ax.set_xlabel(r'$1/\lambda$ in cm$^{-1}$')
        ax.set_title(i)

# below pandas methods prove more useful than just matching one field

def plot_CH_bending():
    """Find two fields, carbon hydrogen bonds which are bending."""
    plt.figure()
    plt.xlim((4000, 500))

    a = df['atom pair'] == 'C-H'
    b = df['mode'] == 'bending'
    sb = df[a & b]
    for c in range(len(sb)):
        x1 = sb['min wavenumber'].iloc[c]
        x2 = sb['max wavenumber'].iloc[c]
        z = sb[['atom pair', 'mode', 'functional group']].iloc[c]
        plt.plot([x1, x2], [c] * 2, '|-', label=z)
    plt.yticks([])
    plt.xlabel(r'$1/\lambda$ in cm$^{-1}$')
    plt.title('Bending Modes')
    plt.legend()


def plot_CO_by_bond_order():
    """Classify the types of C-O pair bond modes by bond order."""
    plt.figure()
    plt.xlim((4000, 500))
    sb = df[df['atom pair'].apply(
        lambda x: True if ('C' in x and 'O' in x) else False)]
    g = sb.groupby('atom pair')

    import numpy as np
    from matplotlib import cm
    from math import floor, ceil
    colors = cm.get_cmap('viridis')(np.linspace(0, 1, len(g)))

    counter = 0
    diff = False
    for n, gr in g:
        if counter == 0:
            n0 = n
        if n != n0:
            diff = True
        for c in range(len(gr)):
            if diff:
                plt.plot([gr['min wavenumber'].iloc[c], gr['max wavenumber'].iloc[c]], [
                         c] * 2, '|-', label=n, color=colors[counter])
                diff = False
            else:
                plt.plot([gr['min wavenumber'].iloc[c], gr['max wavenumber'].iloc[c]], [
                         c] * 2, '|-', color=colors[counter])
        counter += 1

    plt.xlabel(r'$1/\lambda$ in cm$^{-1}$')
    plt.legend()


def plot_modes_by_H():
    """Show the classically expected result that atom pairs with hydrogens will
    have significantly greater inverse wavelengths (significantly smaller
    wavelengths, significantly greater frequencies) when the atom is
    lighter. Bonds with hydrogen are having a factor of 2 greater."""

    plt.figure()
    plt.xlim((4000, 500))
    df['hasH'] = df['atom pair'].apply(lambda x: True if 'H' in x else False)
    df1 = df[df['hasH']]
    df2 = df[~df['hasH']]
    avg1 = (df1[['min wavenumber', 'max wavenumber']]).mean(axis=0).sum() / 2.
    avg2 = (df2[['min wavenumber', 'max wavenumber']]).mean(axis=0).sum() / 2.
    plt.plot([avg1] * 2, [0, 10], 'k', label='H')
    plt.plot([avg2] * 2, [0, 10], 'b', label='~H')

    for c in range(len(df1)):
        plt.plot([df1['min wavenumber'].iloc[c],
                  df1['max wavenumber'].iloc[c]], [c] * 2, 'k|-')
    for c in range(len(df2)):
        plt.plot([df2['min wavenumber'].iloc[c],
                  df2['max wavenumber'].iloc[c]], [c] * 2, 'b|-')
    plt.xlabel(r'$1/\lambda$ in cm$^{-1}$')
    plt.legend()
    return df.groupby('hasH').agg('mean')

if __name__ == '__main__':
    r = plot_modes_by_H()
    print(r)
    plt.show()
