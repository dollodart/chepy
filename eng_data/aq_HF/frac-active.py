import numpy as np
import matplotlib.pyplot as plt


def HA_frac_1(xa, Ka):
    a = 1 / Ka - 1
    b = 1
    c = - xa * (1 - xa)
    n = (b - np.sqrt(b - 4*a*c)) / (2 * a) 
    return n + xa

def HA_frac_2(xa, Ka):
    """
    Equivalent formulation of quadratic problem to HA_frac_1.
    """
    d = Ka*(1 - np.sqrt(1 + 4*(1/Ka - 1)*xa*(1-xa)))/(2*(1-Ka))
    return d + xa

pKa = 3.17
Ka = 10**(-pKa) # constant for HF
xa = np.arange(0, 0.5, 0.01)
vals = HA_frac_2(xa, Ka)
plt.semilogy(xa, vals)
plt.xlabel('Fraction HA/H2O')
plt.ylabel('Fraction Active HA(aq)')
plt.show()
