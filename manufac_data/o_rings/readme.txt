Investigates the design space for o-rings in the AS568 specification.

The equation from geometry O.D. - I.D. = 2*thickness implies there are only
two degrees of freedom for an o-ring. This is verified by showing O.D - I.D. -
2*thickness is no greater in magnitude than 1e-14 inches for all o-ring sizes.

O-rings come in all sizes. There are more than 300 inner diameter and outer
diameters, but only 16 thicknesses. Series of monotonically increasing
O.D. at a fixed thickness are in size ranges 10--19, 20--29, 30--39,
40--49, 100--200, 200--300, 300--400, 400--500, and 900--1000. These are
called series here.

The number of outer diameters is different from the number of inner diameters,
even when rounding the inner and outer diameters to 3 or 2 significant figures
(5e-4 or 5e-3 precision). This is consistent with the equation from geometry
because for any given thickness, the number of unique inner and outer
diameters is the same (given a set X and a set Y, it is possible that a set X
x Y generated with the operator + has only unique elements: if |X| = |Y| = n,
then this would be n^2 unique elements, but for each y in Y, there would be n
unique elements from X, all of X, and n unique elements from X x Y, all of X
plus y). It's possible that in coming up with this standard, a set of I.D.
were used as well as the set of 16 thicknesses, and this generated almost
unique O.D. (so much can be found by consulting some references). Only 3 size
pairs are duplicates in the O.D., and each pair has one value in the 900
series, but there are 79 size tuples which are replicates in the I.D., which
include four triplets.  Some patterns suggest design, e.g., sizes 388--395 are
correspondingly duplicate in I.D. with sizes 469--476.

The inner diameter (and outer diameter) do not make a geometric series. The
fractional change between sizes is much greater at the smallest sizes and also
significantly greater at the largest sizes than the intermediate sizes,
forming a kind of sigmoidal shape in a semilogy plot of the distribution that
may be approximated by three linear pieces, each a geometric series. The
thickness is similar in its distribution (though much more discrete with only
16 values). One can also take a "logarithmic difference" (divide each value by
the previous one) to show the fractional steps. This shows that even in
regions which may appear piecewise geometric, the fractional differences can
vary significantly, but make intervals of spikes with nearly the same height
and so giving an appearance of a geometric series in these intervals. Some
fractional differences are as small as .1%.

Within each size series (equivalent to grouping by thickness), the outer
diameter does not make an exact geometric series, though the shapes are no
longer sigmoidal and are significantly more linear in semilogy coordinates,
with only the low values tailing down, that is, the density of o-ring sizes is
less at smaller sizes.  This may be approximated by a geometric series to some
error and for the three-digit series the average absolute fractional error is
no more than 15%, though the maximum is as high as 75%. This is plotted by the
series number because the series number is uniformly incremented, so it will
make a geometric series when plotted in semilogy coordinates which can be
regressed. The average fractional step in the series varies in the range
of 3--5%, with higher numbered (and higher sized) series having smaller
average fractional steps.

Data source: The AS568 standard is available from many online sources. This
data was taken from allorings.com.
