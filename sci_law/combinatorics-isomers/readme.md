# Semilogarithmic Fit to Data

The script fits a line to the logarithmic and semilogarithmic plot of number of
isomers to number of carbon atoms for a hydrocarbon. If the combinatorics yield
exponentials, then the semilogarithmic plot will be linear. If the
combinatorics yield factorials, then taking the logarithm of the factorials
yields by Stirlings approximation something of the form n x ln(n), and the
semilogarithmic plot will be approximately linear over some range since ln(n)
grows much more slowly than n.  The fit using semilogarithmic coordinates is
excellent with R^2 = 0.99, though lower magnitude points which are deviating
from the law are clustered together.  The logarithmic fit is very poor because
a power law relationship increases too slowly for the observed exponential
relationship.

The consulted mathematician's conclusion (see textbook data source) is that
there is no closed form, which accords with results of easier enumerations (see
below) which only have infinite power series. But over large ranges it may be
linear (or of another simple functional form like second-degree polynomial) in
the semilogy space and predictable to some error.  

# Theory of Enumeration of Isomers 

One expects a recurrence relation which leads to something like exponential
growth in the number of possible isomers, which would also lead to a linear
plot in the semilogarithmic space. However, such a recurrence relation is hard
to derive because each carbon atom can have only so many bonded carbon atoms
(0--4) and symmetries make some permutations equivalent. Knuth (The Art of
Computer Programming, Second Ed., Vol. 2, Section 2.3.4.4) derives the
enumeration of binary trees as asymptotically 4^n/(n.sqrt(pi.n)) and higher
order terms, which is a lower bound on the number of isomers for a hydrocarbon
with n atoms and linear in logarithm. He also derives the power series for the
number of structurally different free trees, which is an upper bound on the
number of isomers for a hydrocarbon, since free trees can have any number of
edges between two nodes, or in the present case, any number of bonds between
atoms.

In fact, the problem of enumerating the isomers of hydrocarbons of the form
CnH(2n+2) is one of rich history, which is discussed in Biggs, Lloyd, and
Wilson's History of Graph Theory. Illustrious mathematicians such as Sylvester,
Cayley, and Polya have contributed to this problem, in fact a famous theorem
(Polya's enumeration theorem) was applied to enumerate the isomers. Accordingly
this problem is discussed widely, for example, the Handbook of Applicable
Mathematics has in its volume on combinatorics a table of the number of isomers
of CnH(2n+2) developed by an algorithm in a research paper. A brief survey of
the history of the problem of enumerating hydrocarbon isomers, and the
application of a generating function method like that used in Knuth though with
an explicit consideration of group theory, is available at
https://arxiv.org/abs/math/0207176v1. These reference sequences in the OEIS
which are exact and provided up to small integer numbers.

Data source: Table 2.1 of Organic Chemistry by Carey, Guiliano 9th Edition.
