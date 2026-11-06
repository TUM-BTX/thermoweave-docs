# Practical guide

Use ThermoWeave to define a mixture, choose a model and run a calculation.
Start with installation if this is your first session, or choose the relevant
model and workflow below. For the physical derivations, use [Theory](../theory.md).

## First steps

1. [Install ThermoWeave](../installation.md) in the named Conda environment.
   The guide covers Linux, macOS and Windows, including optional backend builds.
2. Activate `thermoweave` in your terminal or select its Jupyter kernel.
   Your scripts can live in any project folder.
3. Run the [quickstart notebook](../notebooks/00_quickstart_and_units.ipynb),
   or follow the [calculation recipes](calculations.md).

## Choose a model

| You need | Model | Required inputs |
|---|---|---|
| Density, volume, pressure, fugacity and liquid activities | [SAFT-γ Mie](../models/saft-gamma-mie.md) | Functional groups or SMILES, group parameters, T/P |
| Empirical liquid nonideality with fitted pair coefficients | [NRTL](../models/nrtl.md) | Ordered components and directed interaction parameters |
| Tabulated machine-learning predictions in NRTL form | [SPT-NRTL](../models/spt-nrtl.md) | Component SMILES; cached or downloaded SPT tables |
| Liquid activities from molecular surface interactions | [openCOSMO-RS](../models/opencosmors.md) | Compiled backend, compatible COSMO conformers and parametrization |
| Liquid activities from a learned excess-Gibbs model | [HANNA](../models/hanna.md) | External predictor, dependencies and model assets |

A shared activity interface lets the liquid models use common equilibrium
routines. An activity model alone supplies no density/volume EoS. See the
[theoretical distinction](../theory/excess-gibbs.md#what-a-ge-model-supplies)
when choosing which properties to request.

## Choose a calculation

The [calculation guide](calculations.md) gives executable recipes and units.
For longer workflows, use the independent notebooks:

| Calculation | Start here |
|---|---|
| Activities and mixing/excess Gibbs energy | [01 · Activities](../notebooks/01_excess_gibbs_models.ipynb) |
| EoS pressure, density and volume | [03 · EoS properties](../notebooks/03_saft_eos_properties.ipynb) |
| Derivatives and response functions | [04 · Derivatives](../notebooks/04_derivatives_and_response_functions.ipynb) |
| Bubble/dew pressure and temperature | [05 · VLE](../notebooks/05_vapour_liquid_equilibrium.ipynb) |
| Stability and liquid splitting | [06 · LLE](../notebooks/06_liquid_stability_and_flash.ipynb) |
| Solubility and liquid/solid flash | [07 · SLE](../notebooks/07_solubility_and_solid_liquid_flash.ipynb) |
| Binary and ternary SLLE | [10–12 · SLLE workflows](../tutorials.md#solidliquidliquid-equilibrium) |
| NRTL, VLE and fitting | [13 · NRTL](../notebooks/13_nrtl_and_parameter_fitting.ipynb) |
| SPT collection, temperature functions and offline use | [14 · SPT-NRTL](../notebooks/14_spt_nrtl_parameters.ipynb) |

## Parameters, fitting and validation

[SAFT fitting](../notebooks/08_parameter_fitting_and_evaluation.ipynb),
[NRTL fitting](../advanced/nrtl-fitting.md) and
[COSMO-RS parametrization](../advanced/parametrization.md) expose different
parameterizations through their respective model interfaces. Keep data sources,
units, temperature coverage, fit objectives and independent validation with the
resulting parameter set. The [corpus tools](../advanced/production-evaluation.md)
help evaluate larger collections of experimental records.

For each calculation, record model parameters and component order, inspect
solver diagnostics and check material balances. Read [API and units](../api.md)
for exact signatures and [capabilities](../capabilities.md) for supported
assumptions. Numerical convergence and agreement with measured data answer
different questions.
