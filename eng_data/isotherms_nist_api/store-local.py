import pathlib
import json
import requests
from time import time

API_URL = 'https://adsorbents.nist.gov/isodb/api'
OUT_DIR = 'out/'

# initial isotherms (abbreviated) information query
def get_isotherms_abbreviated():
    url = f'{API_URL}/isotherms.json'
    print(f'getting abbreviated isotherms from {url}')
    isos = requests.get(url).json()
    with open(f'{OUT_DIR}/all_isos_abbreviated.json','w') as write_file:
        write_file.write(json.dumps(isos))



def get_isotherms(max_queries=1e100, overwrite=False):

    try:
        with open(f'{OUT_DIR}/all_isos_abbreviated.json', 'r') as read_file:
            isos = json.loads(read_file.read())
    except FileNotFoundError:
        raise FileNotFoundError("Run get_isotherms_abbreviated before get_isotherms")
    
    out_dir = pathlib.Path(f'{OUT_DIR}')
    cache = []
    for f in out_dir.iterdir():
        if f.name.startswith('isotherm-'):
            cache.append(f.name.lstrip('isotherm-').rstrip('.json'))

    for c, iso in enumerate(isos):
        fname = iso['filename'].lower()

        if fname in cache:
            print(f'already have data for {fname} at position {c:04d} in all_isos_abbreviated.json')
            if not overwrite:
                print('skipping this query')
                continue
            else:
                print('overwriting this data')
        else:
            print(f'no record for {fname} at position {c:04d} in all_isos_abbreviated.json')
            print(f'querying for this data')

        t0 = time()
        hkey = iso['adsorbent']['hashkey']

        name = requests.get(f'{API_URL}/material/{hkey}.json').json()
        with open(f'{OUT_DIR}/material-{hkey}.json', 'w') as write_file:
            write_file.write(json.dumps(name))

        data = requests.get(f'{API_URL}/isotherm/{fname}.json').json()

        with open(f'{OUT_DIR}/isotherm-{fname}.json', 'w') as write_file:
            write_file.write(json.dumps(data))

        print(f'collected data for {fname} at position {c:04d} in {time()-t0:.1f}s')

if __name__ == '__main__':
    #get_isotherms_abbreviated()
    get_isotherms(overwrite=False)
