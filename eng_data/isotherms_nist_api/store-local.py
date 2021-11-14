from urllib.request import urlopen
import json
import numpy as np
from time import time

parent_url = 'https://adsorbents.nist.gov/isodb/api/'

# initial isotherms (abbreviated) information query
# isos=urlopen(parent_url+'isotherms.json')
# isos=json.loads(isos.read())
# with open('out/all_isos_abbreviated.json','w') as write_file:
#    write_file.write(json.dumps(isos))


with open('out/all_isos_abbreviated.json', 'r') as read_file:
    isos = json.loads(read_file.read())

ci = 500  # update to prevent overwriting
for d, iso in enumerate(isos[ci:]):
    c = ci + d
    t0 = time()
    hkey = iso['adsorbent']['hashkey']
    fname = iso['filename']

    name = urlopen(parent_url + 'material/' + hkey + '.json')
    name = json.loads(name.read())
    with open('out/{0:04d}-name-query'.format(c), 'w') as write_file:
        write_file.write(json.dumps(name))

    data = urlopen(parent_url + 'isotherm/' + fname + '.json')
    data = json.loads(data.read())

    with open('out/{0:04d}-data'.format(c), 'w') as write_file:
        write_file.write(json.dumps(data))

    print('{0:04d} {1:.1f}'.format(c, time() - t0))
