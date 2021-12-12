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
        c = tuple(len(x) for x in inchi.split('-')) == (14, 10, 1)
        if not c:
            raise KeyError
        url = API_URL / inchi / 'property' / 'MolecularWeight' / 'JSON'

    print(f'running query on {inchi}')
    record = url.get().json()
    try:
        val = float(record['PropertyTable']['Properties'][0]['MolecularWeight']) 
        global_dct[inchi] = val
    except KeyError:
        global_dct[inchi] = None

    return global_dct[inchi]

if __name__ == '__main__':
    #mw = mw_req('YNQLUTRBYVCPMQ-UHFFFAOYSA-N')
    mw = mw_req('STZCRXQWRGQSJD-GEEYTBSJSA-M')
    print(mw)
