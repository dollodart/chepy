from numpy import sqrt, log10, arange, argmin

# candidate solution space
barxi = 10.**arange(-4, -2.60206, 0.05) # .1 mm to 1/4 cm thickness

def solve_with_surf_tens(rho, sigma, eta, s, show_space = False):

    S = sigma / (eta * s)  # dimensionless group from dimensional analysis
    f = sqrt(rho * g / (eta * s))
    barT = barxi * f
    err = (log10(S) + 5.45 * log10(1.5 * barT) - 
        0.151 / log10(1.5 * barT) - 1.44)

    if show_space:
        import matplotlib.pyplot as plt
        plt.plot(barxi*1000, err, 'ko-')
        plt.plot([min(barxi)*1000, max(barxi)*1000], [0]*2, 'k-')
        plt.xlabel('thickness in mm')
        plt.ylabel('residual in root function')
        plt.show()

    err = abs(err)
    amin = argmin(err)

    return barxi[amin]

if __name__ == '__main__':
    # properties of water
    # all in SI
    rho = 1000  # density
    sigma = 72e-3  # surf. tens.
    g = 9.8  # local gravitational constant
    eta = 0.001  # dynamic viscosity
    # convert to oil-like properties
    rho *= 0.7
    sigma /= 4
    eta *= 1.e2
    s = 0.03  # lifting velocity, m/s, approximately 1 in./s

    xi = solve_with_surf_tens(rho, sigma, eta, s, show_space=True)
    print(f"average film thickness = {xi * 1000:.1f} mm "
        + f"= {xi * 1000 / 25.4 * 1000:.1f} thou")

    # without surface tension effects
    f = sqrt(rho * g / (eta * s))
    print(f"average film thickness neglecting surf. tens. " +
        f"= {2/3 / f * 1000:.1f} mm = {2/3 / f * 1000 / 25.4 * 1000:.1f} thou")

    # if a plate is 1 ft by 1 ft, the volume of oil is
    v = 12 * 12 * xi * 1000 / 25.4
    print("volume on one side of 1' x 1' plate = {:.1f} in^3".format(v))
    print("equivalent cube edge length = {:.1f} in".format(v**(1/3)))
    print("volume per area = {:.2f} teaspoons/in^2".format(v * 3.32 / 144))
