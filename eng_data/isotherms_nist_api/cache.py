from .env import CACHE_DIR, ISODB_URL
from time import time
import json
import pathlib
import urlpath
import requests

# initial isotherms (abbreviated) information query
def get_isotherms_abbreviated():
    url = ISODB_URL.joinpath('isotherms.json')
    print(f'getting abbreviated isotherms from {url}')
    isos = url.get().json()
    with open(CACHE_DIR.joinpath('all_isos_abbreviated.json'), 'w') as write_file:
        write_file.write(json.dumps(isos))


def get_isotherms(max_queries=1e100, overwrite=False):

    try:
        with open(CACHE_DIR.joinpath('all_isos_abbreviated.json'), 'r') as read_file:
            isos = json.loads(read_file.read())
    except FileNotFoundError:
        raise FileNotFoundError("Run get_isotherms_abbreviated before get_isotherms")
    
    cache = []
    for f in CACHE_DIR.iterdir():
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

        name = ISODB_URL.joinpath('material').joinpath(f'{hkey}.json').get().json()

        with open(CACHE_DIR.joinpath(f'material-{hkey}.json'.lower()), 'w') as wf:
            wf.write(json.dumps(name))

        data = ISODB_URL.joinpath('isotherm').joinpath(f'{fname}.json').get().json()

        with open(CACHE_DIR.joinpath('isotherm-{fname}.json'.lower()), 'w') as wf:
            wf.write(json.dumps(data))

        print(f'collected data for {fname} at position {c:04d} in {time()-t0:.1f}s')
