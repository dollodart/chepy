Design analysis of high-power and high-temperature consumer-commercial heater
cartridges. 

Systematic analysis is done using correlation coefficients (assuming
linear relationships, which is likely valid). One can also look at the
distributions of all variables, which is far fewer than the correlations
of all pairs.

Element length and diameter are conspicious as a design parameters because
they are stepwise uniformly distributed (nearly stepwise linear in cumulative
distribution). Power, the only other independent variable (except lead length
which isn't related to device output), is nearly stepwise uniform in 0 to 560
watts, but then tails at higher values.

Volume correlates well with power, as expected for constant volumetric heat
rate. Note the volumetric heat rate, is, though, far from constant: the mean
and standard deviation are approximately 3000 and 2000 W/in^3. Volume
correlates even better when grouping by diameter (or what is the same,
grouping by area); this suggests a relatively constant "heat flux" (see (1)).

Wire lead lengths are negatively correlated with power and power density
(there are only 12 and 16 inch lengths, though). In particular, those elements
with the shorter wire lead length are about 44% longer and have a power nearly
400% greater than those with longer wire lead lengths. Perhaps longer wire
leads are more needed in applications with smaller length and lower power which
need to be placed in a hard to reach parts of machines or process equipment.

The power versus current curve at fixed (RMS) voltage is exactly linear, as
required by its definition P = IV. By Ohm's law, for a given material, I =
V/rho*A/L, but the data for these elements is very spread in correlating I
with A/L, indicating either different resistor materials are used between
different models (perhaps) or the element length and width is unrelated to the
lengths and widths of resistors and/or series or parallel circuit arrangement
of resistors (likely). Of course, since the element power is a separate design
dimension from its length and diameter, one expects this spread and
inapplicability of Ohm's law.

(1) Heat doesn't have a direction, but the heat flux can be thought of as simply
a multiple of the current density, which does have a direction (since P = IV,
and power and heat rate are the same for a resistor). The heat flux should be
equivalent to power density, but the provided data shows it is not. In fact,
the reported power densities are on the order of 100 W/in^2, while the heat
fluxes calculated from the quotient of power and cross-sectional area are on
the order of 10,000 W/in^2. Power densities reported in the data might be for
the resistors rather than cumulatively for the elements. But the resistors
would have to have power density greater than the element, since they at most
take up the same cross-sectional area. It is irrelevant for the area-specific
power density that resistors can wrap around many times inside the element and
have lengths significantly greater than the element length---given a power and
voltage, there is a current, and therefore a current density, and therefore a
power density, independendent of the length. There is a linear power density,
which is the current times the voltage drop per unit length, which is a more
physical varaible that corresponding to the heat released per unit length.
But this is specific to length, not area.

Data source: McMaster-Carr catalog using chrome plug-in Table Capture. 
