This script investigates the trend of heat of formation of straight chain
hydrocarbons with increasing length in a manner like that of the paper used
for part of the data source.

# Trend of Carbon Unit Specific Heat of Formation

It is found that the mole specific heat of formation, defined by number of
carbon atoms, decreases in magnitude with increasing chain length. That is,
there is less energy incentive to build large hydrocarbons than there is to
build small ones. More exactly, the 'methylene heat of combustion' from the
paper, the intercept in the plot of H/n versus 1/n, is found to be -157.0
kJ/mol, which is compared to the heat of combustion of methane which
is -212.8 kJ/mol. Thus a 'methylene heat of combustion' is 73.8% of the value
of a 'methane heat of combustion' (see theory section).

Some remarks on this fact in the general domains of science. In biology there
is often cited the fact that it requires energy to build larger organic
molecules from smaller ones, which is in agreement with this result. This fact
is the same when considering reaction from carbon dioxide and water as
precursors, to the combinations of organic molecules such as saccharide
monomers into disaccharides (even when these have generally far more
complicated functional groups including oxygen, the relevant point is the
carbon-carbon bond formation, those other functional groups often being
retained or simply shifted around, or as it turns out the dehydration
reactions required to form also costing energy). In oil formation, large
hydrocarbon chains originally derived from decaying organic matter are
degraded in high temperature processes, and beyond a certain temperature they
are converted to methane.  This process is called cracking, and this accords
both with the energy and (not discussed here) entropy incentive of making
smaller hydrocarbons from larger ones.

## Theoretical reasoning

The terminal methyl group contributions to the energy vanishes to zero as the
number of carbon atoms (and therefore the number of methylene atoms minus two)
approaches infinity. This theory is well developed in the paper using the data
source, and in fact there was a literature on the subject of the enthalpies of
formation of normal hydrocarbons. To excellent approximation the energy of a
hydrocarbon is a superposition of bond energies which depend only on the atoms
they bond; the dependence on the further bonding is negligible for most cases
of interest, as is commonly the case in organic chemistry. The reason for
decreasing (in magnitude) heat of formation is that carbon-hydrogen bond
formation is more favorable than carbon-carbon bond formation, so from the
elements making CH3-R (3 C-H bonds and one C-C bond) is more favorable than
R-CH2-R (2 C-H bonds and 2 C-C bonds). This is shown by the below data
from Chemistry LibreTexts:

Bond,Energy/(kJ/mol)
C-C,348
C-H,413
H-H,436

Therefore the formation of C-H bonds has the following energy of reaction:

H2 + C2 -> 2CH (2*(-413) - (-348 + -436) = -42 kJ/mol)

That is, it releases 21 kJ/mol of energy when one forms a C-H bond from C-C
and H-H bonds. 

## Quantitative Agreement

The paper reports both heats of combustion and formation. Here the heat of
combustion from the paper is compared to the heat of formation from the other
data source using heats of formation of carbon dioxide and water. The other
data source has disagreement only on average of 3% with that of the paper in
the heats of formation. 

For the heat of combustion, the paper reports the general formula 7.91 - 5.55n
when n > 5, which is to the same number of significant digits reproduced here.
The intercept in the inverse plot (1/n as the horizontal axis) is by theory
equal to the slope in the primal plot, and is in agreement by fit. In order to
evenly weigh the contributions of data points when doing a linear regression
in the inverse plot, an alternation of logarithmic fitting (to obtain a slope)
and linear fitting (to obtain an intercept) is done.

# Deriving Bond Energies from Heats of Formation

The paper goes on to, from these, discuss how the bond energies (which are
above tabulated from LibreText sources) are related to the data, though it
notes that 'bond energy' is an approximation and second nearest neighbors may
be relevant, including citing spectroscopic data on the point. The question is
if bond energies may be derived from heats of combustion or formation found in
the data. But in fact one needs the heats of atomization from the elements to
do this. The basis taken of zero energy for the elements in heat of formation
makes it not possible to derive bond energy.  Naively regressing heat of
formation (or heat of combustion) data gives only qualitatively correct data
in that the C-H bond formation is more favorable than the C-C bond formation,
but it also gives very incorrect trends where the bond energies vary
significantly depending on nearest neighbors. The paper gets around the
problem of atomization energies by determining deviation from linearity, but
this is highly similar to the already made plot of carbon unit specific heat
of formation (in fact figure 2 appears to be simply a reflection and change of
scale on the y-axis from figure 1).

Data source: Heat of formation data source Chemistry LibreText. All other data
from HEATS OF COMBUSTION AND OF FORMATION OF THE NORMAL PARAFFIN HYDROCARBONS
IN THE GASEOUS STATE, AND THE ENERGIES OF THEIR ATOMIC LINKAGES By Frederick
D.  Rossini.
