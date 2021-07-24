import matplotlib.pyplot as plt
import pandas as pd
lines = open('./ir-active-modes.csv', 'r').readlines()

line0 = ''
tb = []
for line in lines:
    line = line.rstrip('\n')
    line = line.split('|')
    if '-' in line[0]:
        lb, ub = line[0].split('-')
        lb, ub = float(lb), float(ub)
    elif '±' in line[0]:
        val, unc = line[0].replace('(', '').replace(')', '').split('±')
        lb, ub = float(val) - float(unc), float(val) + float(unc)
    if line[1] == '\xa0':
        line[1:3] = line0[1:3]
    if ' ' in line[1]:
        f = line[1].split(' ')
        tb.append([lb, ub] + f + [line[2]])
    else:
        tb.append([lb, ub, line[1], line[2]])
    line0 = line

tb = sorted(tb, key=lambda x: x[0])

df = pd.DataFrame(
    tb,
    columns=[
        'max wavenumber',
        'min wavenumber',
        'atom pair',
        'mode',
        'functional group'])


# peak_center=2900.
def plot_ref(peak_center, ax, offset=1):
    o = 0
    for row in tb:
        l = peak_center - row[0]
        u = peak_center - row[1]
        if l < 0 < u:
            ax.plot([row[0], row[1]], [o * offset] *
                    2, '|-', label=' '.join(row[2:]))
            o += 1
    return ax
