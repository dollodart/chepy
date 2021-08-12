from chepy.manufac_data.heater_cartridges import df, sdf

def tables_leadlength():
    table = df.groupby('Wire Lead Length (in)').agg(['mean', 'std'])
    print(table.transpose())

    table = df.groupby('Wire Lead Length (in)').agg('mean')
    table = table.transpose()
    r = table[12] / table[16]
    print('fractional 12 / 16')
    print(r)

def tables_systematic():
    # systematic
    for col in sdf.columns:
        s = sdf.groupby(col).agg(['mean', 'std'])
        if s.shape[0] < 20:
            print('\n' + col + '\n')
            print(s.transpose())

def tables_systematic_2():
    # systematic quantitative
    tab = sdf.corr().round(2)
    c = 0
    while 3*c < len(tab.columns):
        c += 1
        print(tab[tab.columns[3*(c-1):3*c]])
    print(tab[tab.columns[3*c:]])

if __name__ == '__main__':
    #tables_leadlength()
    #tables_systematic()
    #tables_systematic_2()

    print(df['Volumetric Heat Rate (W/in^3)'].mean(),
          df['Volumetric Heat Rate (W/in^3)'].std())

    for n, gr in df.groupby('Element Diameter (in)'):
        print(n, gr['Power (W)'].corr(gr['Volume (in^3)']).round(2))
