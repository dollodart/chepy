TODO: still thermodynamically inconsistent integration (path dependent)

# Motivation

Justify the heuristic "add acid to water"

# Heat of Solution Data

The heuristic "add acid to water" might be evidenced by the low heat of mixing
for dilute solutions of strong acids in water, but the corresponding limit, of
dilute solutions of water in strong acids (for those mineral acids which are
liquid at room temperatures) is not shown by heat of solution data. This is because the
heat of solution data goes only between approximately 0 to 50% composition of
the solute in water. Note one can only deduce from the heat of solution at 50%
composition an upper bound of that in the limit of large amounts of the
solute. The trend of the heat of mixing must be 0 toward composition of 0 and
100% solute composition, and the heat of solution
should asymtoptically limits to values smaller than the 1:1 composition.

## Relation of Heat of Solution and Heat of Mixing

The heat of solution is related to the heat of mixing by material
balance as

𝛥 h_m = 1/(1+n) 𝛥  h_s

Then the following limit arguments apply:

lim_(n->0) 𝛥 h_m = 0 necessarily 
lim_(n->0) 1/(1/n) 𝛥 h_s = 𝛥 h_s which implies
lim_(n->0) 𝛥 h_s = 0.

In the limit as n->infinity, as the plots show, there is no known bound on the
heat of solution, though clearly it bounds to a constant value as it must. This
is because 1/(1+n) goes to 0. The heat of solution is asymmetric in what it
defines as solvent (which is assigned n moles) and what is defined as solvent.
When n = 1, the two heats of solution for a binary mixture considering one the
solvent and the other the solute are equal. There is no limit on what 𝛥 h_s,
considering water to be the solute, has to be, given its value at equimolar
composition, at least from simple limit arguments. In the heat of solution data
𝛥 h_s is monotonic even when 𝛥 h_m is not, looking at the example of H3PO4 in
water. The mixture of chloroform and methanol has a highly non-linear heat of
mixing of chloroform and methano: adding chloroform to methanol is exothermic,
but adding methanol to chloroform is endothermic, approximately, with the heat
of mixing inverts sign at a composition of around 64% chloroform in methanol.
But the heat of solution is monotonic with respect to both methanol and
chloroform as solutes. Because the data points are limited, a cubic spline
interpolator is used to further justify these conclusions.

For universally favorable interactions like those between acids and waters, the
heat of mixing may be symmetric and like a parabola, and in any case it has
only one extremum.  Because of this, the heats of solution for both solutes are
decreasing with increasing solvent number at least at compositions near the
limits of pure components, so the equimolar heat of mixing gives an upper bound
on the heat of solution.

# Heat of Mixing of Sulfuric Acid and Water

While not a general analysis, the source provides for all compositions the heat
of mixing for H2SO4 and H2O, and one expects the arguments for other aqeous
solutions of acids to be similar. 

In figure E6.13 of Koretsky, the partial molar enthlapy of sulfuric acid as a
dilute solute is -72 kJ/mol, while the partial molar enthlapy of water as a
dilute solute is -32 kJ/mol. This data alone might suggest adding water to
acid. But one one wants to achieve a relatively, though still non-zero, dilute
solution of acid. Most acidic solutions prepared are relatively dilute in the
acid, something like 10%. It is mostly because the heat capacity (extensive) of
the large amount of water used is far greater than that of the acid that one
would want to add acid to water for such solutions. While the ultimate
temperature, if adiabatic, of the mixture is independent of how you add the
components, the intermediate temperatures of the solution do depend on it, and
these are what is dangerous. If you were to prepare an equimolar solution of
acid and water, the only factor that would be relevant is the ratio of molar
specific heat capacities (choose to add to the substance with a higher molar
specific heat capacity so the intermediate temperatures will not climb as
quickly). The 'accumulated heat' upon differential addition of either acid to
water or water to acid of a 10% H2SO4 solution, an equimolar solution, and a
90% H2SO4 solution are shown to demonstrate this concept.

The evolved heat should not differ depending on the path taken, though it
clearly does. This despite the fact that the thermodynamic consistency test,
provided by the data source, is passed.

Data source: Table 6.1 Koretsky Engineering and Chemical Thermodynamics, 2nd edition.
Heat of solution in kJ/mol solute
n in moles of H2O

One note: the kJ/mol solute applies when 1 mole of solute is added to the n
moles of water. The heat of solution isn't an intensive quantity like the heat
of mixing is to the moles of total solution. If one added .5 moles of solute
to n moles of water, the result isn't .5 times the heat of solution of adding 1 mole
of solute to n moles of water. The fact that 𝛥 h_m = 1/(1+n) 𝛥 h_s
implies that 𝛥 h_s is in fact an extensive heat, which should by most
conventions read 𝛥 H_s, since it is divided by number. It is meaningless to
conclude that the numerator 1 is 1 mole, rather than the identity operator,
because that would presuppose that 𝛥 h_s is intensive (in formal logic,
begging the question or assuming the conclusion).
