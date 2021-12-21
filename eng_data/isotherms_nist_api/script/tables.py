import numpy as np
import pandas as pd

# utility stat functions (for agg op)
def p05(x):
    return np.quantile(x, 0.05)
def p50(x):
    return np.quantile(x, 0.50)
def p95(x):
    return np.quantile(x, 0.95)
def std_over_mean(x):
    return x.std() / x.mean()
def maxminmin(x):
    return p95(x) - p05(x)
def maxminminnorm(x):
    return maxminmin(x) / p50(x)

def table_ind_means(df):
    g = df.groupby('adsorbate')['temperature', 'pressure']
    res = g.agg([np.mean, np.std, p05, p95])
    res = res.sort_values(by=[('temperature', 'mean'), ('pressure', 'mean')])
    return res

def table_ind_ranges(df):

    for func, st in (maxminmin, 'max-min'), (maxminminnorm, '(max-min)/med'):
        g = df.groupby(['doi', 'adsorbate', 'adsorbent'])
        gg = g['pressure'].agg(func)
        print('pressure mean, max, min of', st, gg.mean(), gg.max(), gg.min(), sep='\n')
        gg = g['temperature'].agg(func)
        bl = gg > 0
        print('temperature (excluding 0) mean, max, min of', st, gg[bl].mean(), gg[bl].max(), gg[bl].min(), sep='\n')
        print('excluded', bl.sum() / len(bl), 'of datapoints')
    return None

def test_invar(df):
    df['invar'] = np.log(df['pressure']) / ( df['temperature'] * np.log(df['temperature']) )
    invars = []
    for n, gr in df.drop_duplicates(['pressure', 'temperature']).groupby(['adsorbate', 'adsorbent']):
        for q in np.linspace(0.15, 0.85, 15):
            q = gr['adsorption'].quantile(q)
            bl = ~(gr['adsorption'] > 1.05*q) & ~(gr['adsorption'] < 0.95*q)
            if bl.sum() > 2:
                invars.append((gr['temperature'].mean(), np.log(gr['pressure'].mean()), gr['invar'][bl].mean()))

    t, p, i = zip(*invars)
    ndf = pd.DataFrame(np.transpose([t, p, i]), columns=['temperature', 'log pressure', 'invar'])

    r = ndf.agg(['mean', 'std', std_over_mean])
    return r

def test_temp_ranges(df):
    gr = df.groupby(['adsorbate', 'adsorbent'])
    r = gr['temperature'].agg([p05, p50, p95, std_over_mean])
    return r.sort_values(by='p50')

if __name__ == '__main__':
    from chepy.eng_data.isotherms_nist_api import load_isotherm_data
    df = load_isotherm_data()

    ## tests
    #r = test_invar(df)

    #df['temperature'] = df['temperature'].map(lambda x: x if x > 0 else x + 273.15)
    #r = test_temp_ranges(df)
    #print(r)

    gr = df.groupby('doi')['adsorption']
    g = gr.agg([p05, p50, p95, std_over_mean, maxminmin, maxminminnorm])
    print(g.mean(axis=0), g.std(axis=0))
