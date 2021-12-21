from chepy.eng_data.isotherms_nist_api import load_isotherm_data

df = load_isotherm_data()
bl = df['adsUnit'] == 'wt%'
sdf = df[bl]
s = sdf['adsorption'] 
print('adsorption statistics on wt% data')
print(f'mean={s.mean():.2f}, std={s.std():.2f}, 95%={s.quantile(0.95):.2f}')
bl = s > s.quantile(0.95)
print('high adsorption data frame')
print(sdf[bl].drop_duplicates())
bl = df['adsorbent mw'].isna() 
print('number of entries for which adsorbent mw was found', len(bl) - bl.sum(), 'out of', len(bl))
print('adsorbents for which no adsorbent mw was found')
print(df[bl]['adsorbent'].drop_duplicates())
print('different types of units')
print(df['adsUnit'].drop_duplicates())
