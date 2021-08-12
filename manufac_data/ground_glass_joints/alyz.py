import sys
import numpy as np
import matplotlib.pyplot as plt

lines = open('ground-glass-joints.csv', 'r').readlines()

ggjs = []
for line in lines[2:]:
    line = line.rstrip('\n')
    line = line.split(',')
    for field in line:
        if field == '':
            continue
        ggjs.append(tuple(float(f) for f in field.split('/')))

tr = 0.1 # taper ratio
ggjs = np.array(sorted(ggjs, key=lambda x: (-x[1], -x[0]))) 
# sort descending on length and then width for visualization

def diagram():
    fig, axs = plt.subplots(nrows=1, ncols=2)

    for co, bl in enumerate((ggjs[:, 0] / ggjs[:, 1] < 1, ggjs[:, 0] / ggjs[:, 1] > 1)):

        ax = axs[co]
        ax.set_aspect(1)

        for p in ggjs[bl]:
            y0p = p[0] / 2.
            y0n = -y0p # == - p[0] / 2.

            y1p = y0p - tr * p[1] / 2.
            y1n = -y1p # == - y0p + m * p[1] / 2.

            x0 = 0
            x1 = p[1]

            plot = ax.plot([x0, x1], [y0n, y1n], label='{0}/{1}'.format(*p))
            c = plot[0].get_color()
            ax.plot([x0, x1], [y0p, y1p], color=c)
            ax.plot([x0] * 2, [y0p, y0n], color=c)
            ax.plot([x1] * 2, [y1p, y1n], color=c)

        ax.set_xticks([])
        ax.set_yticks([])

        for x in ['right', 'top', 'bottom', 'left']:
            ax.spines[x].set_visible(False)

        ax.legend(bbox_to_anchor=(co, 1.0))

def fitting_pairs(log=sys.stdout):
    """
    An algorithm more efficient than O(n^2) possible with interval tree
    construction in O(n lg(n)).
    """

    parts = []
    parts_noexcess = []
    for i in range(len(ggjs)):
        for j in range(len(ggjs)):
            if i == j: 
                continue
            wa1, la = ggjs[i]
            wa2 = wa1 - tr*la
            wb1, lb = ggjs[j]
            wb2 = wb1 - tr*la

            if wb2 <= wa1 <= wb1:
                i, j = j, i
                wa1, la, wa2, wb1, lb, wb2 = wb1, lb, wb2, wa1, la, wa2

            if wa2 < wb1 <= wa1: # b fits into a, and if long enough, will stop
                frac = (wa1 - wb1) / (wa1 - wa2) # how far into the channel of a until the width is equal to that of b?
                lc = la * frac
                if lc + lb <= la:
                    parts_noexcess.append((i, j))
                    print(i, j, file=log)
                    print(f'partial fit for {wb1}/{lb} in {wa1}/{la} at {100*frac:.0f}% in channel', file=log)
                    print(f'  no excess length', file=log)
                else:
                    parts.append((i, j))
                    print(i, j, file=log)
                    print(f'partial fit for {wb1}/{lb} in {wa1}/{la} at {100*frac:.0f}% in channel',file=log)
                    print(f'  excess length = {lc + lb - la:.1f} mm',file=log)

    print(f"{len(ggjs)} number of ground glass joints",
          f"{len(ggjs)*(len(ggjs) - 1)} number of directional pairs",
          f"{len(parts) + len(parts_noexcess)} directional with partial fit",
          f"{len(parts_noexcess)} directional pairs with partial fit and no excess length",
          sep='\n', file=log)

    return parts, parts_noexcess

if __name__ == '__main__':
    with open('log.log', 'w') as _:
        fitting_pairs(_)
    diagram()
    plt.show()
