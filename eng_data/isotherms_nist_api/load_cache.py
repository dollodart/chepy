from chepy.utils.mol_mass import formula2molmass
from .env import CACHE_DIR, GLOBAL_DCT_FILE
from .pubchem_api import mw_req, global_dct
import json
import numpy as np
import pandas as pd

def tdata2df(tdata):
    #
    cols = ['doi',
            'adsUnit', 'pressUnit',
            'adsorbate', 'adsorbate mw',
            'adsorbent', 'adsorbent mw',
            'temperature', 'pressure',
            'adsorption']
    #
    dtypes = {'temperature':'float64',
              'pressure': 'float64', 'pressUnit': str,
              'adsorption': 'float64',
              'adsUnit': str,
              'doi': str,
              'adsorbate': str,
              'adsorbate mw': 'float64',
              'adsorbent': str,
              'adsorbent mw': 'float64'}
    #
    df = pd.DataFrame(tdata, columns=cols)
    for col in dtypes:
        df[col] = df[col].astype(dtypes[col])
    #
    return df

def global_dct_save():
    with open(GLOBAL_DCT_FILE, 'w') as _:
        json.dump(global_dct, _) #

def load_isotherm_data():
    tdata = []
    for f in CACHE_DIR.iterdir():
        if not f.name.startswith('isotherm'):
            continue
        with open(f, 'r') as read_file:
            data = json.loads(read_file.read())
            # print(data['adsorptionUnits'], data['pressureUnits']) # all temperatures in K
            # one must know the material properties (can be looked up by InChi Key) to convert adsorptionUnits
        try:
            doi = data['DOI']
            adsUnit = data['adsorptionUnits']
            pressUnit = data['pressureUnits']
            if len(data['adsorbates']) > 1:
                print('multi component adsorption') # this never happens
                continue
            adsorbate = ''.join(x['name'] for x in data['adsorbates'])
            adsorbate_inchi = ''.join(x['InChIKey'] for x in data['adsorbates'])

            try:
                adsorbate_mw = mw_req(adsorbate_inchi) # looks up, online or in cache, the molecular weights
            except KeyError:
                try:
                    adsorbate_mw = formula2molmass(adsorbate)
                except (KeyError, ValueError) as e:
                    adsorbate_mw = np.nan

            adsorbent = data['adsorbent']['name']

            try:
                adsorbent_mw = formula2molmass(adsorbent)
            except (KeyError, ValueError) as e:
                adsorbent_mw = np.nan

            temperature = data['temperature']
            data = data['isotherm_data']

            for d in data:
                tdata.append([doi,
                    adsUnit, pressUnit,
                    adsorbate, adsorbate_mw,
                    adsorbent, adsorbent_mw,
                    temperature, d['pressure'],
                    d['total_adsorption']])

        except KeyboardInterrupt:
            import sys; sys.exit()
        except Exception as e:
            print(e)

    global_dct_save()

    return tdata2df(tdata)
