import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv('paschen-parameters.csv', delimiter=',')
pdmin = 1.  # mm*torr
pdmax = 1000.  # mm*torr
pd = np.linspace(pdmin, pdmax, 100)
for i in range(len(df)):
    B = df['b'][i]
    aprime = df['aprime'][i]
    VB = B * pd / np.log(aprime * pd)
    plt.plot(np.log10(pd), np.log10(VB))

plt.legend(df['gas'])
plt.xlabel('log10 $pd$ in mm*Torr')
plt.ylabel('log10 Breakdown voltage in V')
plt.xlim((0, None))
plt.ylim((0, None))
plt.show()
