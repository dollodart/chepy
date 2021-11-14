import json
import numpy as np
import pandas as pd
from pubchem_api import mw_req
from chepy.utils.mol_mass import formula2molmass

def read_isotherm_data():
    tdata = []
    for c in range(300):
        with open(f'out/{c:04d}-data', 'r') as read_file:
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
            raise
        except Exception as e:
            #print('exception b4')
            #print(c, e)
            raise e
    #
    cols = ['doi',
            'adsUnit', 'pressUnit',
            'adsorbate', 'adsorbate mw',
            'adsorbent', 'adsorbent mw',
            'temperature', 'pressure',
            'adsorption']
    #
    dtypes = {'temperature':'float64',
              'pressure': 'float64',
              'pressUnit': str,
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

if __name__ == '__main__':
    df = read_isotherm_data()
    bl = df['adsUnit'] == 'wt%'
    sdf = df[bl]
    s = sdf['adsorption'] 
    print(s.mean(), s.std(), s.quantile(0.95))
    bl = s > s.quantile(0.95)
    print(sdf[bl].drop_duplicates())
    print(df[df['adsorbent mw'].isna()]['adsorbent'].drop_duplicates())
