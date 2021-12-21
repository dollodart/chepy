from chepy.eng_data.isotherms_nist_api import load_isotherm_data, fit_freundlichs, fit_langmuirs, fit_vanthoft
import pandas as pd

df = load_isotherm_data()

def std_over_mean(ndf, Kdf):
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

def vanthoft(Kdf):
    acc = []
    for n, gr in Kdf.groupby(['adsorbent', 'adsorbate']):
        gr = gr.dropna()
        if len(gr) <= 3 or (gr['K'] < 0).any() or (gr['temperature'] < 0).any():
            continue
        delH_kB, delS_kB = fit_vanthoft(gr['temperature'], gr['K'],
                 delH_kB0 = -1000, delS_kB0 = -25)
        acc.append( (n[0], n[1], delH_kB, delS_kB) )
    return pd.DataFrame(acc, columns=['adsorbent', 'adsorbate', 'delH_kB', 'delS_kB'])

if __name__ == '__main__':

    ## this gives the exponents as the 'constants' (empirical model has two parameters, coefficient and exponent)
    ndf = fit_freundlichs(df)
    Kdf = fit_langmuirs(df)

    print(ndf.dropna().sort_values(by='n'))
    print(Kdf.dropna().sort_values(by='K'))

    df = vanthoft(Kdf)
    print(df)
