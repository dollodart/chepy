Analyzes the data for adsorption isotherms from the NIST API.

# About Data Normalization to Fit Langmuir Parameters

For a given isotherm, one can normalize pressure by the saturation pressure of
the gas, provided the temperature is below the boiling point of the liquid for
at least the maximum pressure. This won't be the case, for some elements such
as hydrogen. Note these normalizations are not thermodynamically guaranteed,
but can be absorbed into a coefficient in, e.g., the Langmuir isotherm.

y = K.p/(1+K.p) -> y = K'(p/p*)/(1+K'(p/p*))

However, this makes comparisons between different temperatures meaningless,
since the saturation pressure is a function of temperature. If one wishes to
compare results at different temperatures, or in case the saturation pressure
is infinite or simply unknown, one can impose an arbitrary normalization
constant (this amounts to putting in a unit, like 1 bar).

Now for the dependant variable, the provided data is 𝛴, which is a surface
coverage like moles per mass not equal to the surface coverage fraction. The
surface coverage fraction is equal to some constant multiple of 𝛴, that is, y
= c𝛴.  Then 𝛴/𝛴_0 = y/y_0, so that substituting into the ratio form of the
Langmuir isotherm yields 

𝛴/𝛴_0 = (K.p*(1 + K.p0))/((1 + K.p)*K.p0)

which can be manipulated to an explicit equation for K as

K = (𝛴/𝛴_0 - p/p0)/(p(1 - 𝛴/𝛴_0))

Given an explicit equation for a parameter, the least square
solution is simply the mean of the data vector. This is simple to prove:

min_a 𝛴_i^n (x_i - a)^2 
-a𝛴_i^n x_i + na^2 = 0
-an𝜇 + na^2 = 0
a = 𝜇

This explicit form of K is not merely a change in variables, because fundamentally
it requires a ratio form comparing two datapoints. When making a regression
against some data, the question is what to use as the reference data
point---any error in that data point would be propagated to other places. One
can evaluate for every point as a reference the best fit using all other
points, which creates a problem square in the number of data points.

This works even when using composition variables like wt/wt% because the mass
of adsorbent is small. The 95th percentile of wt% is 4.73. Even here there is
excellent approximation in m_ate/(m_bent + m_ate) ~ m_ate/m_bent = const. *
m_ate = const. * 𝜃, where 𝜃 is surface coverage fraction. In particular, if
the wt% is 4.73, then approximating the weight percent by m_ate/m_bent gives
4.75%, which is 0.42% error. It is quite remarkable that there are
adsorbent/adsorbate compositions where this weight composition is possible,
because if there is it suggests the solid has an 18:1 bulk-to-surface atom
ratio (and thus there is a 19:1 adsorbent-to-adsorbate ratio, assuming equal
molecular weights of the two). In fact rather exotic structures and relatively
high pressure conditions are required for 5 wt% (IRMOF-1, H2 at 45 bar
and 77K; Zn(BDC)(DMBPY), CO2 at 0.5 bar and 273K; Zn(NDC)(BPY), CO2 at 0.78
bar and 273K).

One need not eliminate surface coverage fraction provided some material
properties. Provided pressures are sampled low enough where one can assume 𝜃 =
0 and pressures are sampled high enough so that 𝜃 = 1, taken as a limiting
value, one can obtain the mass adsorbent at 𝜃 = 0, and interpolate with a
surface mass coverage fraction when the mass limits to be 𝜃 = 1 (and with
molecular weights of the two components, one can obtain any measure of the
adsorbate and adsorbent phases in terms of moles or mass).

The above discussion is how applied to the Langmuir isotherm, which has a
rigorous basis in statistical mechanics. The Freundlich isotherm is an
empirical power law which can be used. Except for piecewise-adsorption due to,
e.g., different site types, there is not in abundant use other models (some
more advanced models are sometimes used, such as the BET isotherm for modeling
multi-layer adsorption).

# Theory and Invariants

The chemical potential of a gas, which determines the equilibrium state,
increases logarithmically with pressure but, if other parameters are constant,
linearly or nearly linearly with temperature (𝜇 = 𝜇0(T) + R.T.ln(P) where
𝜇0(T) has for an ideal gas a T.ln(T) dependence).  Assuming the adsorbate
phase, which is a condensed phase, has a much weaker temperature dependence
(it certainly has a much weaker pressure dependence), one sees the equilibrium
condition requires pressure and temperature to covary as ln(P).T = const..
Though, adsorption is not an equilibrium state, a given surface coverage
fraction, say of 0.5, is.

One can test to see whether the quantity ln(P).T (or ln(P).T.ln(T)) is
invariant for a given surface coverage fraction for a given
adsorbate-adsorbent pair in this data (temperature, pressure, and experiment
may vary). It is difficult to do this for a specified surface coverage
fraction, because one isn't guaranteed that the median (or mean) value of the
sampled adsorption is a surface fraction of 0.5 (that's to say, 𝛴_mean != c/2
where 𝛴 = cy). But one can do it for some surface fraction, or rather, some
band of surface fractions (say 10% of the total range) at different quantiles.
Doing show shows this so-called invariant actually varies more, fractionally,
than do the independent variables of temperature and logarithmic pressure
(which is yet to be explained).

