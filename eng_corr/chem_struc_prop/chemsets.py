# from engineering toolbox
eng_toolbox_data = """visc (cP)	surf tension (N/m)
acetic acid	1.155	0.028
acetone	0.316	0.024
benzene	0.601	0.0289
carbon disulfide	0.36	0.032
chloroform	0.53	0.0271
hexane	0.297	0.018
toluene	0.55	0.0284
ether	0.223	0.018
mercury	1.53	0.425
ethylene glycol	16.2	0.0477
carbon tetrachloride	0.91	0.027
water	0.89	0.0729"""

eng_toolbox_data = [i.split('\t') for i in eng_toolbox_data.split('\n')[1:]]

eng_toolbox_chemicals = [i[0] for i in eng_toolbox_data]

common_chemicals = ['anisole',
'water',
'ethylene glycol',
'glycerine',
'ethanol',
'isopropyl alcohol',
'octane',
'nonane',
'decane',
'acetaldehyde',
'acetone',
'aniline',
'benzene',
'toluene',
'sulfuric acid',
'mercury',
'oleic acid',
'steric acid',
#'olelyamine',
'dimethyl sulfoxide',
'tetrahydro furan'] # variety of common chemicals

# homolog series of alkanes
alkanes = ['hexane',
    'heptane',
    'octane',
    'nonane',
    'decane',
    'undecane',
    'dodecane',
    'tridecane',
    'tetradecane',
    'pentadecane',
    'hexadecane',
    'heptadecane',
    'octadecane',
    'nonadecane',
    'icosane']

butanes = ['isobutane', 'cyclobutane', 'butane']

# homolog series of alcohols
alcohols =['methanol',
             'ethanol',
             'propanol',
             'butanol',
             'pentanol',
             'hexanol',
             'heptanol',
             'octanol',
             'nonanol',
             'decanol',
             'undecanol',
             'dodecanol']

butanols = ['isobutanol',
        'tert-butanol',
        'butanol']
# limited data through thermopy

# homolog series of alkanals
alkanals= [
    'ethanal',
    'propanal',
    'butanal',
    'pentanal',
    'hexanal',
    'heptanal',
    'octanal']
