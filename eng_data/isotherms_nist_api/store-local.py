import json
from urllib.request import urlopen
from time import time

API_URL = 'https://adsorbents.nist.gov/isodb/api'
OUT_DIR = 'out/'

# initial isotherms (abbreviated) information query
def get_isotherms_abbreviated():
    isos = urlopen(f'{API_URL}/isotherms.json')
    isos = json.loads(isos.read())
    with open(f'{OUT_DIR}/all_isos_abbreviated.json','w') as write_file:
        write_file.write(json.dumps(isos))


def get_isotherms(start=0, overwrite=False):
    with open(f'{OUT_DIR}/all_isos_abbreviated.json', 'r') as read_file:
        isos = json.loads(read_file.read())
    except FileNotFoundError:
        raise FileNotFoundError("Run get_isotherms_abbreviated before get_isotherms")

    for d, iso in enumerate(isos[start:]):
        try:
            with open(f'{OUT_DIR}/{c:04d}-data', 'r') as _:
                print(f'already have data for {c:04d}')
                if not overwrite:
                    print('skipping this query')
                    continue
                else:
                    print('overwriting this data')
        except FileNotFoundError:
            pass
        c = start + d
        t0 = time()
        hkey = iso['adsorbent']['hashkey']
        fname = iso['filename']

        name = urlopen(f'{API_URL}/material/{hkey}.json')
        name = json.loads(name.read())
        with open('{OUT_DIR}/{0:04d}-name-query'.format(c), 'w') as write_file:
            write_file.write(json.dumps(name))

        data = urlopen(f'{API_URL}/isotherm/{fname}.json')
        data = json.loads(data.read())

        with open(f'{OUT_DIR}/{c:04d}-data', 'w') as write_file:
            write_file.write(json.dumps(data))

        print(f'collected data for {c:04d} in {time()-t0:.1f}s')

if __name__ == '__main__':
    get_isotherms_abbreviated()
    get_isotherms(start=500)
