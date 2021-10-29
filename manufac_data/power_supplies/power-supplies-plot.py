import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

x = y = np.linspace(-3, 3, 100)
xv, yv = np.meshgrid(x, y)
z = xv + yv

fig, ax = plt.subplots()
CS = ax.contour(xv, yv, z, levels=np.arange(-6, 7, 1))
ax.clabel(CS, inline=1, fontsize=10, fmt='%0.0f')

xnlim = -2.95
ynlim = -2.95
xplim = 2.95
yplim = 2.95

#x is current, y is voltage

def draw_rect(ax, xlb, ylb, xub, yub, label='no label'):
    points = [[xlb, ylb], [xub, ylb], [xub, yub], [xlb, yub], [xlb, ylb]]
    x, y = np.transpose(points)
    x, y = y, x # change to abc
    ax.plot(x, y, label=label)


# HVPS
xlb = xnlim
ylb = np.log10(0.1)
xub = np.log10(0.005)  # 5 mA maximum
yub = yplim
draw_rect(ax, xlb, ylb, xub, yub, label='HVPS')

# Mid-range power supply
xlb = np.log10(0.1)
ylb = np.log10(0.1)
xub = np.log10(40.)
yub = np.log10(36.)
draw_rect(ax, xlb, ylb, xub, yub, label='MRPS')

# Lambda small power supply
xlb = np.log10(0.01)
ylb = np.log10(0.1)
xub = np.log10(0.2)
yub = np.log10(120.)
draw_rect(ax, xlb, ylb, xub, yub, label=r'$\lambda$SPS')

# Variac (AC, RMS values)
xlb = np.log10(1.)
xub = np.log10(15.)
ylb = np.log10(1.)
yub = np.log10(120.)
draw_rect(ax, xlb, ylb, xub, yub, label='Variac')

# variable load wall power
xlb = np.log10(0.1)
xub = np.log10(10.)
ylb = np.log10(120.)
yub = np.log10(120.)
draw_rect(ax, xlb, ylb, xub, yub, label='Wall')

# high current DC power supply
xlb = np.log10(0.1)
xub = np.log10(150.)
ylb = np.log10(0.1)
yub = np.log10(7.5)
draw_rect(ax, xlb, ylb, xub, yub, label='HCPS')

# wall AC to dC rectifier-transformer
xlb = np.log10(1e-3)
xub = np.log10(300e-3)
ylb = np.log10(12)
yub = np.log10(12)
draw_rect(ax, xlb, ylb, xub, yub, 'Converter')

# ATR Mid-range power supply
xlb = np.log10(0.1)
xub = np.log10(50.)
ylb = np.log10(0.1)
yub = np.log10(10.)
draw_rect(ax, xlb, ylb, xub, yub, 'ATR MRPS')

ax.set_xlabel(r'$\log_{10} V$ / V')
ax.set_ylabel(r'$\log_{10} I$ / A')
ax.set_title(r'$\log_{10} P$ / W')

plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

plt.show()
