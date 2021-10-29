Phase space of current, voltage, and power for some power supplies found in a
lab. The relationship P = IV is as simple a relation as can be, as is the
logarithmic form log(P) = log(I) + log(V). However, achieving wide ranges of
current and voltage (and therefore power) is a hard engineering problem. Even
today power supplies with large I-V ranges and high precision cost thousands
of dollars. Hence there is interest in documenting the I-V ranges (and also
power ranges) of available power supplies. The I-V ranges are represented by
vertical and horizontal bases of the rectangle, and the power range is the
difference in the diagonals of the rectangle, which is a height normal to the
plane of projection.

In chemical engineering applications power supplies are most often used to
precisely set temperature by the Joule heating effect, in which the power for
a voltage drop across a resistor is converted to heat. The cheapest power
supplies are fixed-voltage power supplies, which are only appropriate for this
application when the load resistance can be adjusted and maintained constant
to control the desired power delivery. These are shown as vertical lines in the
plots. In many applications load resistance is variable (uncontrollably so)
and even if it remains constant the power requirements may vary (e.g., to
change the temperature), in which case variable-voltage and variable-current
power supplies are needed. Different applications demand different ranges and
precisions.

While fixed current sources are common in, e.g., digital electronics
applications, I have never encountered them in power supplies. There are
therefore no horizontal lines in the plot.

Data source: Specifications in power supply manuals. Note the Power Supplies
Selector Guide from tektronics uses similar plots, using points to denote
maximum values. As an aside, a good UX design would be to have users click
somewhere (or click and drag a region) in the phase space and have the nearest
power supplies displayed, if a database of power supplies were given. Sorting
by cost, programmability, and other features gives a single-feature penalty in
an optimization problem, and generally one could weigh these factors.
