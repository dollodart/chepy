Analyzes by physical model the mechanical properties derived from measurements
on wires of differing thicknesses. No guarantee to correctness of the physical
model is given.

Though the modulus of elasticity is nominally a bulk material property, for
these wires it is shown to be a function of the diameter even when the
diameter remains macroscopic (in the micrometer range). The yield stress
versus diameter plot is well fit by an inverted parabola when the fractional
change in the wire diameter is a factor of 10. This suggests there is a
physical reason for a square dependence rather than a fit simply due to a
local approximation, however there are also only 5 data points.

The modulus of rigidity is shown to have a power law exponent of less than (in
magnitude) -1/10. This is not a negligible change because the wire diameter
varies more than an order of magnitude, but it shows that a practical wire's
torsion response is to a good approximation constant with its thickness, an
important point for designing torsional pendulums using wires (which is often
done near small radii because the torsion constant varies as the quadratic
power of diameter---in fact, Cavendish could measure the mass of the earth by
the gravitational deflection of lead spheres on a rod suspended on a torsional
wire).

The yield stress has an approximate power law relationship, though it deviates
from this slightly forming a sigmoidal shape (which would be difficult to
explain on any physical grounds). The exponent is appreciable at -0.37,
the resulting curve for the yield strain from the rational quotient of yield
stress and modulus of elasticitiy is, like modulus of elasticity, parabolic,
though of course increasing. The division of something like the form x^-0.37 /
(ax^2 + bx + c) is necessarily not itself parabolic, so the resulting
fit should really be interpreted as a consequence of there being few data
points, especially since it has an otherwise unexplained vertex in the
middle of the data set.

# Effects of Extended Defects on Yield Stress

The size effect observed for yield stress is that it decreases with a low
power of -0.37 with respect diameter (but because diameter varies over a
factor of 333, the change in yield stress is still significant). The size
effect must be non-thermodynamic, and is due to extended defects in the
material. 

Extended defects cause the material to more resist initial (and
elastic) deformation because the material cannot relax in all degrees of
freedom to the applied stress, so in those remaining degrees of freedom the
effective strain is higher than it would otherwise be. Then the material
breaks earlier because parts of it are at a higher effective strain than the
nominal strain of the material (the strain that every part would experience if
it were homogeneous). It the case "The theoretical yield strength of a perfect
crystal is much higher than the observed stress at the initiation of plastic
flow." (https://en.wikipedia.org/wiki/Yield_(engineering)). Yet work hardening
is a method of increasing strength by introducing dislocations, in particular,
by the square root of dislocation density. This is due to higher dislocation
densities (the extended defect of interest) causing some defects to block the
movement of others (loc. cit.). Then strength is a non-monotonic function of
the dislocation density. A perfect crystal is strongest, a low dislocation
density is weakest, and a high dislocation density is intermediate in
strength. The weakest material, by this reasoning, would be that which has
many dislocation planes in parallel, so that the material could yield along
any dislocation plane without being blocked by any other. 

Methods for improving the strength of materials (once fabricated) rely on increasing
dislocation density. It is not possible to make polycrystalline or defected
crystals into a single crystal and it is expensive to produce single crystals
(for most engineering and mass production applications), and anyway the
dislocation density would increase from a single crystal for any material
which is regularly subject to large mechancial loads. And of course large and
frequent mechanical loads is the application where high strength materials are
needed. (Whatever other types of defects may exist, dislocations are the
primary ones of interest for the strain-stress curve relation).

# Effect of Extended Defects on Elastic Modulus

The maximum stress that can be applied before yielding, which is in a
stress-strain plot a horizontal line, is independent of the strain at which
the material yields. Therefore mathematically there is no necessary
relationship between changes in the yield stress and changes in the yield
strain. However, by the hypothesis that increasing dislocation density causes
undefected parts of the material to strain more than others, the elastic
modulus should increase, and the yield strain should decrease. But how much
they change relative to each other depends on where in the non-monotonic curve
of yield stress versus dislocation density one is at.

# Effect of Extended Defects on Modulus of Rigidity

Why the shear response should remain constant when the tension response
doesn't may be due to the orientation of extended defects in a wire. In
particular, a wire drawing process might introduce defects which are mostly
perpendicular to the axis of the wire, causing significant effects on elastic
modulus but insignificant effects on modulus of rigidity. For polycrystalline
materials, no difference is expected in the effect of a strain resulting from
shear and normal forces at the molecular level.

# Size Effects on Mechanical Properties in the Presence of Extended Defects

The manufacturing process for wires of different diameters may change the
extended defect concentrations, in particular, smaller diameter wires may have
more extended defects, since wires are continuously drawn through die. Since
the yield stress is found to increase with decreasing diameter, by the given
hypothesis, this would require that the die pulling process is effectively
work-hardening the wire. That is plausible given the wire is first smelted
and drawn into a standard thickness. The increase of elastic modulus
with decreasing diameter is explained, mathematically, by the fact that the yield strain
changes less significantly than the yield stress.

Data source: Handbook of Materials and Techniques for Vacuum Devices, Walter
Kohl, Table 9.3.
