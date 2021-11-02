import csv
import os.path as osp
from chepy.utils.string2symbols import string2symbols, symbols2numbers

data_file = osp.join(osp.dirname(__file__), 'element-atom-weights.csv')

with open(data_file, mode='r') as infile:
    mol_mass = csv.reader(infile)
    mol_mass = {k: float(v) for k, v in mol_mass}

def formula2molmass(s):
    symbols = string2symbols(s)
    return sum([mol_mass[k] for k in symbols])

# example usage
if __name__ == '__main__':
    s = 'CH2I(CH(CH3)3)'
    symbols = string2symbols(s)
    mw = sum([mol_mass[k] for k in symbols])
    symbols = sorted(symbols)
    print(s)
    print(''.join(symbols))
    print(symbols2numbers(string2symbols(s)))
    print(mw)
