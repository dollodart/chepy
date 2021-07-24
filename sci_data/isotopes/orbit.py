# this method of assigning orbitals doesn't take into account known
# exceptions to the Aufbau principle
dct = {i + 1: {'s': 0, 'p': 0, 'd': 0, 'f': 0, 'period': 0, 'group': 0}
       for i in range(118)}

z = 0
for period in range(1, 8):
    s = p = d = f = 0
    for s in range(1, 3):
        z += 1
        dct[z]['s'] = s
        dct[z]['period'] = period
        dct[z]['group'] = s
    if period > 5:
        for f in range(1, 15):
            z += 1
            dct[z]['s'] = s
            dct[z]['f'] = f
            dct[z]['period'] = period
            dct[z]['group'] = s
    if period > 3:
        for d in range(1, 11):
            z += 1
            dct[z]['s'] = s
            dct[z]['f'] = f
            dct[z]['d'] = d
            dct[z]['period'] = period
            dct[z]['group'] = s + d
    if period > 1:
        for p in range(1, 7):
            z += 1
            dct[z]['s'] = s
            dct[z]['f'] = f
            dct[z]['d'] = d
            dct[z]['p'] = p
            dct[z]['period'] = period
            # new convention, old convention is s + p for p-block elements
            dct[z]['group'] = s + d + p


def fmt(adct):
    string = ''
    for orb in 's', 'p', 'd', 'f':
        if adct[orb] > 0:
            if adct[orb] == 1:
                string += orb
            else:
                string += orb + str(adct[orb])
    return string


dct_fmt = {i: fmt(dct[i]) for i in dct.keys()}
