import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

df = pd.read_csv('NPT-national-pipe-thread.csv')
df = df.dropna() # some sizes don't have certain dimensions, drop them
cols = ['pipe size (in)', 
        'tpi', 
        'length of threads (in)', 
        'total thread makeup (in)',
        'tap drill (in)'] # fractional specified

def eval_arit(iput):
    if type(iput) == str:
        # proper fraction specification as 
        # whole_number[DELIM]proper_fraction where [DELIM] = -, _
        iput = iput.replace('-', '+') 
        iput = iput.replace(' ', '+') 
        return eval(iput)
    return str(iput)
    
    return ev

for col in cols:
    df[col] = df[col].map(eval_arit)

# the arc length of a coil is not simply the number of circles it makes
# this is a kind of nominal arc length of a coil
df['thread arc length per inch (in/in)'] = df['nominal OD (in)'] * np.pi * df['tpi']
df['thread arc length (in)'] = df['thread arc length per inch (in/in)'] * df['length of threads (in)']
df['helix arc length (in)'] = df['length of threads (in)'] * np.pi * np.sqrt( (df['nominal OD (in)']*df['tpi'])**2 + 1)

def check_geo():
    df['tpi'].drop_duplicates()
    y = df['tpi'].drop_duplicates()
    y = y.values # -> numpy array
    print(' '.join(f'{x:.1f}' for x in y)) 
    y = y[:-1] / y[1:]
    print('    ', ' '.join(f'{x:.2f}' for x in y))
    print(f'mean = {y.mean():.2f}')
    print(f'std = {y.std():.2f}')

def check_ntbytpi_lt():
    x = df['number of threads']/df['tpi']
    y = df['length of threads (in)']
    plt.xlabel('Number of Threads / Threads per Inch')
    plt.ylabel('Length of threads in in.')
    plt.plot(x, y, 'o')
    plt.plot((x.min(), x.max()), (x.min(), x.max()), 'k-')

def plot_od_pipesize():
    xstr = 'pipe size (in)'
    ystr = 'nominal OD (in)'
    xmax = df[xstr].max()
    ymax = df[ystr].max()
    plt.xlim((0,xmax))
    plt.ylim((0,ymax))

    for n, gr in df.groupby('tpi'):
        plot, = plt.plot(gr[xstr], gr[ystr], 'o', label='data')

    m = max(xmax, ymax)
    plt.plot([0,m],[0,m],'k-', label='equality line')

    x, y = df[xstr].values, df[ystr].values
    slope, inter, *_ = linregress(x, y)

    plt.plot(x, slope*x + inter, 'k-', label='best fit')

    for i in range(len(y) - 1):
        actual_pipe_size = x[i]
        measured_od = taken_pipe_size = y[i]
        resulting_od = taken_pipe_size*slope + inter

        plt.plot([actual_pipe_size, taken_pipe_size, taken_pipe_size], 
                [measured_od, measured_od, resulting_od], 'k->')

    plt.xlabel(xstr)
    plt.ylabel(ystr)

    plt.title(f'slope={slope:.2f} inter={inter:.2f}')

def plot_tpi_pipesize():
    plt.xlabel('pipe size in in.')
    plt.ylabel('thread per inch')
    plt.semilogy(df['pipe size (in)'], df['tpi'])

def plot_tot_lt():
    x = df['total thread makeup (in)']
    y = df['length of threads (in)']
    plt.xlabel('Total Thread in in.')
    plt.ylabel('Length of threads in in.')
    plot, = plt.plot(x, y, 'o', label='data')

    s, i, *_ = linregress(x, y)
    plt.plot(x, s*x + i, '-', color=plot.get_color(), label='best fit')
    plt.plot([0, x.max()], [0, np.sqrt(2)*x.max()], 'k-', label='$\sqrt{2}$ line')

    plt.title(f'slope={s:.3f}={s/np.sqrt(2):.3f}' + '$\\sqrt{2}$, ' + f'inter={i:.3f}')
    plt.xlim(0, None)
    plt.ylim(0, None)

    plt.legend()

def plot_tap_od():
    plt.xlabel('nominal OD in in.')
    plt.ylabel('tap drill size in in.')
    x = df['nominal OD (in)']
    y = df['tap drill (in)']
    plot, = plt.plot(x, y, 'o-')
    m = max(x.max(), y.max())
    plt.plot([0,m],[0, m], 'k-')

def plot_tap_od_diff():
    x = df['nominal OD (in)']
    y = df['tap drill (in)']
    plt.plot(x, x - y, 'o') 
    plt.xlabel('nominal OD in in.')
    plt.ylabel('OD - tap in in.')
    plt.title('nominal thread height')

def plot_nt_pipesize():
    plt.plot(df['pipe size (in)'], df['length of threads (in)']*df['tpi'])
    plt.ylabel('Number of Threads')
    plt.xlabel('Pipe Size')

def plot_lt_od():
    x = df['nominal OD (in)']
    y = df['length of threads (in)']
    plt.plot(x, y, 'o-')
    plt.xlabel('Nominal OD in in.')
    plt.ylabel('Length of threads in in.')
    plt.xlim((0, None))
    plt.ylim((0, None))
    slope, inter, *_ = linregress(x, y)
    plt.plot(x, x*slope + inter, '-')
    plt.title(f'slope={slope:.2f}, inter={inter:.2f}')

def plot_arclength_pipesize():
    plt.plot(df['pipe size (in)'], df['thread arc length (in)'] / 12., 'o-')
    plt.xlabel('Pipe Size in in.')
    plt.ylabel('Nominal Thread Arc Length in ft')

def plot_arcerr_pipesize():
    err = (df['thread arc length (in)'] - df['helix arc length (in)'])/df['helix arc length (in)']
    plt.plot(df['pipe size (in)'], err)
    plt.xlabel('Pipe Size in in.')
    plt.ylabel('Error in Nominal Approximation')

if __name__ == '__main__':
    check_geo()

    #plt.figure()
    #check_ntbytpi_lt()

    #plt.figure()
    #plot_tot_lt()

    #plt.figure()
    #plot_od_pipesize()

    #plt.figure()
    #plot_tpi_pipesize()

    #plt.figure()
    #plot_tap_od()

    #plt.figure()
    #plot_tap_od_diff()

    #plt.figure()
    #plot_lt_od()

    #plt.figure()
    #plot_nt_pipesize()

    #plt.figure()
    #plot_arclength_pipesize()

    plt.figure()
    plot_arcerr_pipesize()

    plt.show()
