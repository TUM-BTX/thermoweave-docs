# Calculation tutorials

Read the notebooks directly on this site, including their saved figures and
outputs. Each notebook page includes its source download so you can run it
locally after [installation](installation.md). The site build **does not execute**
notebooks or download external data.

## Solid–liquid–liquid equilibrium

| Calculation | Notebook | Additional inputs |
|---|---|---|
| Binary benzene/water SAFT: SLE/LLE boundaries and invariant temperature | [10 · Binary SLLE](notebooks/10_binary_slle_saft.ipynb) | Bundled SAFT parameters; cited benzene fusion data |
| Ternary benzene/water/ethanol SAFT: phase amounts, tie triangle, phase survey | [11 · Ternary SLLE](notebooks/11_ternary_slle_saft.ipynb) | Same standalone SAFT setup |
| Binary and ternary benzene/water/ethanol COSMO-RS SLLE | [12 · COSMO-RS SLLE](notebooks/12_binary_ternary_slle_cosmors.ipynb) | Compatible backend, conformers and parametrization |

The examples use measured benzene fusion properties and explicitly identify
model parameters. Their solid model is pure benzene(s), constant fusion
enthalpy and ΔCp=0, above the other components' melting temperatures. Results
are model predictions, not a demonstration of agreement with measured SLLE.

## Main course

| Notebook | What you learn |
|---|---|
| [00 · Quickstart](notebooks/00_quickstart_and_units.ipynb) | Model construction, units and a first EOS evaluation |
| [01 · Activities and gE](notebooks/01_excess_gibbs_models.ipynb) | Real SAFT activity and excess-Gibbs curves |
| [02 · Molecules](notebooks/02_saft_molecules_and_groups.ipynb) | Automatic/manual groups and parameter coverage |
| [03 · EOS properties](notebooks/03_saft_eos_properties.ipynb) | Density, volume, pressure and fugacity |
| [04 · Derivatives](notebooks/04_derivatives_and_response_functions.ipynb) | Enthalpy, response functions and KB integrals |
| [05 · VLE](notebooks/05_vapour_liquid_equilibrium.ipynb) | Water/ethanol with SAFT activities and saturation pressures |
| [06 · Stability and LLE](notebooks/06_liquid_stability_and_flash.ipynb) | Benzene/water stability and liquid splitting |
| [07 · SLE](notebooks/07_solubility_and_solid_liquid_flash.ipynb) | Benzene solubility and liquid/solid flash |
| [08 · Fitting](notebooks/08_parameter_fitting_and_evaluation.ipynb) | Actual SAFT parameter fitting with labelled synthetic recovery targets |
| [13 · NRTL and fitting](notebooks/13_nrtl_and_parameter_fitting.ipynb) | Water/ethanol NRTL, VLE and fitting to actual SAFT predictions with held-out validation |
| [09 · External models](notebooks/09_cosmors_and_hanna.ipynb) | Actual COSMO-RS activities and optional HANNA setup |

Notebooks are independent; run each from its first cell. When downloading an
individual notebook, keep it inside a checkout's `tutorials/` folder, or download
its [_support.py](notebooks/_support.py) and
[data/real_mixtures.json](notebooks/data/real_mixtures.json) companions. Keep the
JSON file in a `data/` subfolder beside the notebook.
The read-only web pages need no Python environment.

## Optional analytic theory examples

These explain custom interfaces using explicitly synthetic models; they are
separate from the actual-model application course:

- [Custom activity model](notebooks/theory/custom_activity_models.ipynb).
- [Reactive/electrolyte illustration](notebooks/theory/synthetic_reactive_electrolytes.ipynb).
