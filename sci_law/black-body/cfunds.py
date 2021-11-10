import numpy as np
import matplotlib.pyplot as plt

with open('ss2_10q_fine.csv', 'r') as _:
    arr = np.genfromtxt(_,delimiter=',')
    l, r, g, b = arr.transpose()

for a in r, g, b:
    bl = a < -3
    print('range greater than 10^-3', l[bl].min(), l[bl].max())

r = 10**r
g = 10**g
b = 10**b

if __name__ == '__main__':
    fig, ax = plt.subplots(nrows=1,ncols=1)

    ax.plot(l, r, 'r-', label='r')
    ax.plot(l, g, 'g-', label='g')
    ax.plot(l, b, 'b-', label='b')

    #r = (740 + 625) / 2
    #g = 565
    #b = (466 + 436) / 2

    rc = 650
    gc = 530
    bc = 460

    ymin, ymax = ax.get_ylim()
    ax.plot([rc]*2, [ymin, ymax], 'r-')
    ax.plot([gc]*2, [ymin, ymax], 'g-')
    ax.plot([bc]*2, [ymin, ymax], 'b-')
    ax.legend()

    plt.show()
