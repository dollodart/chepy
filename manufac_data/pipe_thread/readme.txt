Analyzing the NPT specification used for connecting pipe parts for fluids under pressure.

As a practical matter, from the source regarding NPT:
    *Note!* Pipe sizes do not refer to any physical dimensions. The outside
    diameter of a pipe or fitting must be measured and compared to a table for
    size identification. A 3/4" NPT pipe thread has an outside diameter - OD - of
    1.050 inches. Each thread size has a defined number of threads per inch - TPI,
    or pitch. The 3/4" NPT pipe thread has 14 threads per inch. Both the TPI and
    OD of the thread are required for positive identification of thread size
    because more than one size have the same TPI.

This practical problem is shown by the plot of the nominal OD versus the pipe
size. In some cases the nominal OD is so sized that one would purchase the
incorrect pipe size assuming the pipe size is the nominal OD. For example,
measuring a pipe to be 3.5" in outer diameter and assuming this is the pipe
size leads to a pipe with a 4" diameter.

The length of threads is the axial distance, as indicated by it being equal to
the reported number of threads divided by threads per inch. The reported total
thread makeup has an approximate proporitionality with a factor of 1/sqrt(2)
to the reported length of threads.

The correlation between nominal outer diameter and tap size is strong but not
exact. The tap drill size is smaller than the nominal outer diameter. This
should be due to the thread depth (see specification or consult general
geometric diagrams for screws). The thread depth calculated from the data is
seen to be piecewise constant. 

The smallest length of threads is 3/5", and for every inch gain in the outer
diameter, there is only about a 1/5" gain in the length of threads. Note,
however, that due to the decrease in the TPI for larger sizes, the number of
threads is relatively constant: it increases from 10 threads to 14 threads
with larger pipe size.

Because the number of threads is relatively constant, and the outer diameter
is strongly correlated to pipe sizes, there appears a correlation of pipe
size and 'nominal arc length' of threads. This correlation, however, is easily
explained by the earlier results and not interesting. It is perhaps remarkable
that for the largest pipe sizes this nominal arc length is nearly 25 feet.

As regards nominal arc length. For a given axial distance (length of threads),
the arc length of a helix has the following form.

L.𝜋.√( ((OD/in).TPI)^2 + 1)

However, when the OD.TPI is large compared to 1, this is equal to the circumferences
of the number of circles: L.TPI.𝜋.OD. That limit is reached for all the pipes.

Data source: Engineering Toolbox, ANSI B1.20.1.
