import matplotlib.pyplot as plt
import numpy as np

logp = np.arange(-8, 7)  # in torr
logq = np.arange(-6, 6)  # in torr*L/s
logp, logq = np.meshgrid(logp, logq)
logc = logq - logp

fig, ax = plt.subplots()
# RT=8.314*298.15
Pstd = 760.  # torr
x = logq - np.log10(Pstd)
y = logp
z = logc
CS = ax.contour(x, y, z, levels=range(-12,12,2))
ax.clabel(CS, inline=1, fontsize=10, fmt='%1.1f')
ax.set_xlabel('log10 flow rate in liters per second')
ax.set_title('log10 conductance in liters per second per torr')
ax.set_ylabel('log10 pressure difference in torr')

ax.plot([x.min(),x.max()],[np.log10(760.)]*2,'k-',label='UHV line')
# differential pumping is often used around UHV systems so this is not
# necessarily the pressure driving force always seen for a leak one can use
# high pump speed pumps (diffusion pumps can have ~2000 L/s pump speeds) for
# relatively high conductance leaks
plt.legend()

plt.figure()
logp = np.log10(760.)
logc = logq - logp
plt.plot(logq, logc, 'k-')
plt.xlabel('log10 flow rate in liters per second')
plt.ylabel('log10 conductance in liters per second per torr')
plt.title('pressure difference = 760 torr')

plt.show()
