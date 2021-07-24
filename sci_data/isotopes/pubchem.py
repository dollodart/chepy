from time import time
import pubchempy as pcp
elements = ['H2', 'He', 'Li', 'Be', 'B', 'C',  # carbon allotropes are many
            # phosphorous allotropes are many
            'N2', 'O2', 'F2', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P8',
            'S8',  # sulfur allotropes are many
            'Cl2', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Ch', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br2', 'Kr',
            'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I2', 'Xe',
            'Cs', 'Ba']
tab_expand = 15
print('element\tquery time\tisotope atom count\tmolecular weight'.expandtabs(tab_expand))
for element in elements:
    t0 = time()
    try:
        cs = pcp.get_compounds(element, 'formula')
        qt = time() - t0
        for c in cs:
            row = '\t{0:.0f}s\t{1:.0f}\t{2:.2f}g/mol'.format(qt, c.isotope_atom_count, c.molecular_weight)
            print(element + row.expandtabs(tab_expand))
    except IndexError:
        print(element + ' has no PubChem Entry')
