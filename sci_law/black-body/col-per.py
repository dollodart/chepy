import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('ss2_10q_fine.csv'
        , header=None
        , names=['l','r','g','b'])

for c in 'r', 'g', 'b':
    bl = df[c] < -4
    print(f'range greater than 10^-4 for {c}', df['l'][bl].min(), df['l'][bl].max())
    df[c] = 10**df[c]

fig, ax = plt.subplots(nrows=1,ncols=1)

ax.plot(df['l'],df['r'],'r-',label='r')
ax.plot(df['l'],df['g'],'g-',label='g')
ax.plot(df['l'],df['b'],'b-',label='b')

#r = (740 + 625) / 2
#g = 565
#b = (466 + 436) / 2

r = 650
g = 530
b = 460

ymin, ymax = ax.get_ylim()
ax.plot([r]*2, [ymin, ymax], 'r-')
ax.plot([g]*2, [ymin, ymax], 'g-')
ax.plot([b]*2, [ymin, ymax], 'b-')
ax.legend()

plt.show()
