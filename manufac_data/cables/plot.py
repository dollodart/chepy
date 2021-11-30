import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('data.csv')

df = df.sort_values(by='length(m)')
fig, axs = plt.subplots(nrows=3, ncols=1, sharex=True)
ax0, ax1, ax2 = axs

ax0.plot(df['type'], df['voltage_max(V)'], '-o')
ax1.plot(df['type'], df['current_max(mA)'], '-o')
ax2.plot(df['type'], df['length(m)'], '-o')

ax0.set_ylim((0, max(df['voltage_max(V)']) * 1.1))
ax1.set_ylim((0, max(df['current_max(mA)']) * 1.1))
ax2.set_ylim((0, max(df['length(m)']) * 1.1))

ax0.set_ylabel('Max Voltage (V)')
ax1.set_ylabel('Max Current (mA)')
ax2.set_ylabel('Max Length (m)')
ax2.set_xlabel('Type')

plt.show()
