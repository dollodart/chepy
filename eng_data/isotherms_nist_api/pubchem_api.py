from urllib.request import urlopen
import json
import pickle
import urlpath

API_URL = urlpath.URL('https://pubchem.ncbi.nlm.nih.gov')
API_URL = API_URL / 'rest' / 'pug' / 'compound' / 'inchikey'

with open('global_dct.json', 'r') as _:
    global_dct = json.load(_)
    
def mw_req(inchi):
    try:
        return global_dct[inchi]
    except KeyError:
        url = API_URL / inchi / 'property' / 'MolecularWeight' / 'JSON'
        print(f'running query on {inchi}')
        record = url.get().json()
        val = float(record['PropertyTable']['Properties'][0]['MolecularWeight']) 
        global_dct[inchi] = val
        with open('global_dct.json', 'w') as _:
            json.dump(global_dct, _) #

    return global_dct[inchi]

if __name__ == '__main__':
    mw = mw_req('YNQLUTRBYVCPMQ-UHFFFAOYSA-N')
    print(mw)
