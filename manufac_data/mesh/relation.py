import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

lines = open('mesh-sizes.csv', 'r').readlines()
lst = []
for line in lines[2:]:
    line = line.rstrip('\n')
    line = line.split(',')
    nl = []
    for l in line:
        if '/' in l:
            n, d = l.split('/')
            nl.append(float(n) / float(d))
        elif l == '':
            nl.append(-1)
        else:
            nl.append(float(l))

    lst.append(nl)

std, mshin, mshno, mshsize = np.array(lst).transpose()
in2mm = 25.4

def plot_mshsize():
    inspec = mshin[mshin > 0] * in2mm
    n = len(inspec)
    plt.semilogy(range(n), inspec, 'o', label='inch specification')
    plt.semilogy(range(n, len(mshsize)), mshsize[n:], 'o', label='integer specification')
    x = np.arange(len(mshsize))
    s, i, *params = linregress(x, np.log10(mshsize))
    plt.semilogy(x, 10**i*10**(s*x), label=f's={s:.2f} i={i:.2f} (base 10)')
    plt.xlabel('ascending index')
    plt.ylabel('mesh size in mm')
    plt.title('R^2={0:.3f} p={1:.3f} sig={2:.3f}'.format(*params) + f'\nfractional increments={10**s:.2f}')
    plt.legend()

def plot_invmshno_mshsize():
    cond = mshno > 0

    plt.plot(1/mshno[cond], mshsize[cond], 'o', label='data')
    s, i, *params = linregress(1/mshno[cond], mshsize[cond])
    plt.plot(1/mshno[cond], s/mshno[cond] + i, label=f's={s:.2f} i={i:.2f}')

    plt.title('R^2={0:.3f} p={1:.3f} sig={2:.3f}'.format(*params))
    plt.ylabel('mesh size in mm')
    plt.xlabel('inverse mesh no.')
    plt.legend()

def plot_mshno_mshsize():
    cond = mshno > 0

    plot, = plt.loglog(mshno, mshsize, 'o', label='data')
    s, i, *params = linregress(np.log(mshno[cond]), np.log(mshsize[cond]))
    plt.loglog(
        mshno[cond],
        np.exp(i) *
        mshno[cond]**s,
        label=f's={s:.2f} i={i:.2f}')

    plt.title('R^2={0:.3f} p={1:.3f} sig={2:.3f}'.format(*params))
    plt.ylabel('mesh size in mm')
    plt.xlabel('mesh no.')
    plt.legend()


def plot_mshin_mshsize():
    # correct unit conversions in data source
    plt.xlabel('mesh size in inches')
    plt.ylabel('mesh size in mm')
    cond = mshin > 0
    plt.plot(mshin[cond], mshsize[cond], 'o')
    plt.plot(mshin[cond], mshin[cond]*in2mm, 'o')

if __name__ == '__main__':
    plt.figure()
    plot_mshin_mshsize()
    plt.figure()
    plot_mshsize()
    plt.figure()
    plot_mshno_mshsize()
    plt.figure()
    plot_invmshno_mshsize()
    plt.show()
