import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def change_comp(vals, weights):
    return vals * weights / np.sum(vals * weights)

def row_op(row):
    if row['unit'] == 'g':
        return row['amount'] / row['mw']
    elif row['unit'] == 'mL':
        return row['amount'] / row['mw'] * row['rho']
    else:
        return row['amount']

def process_data(inputdata, basis, output_filename='table.csv'):
    """
    inputdata: dictionary of components with amount, unit, molecular weight
    ('mw' key), and density ('rho') key. Must be the same units for each
    species in a given dimension, and only recognize 'g' for mass and 'mL' for volume.
    basis: Dictionary of components, and the amount and unit of the basis. 

    All quantities, whether they be mass, volume, or mole, scale by the same
    factor. If a recipe to make 6 cookies asks for 100 g of flour and 1 cup of
    water, then one for 12 cookies will ask for 200 g of flour and 2 cups of
    water. This is how the moles, volumes, and masses are readily determined
    from any basis.

    """
    df = pd.DataFrame(comps)
    df = df.transpose()

    mole_fracs = df.apply(row_op, axis=1)
    mole_fracs = mole_fracs / mole_fracs.sum()
    df['mole_fracs'] = mole_fracs
    df['mass_fracs'] = change_comp(df['mole_fracs'], weights=df['mw'])
    df['vol_fracs'] = change_comp(df['mass_fracs'], weights=1./df['rho'])

    total_frac = 0
    unit = basis['unit']
    m = unit == 'g'
    v = unit == 'mL'
    i = 'mass_fracs' if m else 'vol_fracs' if v else 'mole_fracs'
    # assume a unit basis, then correct for it by the imposed basis
    for component in basis['components']:
        unit_frac = df.loc[component][i]
        total_frac += unit_frac

    a = basis['amount']
    s = a / total_frac  # scale factor
    df[['mole','mass','vol']] = df[['mole_fracs','mass_fracs','vol_fracs']]*s
    with open(output_filename, 'w') as write_file:
        dft = df.transpose()
        dft['sum'] = dft.sum(axis=1)
        write_file.write(dft.transpose().to_csv(float_format='{:.3E}'))
    return df

def plot_mole_mass_frac():
    df.sort_values(by='mole_fracs', inplace=True)
    mole_fracs, mass_fracs, vol_fracs = df['mole_fracs'], df['mass_fracs'], df['vol_fracs']
    colors = ['r', 'g', 'b']
    offset = [-0.1, 0.0, 0.1]

    elems = zip(*[mole_fracs, mass_fracs, vol_fracs])

    plt.figure()
    num_labels = len(df)
    for c, j in enumerate([mole_fracs, mass_fracs, vol_fracs]):
        for d in range(num_labels):
            #        plt.plot([d+offset[c]]*2,[0,100*j[d]],linestyle='-',linewidth=4,c=colors[c])
            plt.semilogy([d + offset[c]] * 2, [0, 100 * j[d]],
                         linestyle='-', linewidth=4, c=colors[c])

    plt.xticks(range(num_labels), labels=df.index)
    plt.title('Mole, Mass, and Volume Fractions')
    plt.xlabel('Species')
    plt.ylabel('Composition in %')
    # for many species it may be desired not to have the upper limit be unity
    plt.ylim((0.01, 110))

def plot_mole_mass_frac_2():
    colors = ['r', 'k', 'b', 'y', 'm'] # need to color cycle
    df.sort_values(by='mole_fracs', ascending=False, inplace=True)
    mole_fracs, mass_fracs, vol_fracs = df['mole_fracs'], df['mass_fracs'], df['vol_fracs']

    plt.figure()

    num_labels = len(df)
    for c, j in enumerate([mole_fracs, mass_fracs, vol_fracs]):
        val = 0
        for d in range(num_labels):
            per = 100 * j[d]
            plt.plot([c] * 2, [val, val + per], linestyle='-',
                     linewidth=4, c=colors[(num_labels - 1 - d) % 5])
            val += per

    plt.xticks([0, 1, 2], labels=['Mole', 'Mass', 'Vol.'])
    patch_lst = [matplotlib.patches.Patch(color=color) for color in colors]
    plt.legend(
        handles=patch_lst, labels=reversed(
            df.index.tolist()), bbox_to_anchor=(
                0.15, 0.35))
    plt.ylabel('Composition in %')

if __name__ == '__main__':
    # make a database of densities and molecular weights
    TPAOH_H2O_vol = 15.0  # mL
    # assume 1 g/mL since 40 weight % for molecule which is 11 times heavier
    # than water is ~ 4 mole %
    TPAOH_H2O_mass = TPAOH_H2O_vol * 1.0
    TPAOH_mass = 0.4 * TPAOH_H2O_mass
    H2O_vol = (1.0 - 0.4) * TPAOH_H2O_mass / 1.0

    comps = {  # 'Cu':{'amount':10.,'unit':'g','mw':53.546,'rho':8.96},
        # 'Te':{'amount':3.,'unit':'g','mw':127.6,'rho':6.24},
        # 'Sn':{'amount':5.,'unit':'g','mw':118.71,'rho':7.31},
        # 'S':{'amount':2.,'unit':'g','mw':32.065,'rho':2.00},
        # 'TMAAOH':{'amount':15.0*0.4,'unit':'g','mw':211.344,'rho':0.70}, #this is only sold as wt% solution
        '(CH3)2CHOH': {'amount': 0.9, 'unit': 'mL', 'mw': 60.1, 'rho': 0.786},
        'Ta(OEt)5': {'amount': 0.1, 'unit': 'mL', 'mw': 406.25, 'rho': 1.566},
        'NPr4OH': {'amount': TPAOH_mass, 'unit': 'g', 'mw': 203.36, 'rho': 1.00},
        'H2O': {'amount': 24 + H2O_vol, 'unit': 'mL', 'mw': 18.01, 'rho': 1.00},
        'Si(OEt)4': {'amount': 10, 'unit': 'mL', 'mw': 208.33, 'rho': 0.993}
    }
    # can calculate molecular weights using the mole moss module, provided the component is specified as a chemical formula
    basis = {'components': ('H2O', 'Si(OEt)4'), 'amount': 2, 'unit': 'g'}
    df = process_data(comps, basis)
    plot_mole_mass_frac_2()
    plt.show()
