from chepy.eng_data.isotherms_nist_api import load_isotherm_data, fit_freundlichs, fit_langmuirs

df = load_isotherm_data()

## this gives the exponents as the 'constants' (empirical model has two parameters, coefficient and exponent)
ndf = fit_freundlichs(df)
Kdf = fit_langmuirs(df)

print(ndf.dropna().sort_values(by='n'))
print(Kdf.dropna().sort_values(by='K'))

ngr = ndf.groupby(['temperature', 'adsorbent', 'adsorbate'])['n']
Kgr = Kdf.groupby(['temperature', 'adsorbent', 'adsorbate'])['K']

nr = ngr.agg(['mean', 'std']).dropna()
Kr = Kgr.agg(['mean', 'std']).dropna()

nr['std/mean'] = nr['std'] / nr['mean']
Kr['std/mean'] = Kr['std'] / Kr['mean']

print('freundlich')
print(nr.sort_values(by='std/mean'))
print('langmuir')
print(Kr.sort_values(by='std/mean'))
