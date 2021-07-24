"""
Includes
- JMAX file format reader.
- Function for smoothing of IR spectra.
- Function for diff'ing spectra, useful for experiments requiring a
  reference spectra subtraction.
"""

from scipy.interpolate import interp1d
from scipy import arange, array, exp
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve


def read_jmax(lines):
    lll = []
    yfactor = 1
    for line in lines:
        line = line.rstrip('\n')
        sign = 1
        l = []
        ll = []
        if line[0:2] != '##':
            if ('+' in line) or ('-' in line):
                for char in line:
                    if char == '-':
                        ll.append(float(''.join(l)) * sign * yfactor)
                        sign = -1
                        l = []
                    elif char == '+':
                        ll.append(float(''.join(l)) * sign * yfactor)
                        sign = 1
                        l = []
                    else:
                        l.append(char)
                ll.append(float(''.join(l)) * sign)
                lll.append(ll)
            else:
                line = line.split(' ')
                line = [float(val) for val in line]
                lll.append(line)
        elif 'YFACTOR' in line:
            # yfactor=float(line.split('=')[-1])
            pass
    return lll


def baseline_als(y, lam, p, niter=10):
    """The als is not for alternating least squares but instead for asymmetric
    least squares.  Generally recommended values are 0.001 <= p <= 0.1 (for
    positive peaks) and 10^2 <= lam <= 10^9, and l should be varied
    logarithmically when finding optimum parameters.  Lambda is the weight for
    the smoothness in the objective function, while p weights the negative
    residual more strongly.

    From reference: Baseline Correction with Asymmetric Least Squares Smoothing
    by Paul H. C. Eilers and Hans F.M. Boelens

    """
    L = len(y)
    D = sparse.diags([1, -2, 1], [0, -1, -2], shape=(L, L - 2))
    w = np.ones(L)
    for i in range(niter):
        W = sparse.spdiags(w, 0, L, L)
        Z = W + lam * D.dot(D.transpose())
        z = spsolve(Z, w * y)
        w = p * (y > z) + (1 - p) * (y < z)
    return z


def extrap1d(interpolator):
    """From https://stackoverflow.com/questions/2745329"""
    xs = interpolator.x
    ys = interpolator.y

    def pointwise(x):
        if x < xs[0]:
            return ys[0] + (x - xs[0]) * (ys[1] - ys[0]) / (xs[1] - xs[0])
        elif x > xs[-1]:
            return ys[-1] + (x - xs[-1]) * (ys[-1] -
                                            ys[-2]) / (xs[-1] - xs[-2])
        else:
            return interpolator(x)

    def ufunclike(xs):
        return array(list(map(pointwise, array(xs))))

    return ufunclike


def diff(refsig, specsig, ref2sig, spec2sig):
    """
    Takes the difference between two spectra, accounting for possibly different
    background references between the two.

    Arguments are the output of jmax_reader.

    specsig: negative signal file in difference
    refsig: negative signal's reference
    spec2sig: positive signal in difference
    ref2sig: positive signal's reference

    """

    l = specsig
    x, *y = zip(*l)
    x = np.array(x)
    y = np.array(y)
    y = y.mean(axis=0)  # average the spectra
    l = refsig
    xref, *yref = zip(*l)
    xref = np.array(xref)
    yref = np.array(yref)
    yref = yref.mean(axis=0)
    f = interp1d(xref, yref)
    f = extrap1d(f)
    yref = f(x)
    y = y + yref

    # time_spectrum = 108.  # seconds
    l = spec2sig
    x2, *y2 = zip(*l)
    x2 = np.array(x2)
    y2 = np.array(y2)
    y2 = y2.mean(axis=0)  # average the spectra

    l = ref2sig
    x2ref, *y2ref = zip(*l)
    x2ref = np.array(x2ref)
    y2ref = np.array(y2ref)
    y2ref = y2ref.mean(axis=0)

    f = interp1d(x2ref, y2ref)
    f = extrap1d(f)
    y2ref = f(x2)
    y2 = y2 + y2ref

    f = interp1d(x2, y2)
    f = extrap1d(f)
    y = f(x) - y

    lmbd = 1.e9
    p = 1.e-1
    y = y - baseline_als(y, lmbd, p)
    # y=y-y.min()
    if y.max() > 0:
        y = y / y.max()
    else:
        y = y / (-1 * y.max())
    return x, y