In fact, in adsorption the entropy may be a significant contribution to the
free energy at the equilibrium conditions of interest (I have heard it said in
lectures to be the object of stimulations to accurately calculate the
adsorption entropy). Then the adsorption free energy varies linearly with
temperature with a slope equal to the entropy of adsorption which is a
significant slope relative to the intercept for the temperature ranges of
interest. Thus even if constant with respect to temperature, there would be no
invariant across several materials for which the entropy of adsorption differ
significantly, and there is no *a priori* way to obtain the invariant when it
depends on a parameter even for a single material.

## Desorption Temperature

Desorption, as a thermodynamic property of a perfect and single-type surface,
might like boiling occur at a given temperature. In practice, there may be
kinetic limitations such that the desorption temperature occurs at much higher
ones, and even if thermodynamic the surface is not heterogeneous and so
different surface sites give up their atoms at different temperatures.
However, even the most elementary of models of surfaces, the Langmuir
adsorption isotherm, do not have a single boiling point. Assuming, and this is
valid under the case that the various thermodynamic parameters are constant
w.r.t. temperature, that the constant K varies as A0 e^{-E0/kT}, then clearly
where

y2/y1 = A0.e^{-E0/kT2}.p.(1 + A0.e^{-E0/kT1}.p) /
        [A0.e^{-E0/kT1}.p.(1 + A0.e^{-E0/kT2}.p)]

and

y2/y1 = K.p1.(1+K.p2)/[K.p2.(1+K.p1)]

show that the surface coverage is variable with the parameters. In effect, the
surface coverage is a composition variable, like that in a binary liquid
mixture such as ethanol and water.

# Physical Reasoning As Applied to Experimental Conditions

Though there is a great diversity in the adsorbent, the gas phase
adsorbates tend to be simple molecules, especially for testing purposes. The
question is then whether there are systematic trends. One certainly expects
that, e.g., the adsorption of hydrogen requires lower temperatures
(and higher pressures) than that of a cyclic organic compound. And that is
demonstrated in the table, which shows hydrogen adsorption is measured on average at 125 K
and 13.3 bar, while cyclohexane adsorption is measured on average at 365 K and 37 mbar.

One sees that low pressures are most often sampled. Low pressures, defined for
a given isotherm as low surface coverage fractions, make a kind of ideal limit
where there is only adsorbent-adsorbate interactions, and quantify the true
'heat of adsorption' (which is assumed constant in Langmuir isotherms, but
which can be made more negative by adsorbate-adsorbate interactions).

On average, pressure is varied in an isotherm over a factor of 2.4 times the
median value (this may not be symmetric, such that the maximum could be more
than 6/5 times the median value and the minimum less than 5/6 times the median
value). The mean value of pressure range is 5.3 bar. On average, and excluding
nonvarying cases, the temperature is varied over isotherms by a factor of
0.74, and the mean value of the temperature range is 95.75 Kelvin.

One sees that in the pressure-temperature space, there is a bivariate
distribution in which they are correlated (there is a diagonal): as one
increases temperature one generally increases pressure, too. This as one
expects (see theory section).

If one fits parameters, one has effectively a 'physical statistic': in fact,
the parameter in the langmuir adsorption isotherm is the inverse of the
pressure at which the surface coverage fraction is 1/2, a kind of 'physical
median'. This reduces the amount of general statistical calculation that has
to be done. However, this only works to the extent the function being fit can
be well-fit. Which isn't always the case. There is the advantage, though, that
determining these parameters allows data sets with differing y-variables to be
compared without making explicit conversions using material property data of
the adsorbent, especially ones that are hard to come by such as active surface
(which has to be measured, anyway, by adsorption techniques).

## Results for Parameter Fits

### Langmuir Isotherms

The Langmuir constant in found to vary between 3.6 mbar^-1 and thousands of
bar^-1 for those isotherms with meaningful fits. This isn't unexpected given
that for some adsorbent, adsorbate, and temperature, the pressure at which
there is 50% adsorption can vary over orders of magnitude (because the
chemical potential in the gas phase is logarithmic with pressure and linear
with temperature, see theory section).

### Freundlich Isotherm

It is found that exponents, when fits are valid, tend to be less than 1, and
they change significantly with temperature in the case of adsorbents and
adsorbates with several isotherms. There is no physical relationship as
precise as an equation expected for the Freundlich isotherm, unlike the
Langmuir parameter which has a Van't Hoff type relationship with temperature.
With increasing temperature, one expects the exponent to have some
non-monotonic trend where it is zero on either side, either because saturation
is independent of pressure at low temperatures or vacancy is independent of
pressure at high temperatures. This behavior being of no interest, however, is
most often not sampled.

# Data Source

NIST API for the isotherm database at https://adsorbents.nist.gov/isodb/api/.
The below i the version JSON for the API.

Version JSON:
{   "version": "3.4598",
    "major": "3",
    "minor": "4598",
    "date": "2019-02-06 10:39:57",
    "comment": "Isotherm Added"    }
