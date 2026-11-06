# COSMO-RS and learned models

An activity model need not start from a small empirical pair-parameter table.
COSMO-RS uses quantum-chemical surface information; learned models use molecular
representations and thermodynamic structure. Their predictions can enter the
same [liquid activity interface](excess-gibbs.md), while their required inputs
and validation domains remain different.

## COSMO surface information

A COSMO quantum-chemical calculation places a molecule in a conducting
continuum. The resulting screening charge on its cavity surface is divided
into small surface segments with charge density sigma. A sigma profile
summarizes how much surface area occurs at each charge density; molecular
size and other surface descriptors also enter the parametrization.

A profile records surface polarity information that is unavailable from a
simple molecular formula. Geometry, conformer selection, quantum-chemical
method, cavity construction and parameter set all affect the input. A SMILES
string alone is not a substitute for these computed surface files in the
ThermoWeave COSMO-RS workflow.

## From surface contacts to chemical potentials

COSMO-RS describes interactions between contacting surface segments. Its
physical terms include electrostatic misfit and hydrogen bonding, with
additional contributions depending on the implementation and parametrization.
The electrostatic mismatch has a schematic dependence

$$E_{\mathrm{misfit}}(\sigma,\sigma')\propto(\sigma+\sigma')^2.$$

Opposite screening charges can complement one another; an unmatched surface
charge costs energy. Hydrogen-bond donor/acceptor conditions introduce further
selective contacts. A self-consistent statistical treatment of contacts in
the mixture determines segment chemical potentials, which are integrated over
molecular surfaces. Combinatorial size/shape and conformer contributions
complete the model's chemical potentials.

This is the physical route introduced by
[Klamt (1995)](https://doi.org/10.1021/j100007a062) and developed in
[Klamt, Jonas, Bürger and Lohrenz (1998)](https://doi.org/10.1021/jp980017s).
Exact contact-energy expressions and parameters belong to the chosen backend;
coefficients from different COSMO variants are not automatically interchangeable.

For pure-liquid references, molecular chemical-potential differences give

$$\ln\gamma_i=
\frac{\mu_i^{\mathrm{mix}}-\mu_i^{\mathrm{pure}}}{RT}-\ln x_i.$$

The subtraction must use a consistent standard state and compatible molecular
inputs. Neutral-mixture activities and ionic reference conventions require
different care; see the supported assumptions in [capabilities](../capabilities.md).

## Learned excess-Gibbs functions

A neural network can predict an unconstrained activity curve, or it can be
constructed around thermodynamic structure. [HANNA](https://doi.org/10.1039/D4SC05115G)
uses a constrained excess-Gibbs function and obtains activity coefficients
through differentiation. This imposes reference and Gibbs–Duhem consistency
through the architecture. The published model is developed and tested on
binary-mixture activity data; the predictor assets and their domain determine
what a particular adapter can meaningfully evaluate.

Consistency removes a class of thermodynamic contradictions. Prediction error,
chemical coverage and extrapolation still need independent validation.

## Learned parameters of a physical model

SPT-NRTL follows another route: a learned molecular representation outputs the
coefficients of an explicit NRTL function. Composition and temperature then
enter that thermodynamic model. Once a coefficient set is obtained, an NRTL
implementation can evaluate its properties without running the neural network.
The [NRTL chapter](nrtl.md) explains its full temperature dependence and the
provenance of the published parameter collection.

## Match the input to the model

| Approach | Molecular information | Thermodynamic representation |
|---|---|---|
| COSMO-RS | COSMO surfaces, conformer information, parametrization | Statistical surface-contact model |
| HANNA | Molecular representations and trained assets | Constrained learned gE |
| SPT-NRTL | Molecular representations; published tables can be looked up by SMILES | Learned NRTL coefficients |

These gE routes supply liquid nonideality. They do not supply a general
pressure–volume EoS or the solid reference data needed for SLE/SLLE.

**Use in Python:** [openCOSMO-RS setup](../models/opencosmors.md),
[HANNA setup](../models/hanna.md),
[SPT collection](../models/spt-nrtl.md) and
[notebook 09](../notebooks/09_cosmors_and_hanna.ipynb).
