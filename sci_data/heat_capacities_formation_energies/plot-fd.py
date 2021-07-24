import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('formation-energies.csv')
df['dS'] = (df['dH'] - df['dG'])/298.15

ax2 = df.plot(x='dH',y='dS',kind='scatter')
for i, txt in enumerate(df['formula']):
    ax2.annotate(txt + '(' + df['phase'].iloc[i] + ')'
            , (df['dH'].iloc[i], df['dS'].iloc[i]) )
ax2.set_xlabel('$\Delta H^\ominus(T=298K)$/(kJ/mol)')
ax2.set_ylabel('$\Delta S^\ominus(T=298K)$/(kJ/(mol*K))')
plt.show()
