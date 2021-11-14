"""Illustrations of the change of spectra on changing the hue, saturation, and
lightness of a color, these being defined here as shift, baseline, and scale
changes. Note the way I define baseline excludes the peaks of the spectrum,
hence a baseline change decreases the peak prominence (some people consider a
baseline change to be a y-shift)."""

import numpy as np
import matplotlib.pyplot as plt

l = np.arange(400, 750)
y = np.exp(-(l - 550)**2/10**2)
n = len(y)

plt.figure()
plt.title('x-shift (hue change)')
plt.plot(l, y, 'k-')
plt.plot(l, np.roll(y, 50), 'k--')

plt.figure()
plt.title('baseline shift (saturation/lightness change)')
plt.plot(l, y, 'k-')
o = y > 0.1
bls = (np.ones(n) - o) / 20
plt.plot(l, y + bls, 'k--')

plt.figure()
plt.title('baseline shift + chromatic attenuation (saturation change w/o lightness change)')
plt.plot(l, y, 'k-')
y2 = 0.25*np.exp(-(l - 550)**2/20**2)
o = y2 > 0.1
bls = (np.ones(n) - o) / 20
plt.plot(l, y2 + bls, 'k--')
# this is qualitatively showing a conservation of area, but note that the net
# intensity is not the brightness/lightness because only the convolution with
# the cones determines the brightness/lightness.  given the data, this can be
# quantitatively modeled, that is, one can determine spectral changes which
# would correspond to constant brightness and lightness.

plt.figure()
plt.title('y-scale (physical, uniform intensity change)')
plt.plot(l, y, 'k-')
plt.plot(l, y*2, 'k--')

plt.show()
