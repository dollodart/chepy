Explores thermodynamic correlations using the thermo package. These are
chemical correlations, e.g., how do chemical properties correlate when
considering a large number of chemicals. It is therefore a structure-property
relationship investigation.

There are many thermodynamic relations that do not predict what the value of
some property at standard temperature and pressure is, but what the value of
the property is up to a constant with respect to some thermodynamic variable.
An example of this is the Eyring relation between heat of vaporization and
activation free energy for viscous transport as a function of temperature
(this is Andrade's relation when empirical), and the functionally identical
Clausius-Clapeyron equation for vapor pressure (this is Antoine's equation
when empirical). In these the prefactors for the thermodynamic variables are
not predicted, only their temperature relationships, and they only apply to a
single substance. These relationships, derived from thermodynamics, are not
able to make predictions for thermodynamic properties between different
substances. For that, one needs models based on molecular structure and
chemical identity, which are famously hard for condensed phases (ideal gases,
on the other hand, can have all their relevant thermodynamic properties well
approximated by just two fundamental molecular parameters, an interaction
energy and collision cross-section).  However, correlations such as the ones
made here can be applied to guide chemical reasoning: qualitative results
should follow from qualitative consideration of chemical structure and
chemical identity.

Material scientists often make plots where the various regions in 2-D phase
spaces of mechanical properties are divided into (approximate) regions by
material. This serves to make analogous plots for chemicals and relevant
thermodynamic and transport properties. Chemical identity is related to
chemical structure, so one need only make plots of the properties (here xy
plots surface tension, viscosity, vapor pressure, to imitate the plots in
material sciences, but one could also look simply at 1-D scatter plots) and
label by chemical identity to infer some chemical structure-property
relationship. This could be further refined by, e.g., plotting against
quantitative measures of structure, such as effective molecular radius or
molecular weight.

One can find even relatively recent literature on structure-property
relationships in chemistry, e.g., 10.1021/ci000139t. In this paper, which is
limited to organics, still there is use of neural networks, informing the
impossibility of any physically exact relationship for properties based on
chemical structure. At least my general chemistry courses did not make
quantitative or even semi-qualitative predictions of chemical properties, but
they did discuss structure-property relationships without the use of plots or
making a systematic treatment of materials. See, e.g., CH 7 Structure-Property
Relationships of the Chemistry LibreText Book: Structure & Reactivity in
Organic, Biological and Inorganic Chemistry (Schaller).

For example, on molecular reasoning, one generally expects surface tension and vapor
pressure to correlate negatively, since the greater the attractive forces
between molecules, the greater the surface tension but less volatile the
material. The most obvious example is mercury, which has a high surface
tension (~500 mN/m at STP) and low vapor pressure (.0017 torr at STP) due to
the strong metallic bonding between the atoms (which is atomic bonding forces,
rather than intermolecular forces between, e.g., organic molecules).

While not a thermodynamic property, one also expects the viscosity to
correlate positively with surface tension and negatively with vapor pressure,
on the same molecular reasoning---molecules more attracted to each other will
resist flowing past each other to a greater extent.

But there are many confounding factors: vapor pressure tends to decrease with increasing
molecular size significantly, but the viscosity and surface tension may not
decrease as dramatically provided the molecule has a functional group that
allows there to be strong interactions. 

Large molecules may be highly viscous not because of interactions but because
they intertwine with each other (this is most exaggerated in polymeric
solutions). Then the surface tension may remain largely the same as viscosity
increases. One can see that in homologous alkanes, the surface tension grows
by around 50% at the same time the viscosity increases by an order of
magnitude, or 1000%.  This doesn't imply a poor correlation in the alkanes: in
fact, one can see that there is a clear, if non-linear, relationship, for
these two variables. But because higher intermolecular forces would generally
cause surface tension and viscosity to both increase, while this size effect
can cause viscosity to increase while surface tension remains nearly the same,
the correlation including alkanes and other chemicals is poor. In fact, we may
expect that some materials inhabit most every region of the space, just as in
those structure-property relationship plots for mechanical properties in
materials science.

Data source: Engineering Toolbox, and data through the thermo package. Thermo
has an extensive set of reference data including several correlations used for
extrapolating data to unknown conditions. As an aside, thermo provides many
plotting utilities which can be used to check against thermodynamic relations
through methods on its "property objects", e.g., the chemical.VolumeLiquid
property is not just a method which evaluates the liquid volume but an object
that supports many methods, such as plot methods.
