Analytics of spring parameters for compression springs.

# Correlations Generally

The below discussion on geometries is limited to the case that the plot axes
are equal in the magnitude they span and the quantities plotted are loglog
quantities.

When the scatter plot has a bounding shape like a square aligned with the
axes, the correlation is zero (this is also the case when the bounding shape
is a rectangle).  When the plot has a bounding shape like a square turned 45
degrees to the axes, the correlation is equal to the variation. One finds the
more general parallelogram as a bounding shape because variables mutually
constrain each other. In that case the correlation is the angle of the
parallelogram while the variations are the base and the height.

The reason to take log coordinates is not necessarily because the relationship
is non-linear, but to equally weigh by magnitude the points. This allows one
to accurately derive scaling relationships even when they are linear. By
correlated here in general I mean in logarithm, which also includes the usual
correlation (linear).

# Spring Design

The design space is large and varies some parameters almost independently.
Even parameters that are highly correlated are having high variance, defined
as more than two orders of magnitude. 

There are only 4 independent design variables (independent meaning satisfying
degrees of freedom in a physical model, not meaning uncorrelated in the design
space). These can be taken to be the wire diameter, the mean diameter (of the
coil), the unloaded length, and the number of (active) coils. All other
parameters either physically result from these 4 independent design variables:
the resulting loaded length, the maximum displacement, the maximum spring
force, and so on; or they result as a matter of calculation, such as rate
being maximum force divided by maximum displacement. Any other differences are
attributed to material differences, which for the steels looked at here are
not great.

The coil diameter and the equilibrium length are highly correlated, with a
linear relationship (in fact all exponents are calculated as nearly zero or
between 0.9 and 1.0). The coil diameter and the wire thickness are highly
correlated (this implies that the equilibrium length and wire thickness are
also highly correlated). The coil diameter must be greater than the wire
thickness, and is on average 8.4 times greater.

The number of coils is a variable independent of both the coil diameter and
wire thickness, making a grid with them. The number of coils is only weakly
related with the equilibrium length, which is perhaps surprising since for a
given lineal coil density they are exactly linearly related.  But given that
the number of coils is not correlated with coil diameter, and equilibrium
length is highly correlated with coil diameter, this fact follows.

Arc length and solid length are highly correlated, even though solid length is
but this is because the equilibrium length and coil diameter are highly
correlated. Solid length and arc length are distinct geometric variables,
being the axial length on compression and length of wire at equilibrium.

Force is correlated with coil diameter and equilibrium length
(naturally, as coil diameter and equilibrium length are highly correlated). It
is expected that larger coils have greater maximum force.

# Mechanical Properties

From a physics perspective, having a mechanical system determined by three
lengths and a number is incorrect. That is because there are mechanical
properties of the material that relate geometric quantities to mechanical
ones, most notably force. If one includes the spring constant, then that
relates length and force, but it varies with the geometric variables. The best
parameterization is in terms of fundamental mechanical properties of the
material.

The shear modulus is calculated according to continuum mechanical theory, in
the limit that the lineal coil density times the wire diameter is large (and
so the forces acting on the spring wire are almost all shear). This limit
should be evidenced by alpha, the angle made from the coil to its axis, though
I would note the laws apply quite well even though the maximum angle is more
than a 1/3 right angle. The shear modulus is found to be constant and within
the ranges of that reported for the grades of steel by other sources. Then the
design space is out of Dt, Dm, L0, nv, and G (using the variable names used in
the script).  However, because only similar steel materials are considered
here, effectively the design space is geometric, the resulting mechanical
variables such as maximum force only varying due to geometry, as was found in
the section on spring design.

Data source: Inexal, a Dutch technical spring supplier. DIN 2098 standard.
Units: distance in mm, force in N.

The rate is defined as the (rational) quotient of spring constant and
deflection, and the deflection is defined as the difference in equilibrium and
compressed length.
