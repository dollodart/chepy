# Description

This directory contains data, processing, and visualizations I found useful
during my graduate research in chemical engineering. It is not a package but a
collection of scripts. However, some scripts are used as modules to other ones,
in which case they have been defined to allow one to import from anywhere.  

There is no standard for processing data with dimensions and units. Here, I
either specify the units in the accompanying text, or directly in the column
name. One can use any of the many existing data structure for arrays, or lists
of arrays, that specifies dimensionality and units in addition to numbers. But
I have simply used pandas dataframes with float arrays because the purpose here
isn't to perform operations between quantities which requires dimensional
consistency, but only to look at distributions and correlations, and the
reported units are often most convenient.

The minimum quality level for inclusion is that a script produces some data
visualization or processing on the input data. This is a low bar because
superior plots are available in the literature, sometimes even on Wikipedia,
but there is some advantage in having the data in machine readable form to do
calculations on. Some scripts merely visualize a geometric sequence as a plot.
Others calculate statistics, evaluate integrals, or do some other computations
on the input data.

For the most part, these scripts demonstrate the application of basic
statistical reasoning in either purely empirical or mixed theoretical and
empirical models for the purpose of prediction or design.

## License

I have tried to cite all data sources but in some cases have lost the original
reference materials (such cases tend to be small amounts of data readily
available on the internet by search). There is no license and it cannot be
licensed because it makes use of copyrighted data. You must comply with any of
the original copyrights should you try to extend these scripts in your own
applications.

# Dependencies

This package extensively uses numpy, scipy, pandas, and matplotlib which are
not standard library but considered core numerical and scientific computing. It
also uses thermo, ase, and pubchempy, though those packages are usually
separated into different scripts from the main one.

## Code Redundancy using APIs

These libraries are already high-level, to an extent that can be questioned as
good practice, such as plot methods for the DataFrame class. Much of the code
in these scripts is redundant because it achieves the same goal, e.g.,
determining if an array makes a geometric sequence. But building a utility API
that do little or nothing more than take inputs and place them into inputs of
another high-level API function appears unnecessary. The only advantage it
gives is that a change to a common source of those utilities would uniformly
change all uses of it, but given the scripts are for the most part standalone,
this advantage is not great. This is the justification for redundant code.

The analysis is ad hoc. What might be done is a systematic and exhaustive
analysis, by consideration of combinatorics.  That is, look into the
distribution of every variable (or its logarithm), and the correlation between
every pair of variables (or the logarithms thereof), with linear regression
done between interesting pairs. In some cases it is done, for example, by using
the pandas.DataFrame.corr method. But each variable has a different physical
significance, many pairs are not interesting even if they have strong
correlations, some pairs are interesting even if they have noisy correlations,
some relationships are neither linear nor power law, and so forth. An ad hoc
approach is useful when one comes in knowing the relationships, usually derived
from physical models, expected between the variables.

# Scientific Python Packages

Some packages which I found useful for research problems, though only a small
number are used here:

For atomistic data including structure:
  - ase.data and ase.neighborlist modules of the ase package, among the very many other useful modules of this package.
  - molmod (the data modules) from the Center for Molecular Modeling.
  - pymatgen, for querying the database of the Materials Project.
  - mendeleev by Lukasz Mentel.
  - pubchempy package from Matt Swain, python interface to the PubChem API.
For unit conversions and calculations with physical quantities:
  - pymatgen.core.units module of the pymatgen package.
  - python-quantities by Darren Dale et al.
  - brian2 by Marcel Stimberg et al.
For thermodynamic data:
  - thermo package from Caleb Bell, has extensive property data and convenient
    methods. Dependencies on some of the author packages in the author's
    Chemical Engineering Design Library, including fluids (modeling fluid dynamics)
    and chemicals (which has most of the thermodynamic data). External C++ library dependency (through python binding) on CoolProp.
  - pyro by Prof. Christopher Martin.
For spectroscopic data processing:
  - Radis by Erwan Pannier et al.
  - rampy by Charles Le Losq et al.
  - chemplexity by James Dillon.
General chemistry modeling
  - ChemPy package from Bjoern Dahlgren, has general solution to the problem of
    equilibria and kinetics, and some thermodynamic data for water. The author
    has several other packages for numerical computing and chemistry applications.
  - ChemPy package from J W Allen, has molecular structure property
    calculations, rate constant fitting, rate equation evaluation, and
    thermodynamic data evaluation, all for molecular scale analysis.
  - Reaktoro package by Allan Leal (C++ library with Python binding). A formulation of equilibrium as a
    minimization of Gibb's free energy, rather than as non-linear system of
    equations which have fundamental thermodynamic variables implicit in rate
    constants (which is what ChemPy by Dahlgren formulates reaction equilibria as, solving
    the nonlinear symbolic equations using its own pyneqsys).
Big, multipurpose libraries:
  - RDKit, for biological applications but there are many useful utilities for
    the more general computational chemist, including structure parsing and
    atom type/functional group classification in its GraphMol sublibrary (C++ library).
  - Cantera, actively community maintained with financial support by NUMFocus,
    has data and processing like in thermo and ChemPy but fuller featured (C++ library).

Some notes:
- I found the thermo package stating that the vapor pressure of silver is 1.e-5
  Pa at 1217 K, when it is ~1.e-2 torr at that temperature. Care should be
  taken in interpreting these results. It appears the thermo package is more for
  vapor-liquid and other conventional chemical engineering and chemistry
  applications.
- There is also the ChemPy package by Jan Rybizki, which is for astrophysics.
- Throughout these scripts there is the common, though incorrect, definition of
  axis labels in logarithmic plots as merely that variable such as 'x', letting
the logarithmic scale on the axis imply that the logarithm is taken. Of course,
what is plotted is the logarithm of the quantity, so the label is more
correctly 'log(x)' .

# Further Development

There are several modules which are erroneous, or sufficiently incomplete as
to not be included in here. They may at some time be added. There is no
guarantee of correctness for what is at this time published. Please report
errors in the issues. Note some errors are already known and stated in the
readmes or commit log.
