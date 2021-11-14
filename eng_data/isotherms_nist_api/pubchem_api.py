from urllib.request import urlopen
import json
import pickle

with open('global_dct.json', 'r') as _:
    global_dct = json.load(_)
    
def mw_req(inchi):
    try:
        return global_dct[inchi]
    except KeyError:
        url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/{inchi}/property/MolecularWeight/JSON'
        query = urlopen(url)
        qread = query.read()
        record = json.loads(qread)
        val = float(record['PropertyTable']['Properties'][0]['MolecularWeight']) 
        global_dct[inchi] = val
        with open('global_dct.json', 'w') as _:
            json.dump(global_dct, _) #

    return global_dct[inchi]

if __name__ == '__main__':
    mw = mw_req('YNQLUTRBYVCPMQ-UHFFFAOYSA-N')
    print(mw)
