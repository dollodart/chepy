import pathlib
import urlpath

CACHE_DIR = pathlib.Path(__file__).parent.joinpath('out')
GLOBAL_DCT_FILE = CACHE_DIR.joinpath('global_dct.json')
ISODB_URL = urlpath.URL('https://adsorbents.nist.gov/isodb/api')

PUBCHEM_URL = urlpath.URL('https://pubchem.ncbi.nlm.nih.gov')
PUBCHEM_URL = PUBCHEM_URL / 'rest' / 'pug' / 'compound' / 'inchikey'
