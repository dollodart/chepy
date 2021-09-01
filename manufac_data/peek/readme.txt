Analyzes PEEK tubing data especially for flow characteristics depending on
tubing size. PEEK tubing is often used for liquid injection in
customized experimental apparatus for gas phase transport as well as for
liquid chromatography. Done here are:

- Calculate the superficial velocity using material balance given the inner
  diameter. To prevent dripping when using low flow rates, sufficiently small
  inner diameters should be chosen.
- Calculate the pressure drop for water using the Hagen-Poiseulle equation.
  While smaller inner diameters increase superficial velocity and so flow
  consistency, pumps (especially syringe pumps) are limited in the force 
  , therefore pressure, therefore flow rates they can apply.
- Calculate the stream trajectory using the free fall equation. This is the
  same as the free fall equation for a point mass except that the time
  variable is replaced by the quotient of distance along horizontal axis over
  superficial velocity. This is because the time required for the liquid to
  travel a distance x in the horizontal direction at superficial velocity s is
  x/s.  This is known as the Purdue trajectory method in the literature when one
  calculates from a trajectory a flow rate. If an injection port is put into the
  side of a tube, this informs where the liquid stream will strike and at what
  velocity. Note that for the chosen flow rate of 10 uL/min, only the smallest
  tube diameters will fall streams that fall anywhere other than directly below
  the orifice.

PEEK tubing colors do not make a geometric series. The fractional tolerance is
not monotonically decreasing with inner diameter.

As an aside, industrial solutions for mixing liquid in a gas stream is to
"atomize" the liquid, or make small (submicrometer) globules which suspend in
the air and with a low area-specific volume vaporize quickly (another effect
for sub micrometer globules is that the surface tension makes them
thermodynamically less stable and so the vapor pressure increases by the
Kelvin equation). This can be done using ultrasonic frequencies on a
cantilever dispenser.

Data source: PEEK tubing catalogue from original manufacturer. The data table
for has diameter and tolerance in inches and tolerance as +/- (half tolerance
range).
