Bar plots of engineering data using the pgfplots package. The main value in
these, as compared to tables, is that they visualize the relative magnitude
while still containing all the data in a searchable form (alphabetized on the
y-axis and containing the numerical entry at the end of the bar). In cases
where the quantities vary by more than two orders of magnitude this requires
a logarithmic axis, in which case the bar plot areas are misleading, since
proportional areas are not proportional magnitudes. In the given base of 10
for the logarithmic axis, a twice as large area is 100 times the quantity, and
generally, a ratio of areas of x is 10^x ratio of magnitudes.

There is a question about pagination, since sometimes the quantity of data is
very large. Obviously one cannot print, on usual printers, 40 cm wide or tall
paper (because the text used in the graphs must be legibly large and is often
the same dimension as the bars, the paper size must be large). However for
viewing on a computer it is fine because things can be magnified, and for
computer viewing pagination just lowers the ability to compare all data. For
best viewing, some application viewer like Javascript webpage application
(with appropriate filtering) might be used rather than static plot generation.

Data source: Data taken from several freely available online sources including
the Engineering Toolbox. The motivation for these types of plots came from
difficult to read graphs in Analysis, Synthesis, and Design of Chemical
Processes Fig A.18 and A.19, which were then extended to datatables, since
this plotting both improves graphs in which one axis is an identifier by
effectively making it a table/graph combination with the value easily read off,
and improves tables by adding a visual dimension to compare entries.

Data for solvent polarities: Miller online
