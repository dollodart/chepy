import matplotlib.pyplot as plt
import pandas as pd
import csv
from operator import itemgetter
from scipy.stats import linregress
import numpy as np

df = pd.read_csv('element-data.csv')
numeric_cols = [
"electronegativity",
"atomicRadius",
#"ionRadius", # contains ion charge, not a float
"vanDelWaalsRadius",
"ionizationEnergy",
"electronAffinity",
"meltingPoint",
"boilingPoint",
"density"]

def gen_sorts():
    params = []
    for ncol in numeric_cols:
        xy = df[['atomicNumber',ncol]]
        xy = xy.sort_values(by=ncol)
        bl = xy[ncol].isna()
        y_com = xy[ncol][~bl].tolist()
        slope, intercept, r_value, p_value, std_err = linregress(
            range(len(y_com)), y_com)
        params.append([ncol, slope, intercept, r_value, p_value, std_err])

    params = pd.DataFrame(
        params,
        columns=[
            'var',
            'slope',
            'intercept',
            'r_value',
            'p_value',
            'std_err'])
    params.sort_values(by='p_value').to_csv('sorts.csv', sep=' ', float_format='%.2E',index=False)
    return params

def gen_corrs():
    params = []
    for i in range(len(numeric_cols)):
        for j in range(i):
            x = df[numeric_cols[i]]
            y = df[numeric_cols[j]]
            bl = ~(x.isna() | y.isna())
            x_com = x[bl].tolist()
            y_com = y[bl].tolist()
            slope, intercept, r_value, p_value, std_err = linregress(
                x_com, y_com)
            params.append([numeric_cols[i], numeric_cols[j], slope,
                        intercept, r_value, p_value, std_err])
    params = pd.DataFrame(
        params,
        columns=[
            'var1',
            'var2',
            'slope',
            'intercept',
            'r_value',
            'p_value',
            'std_err'])
    params.sort_values(by='p_value').to_csv('correlations.csv', sep=' ', float_format='%.2E',index=False)
    return params

if __name__ == '__main__':
    gen_sorts()
    gen_corrs()
