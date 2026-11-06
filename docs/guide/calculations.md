# Run calculations

These recipes show the Python calls behind the main workflows. Run them in an
activated ThermoWeave environment after [installation](../installation.md).
Temperatures are in K, pressures in Pa, energies in J/mol and compositions are
full mole-fraction vectors in component order.

## Calculate density, volume and pressure

Build a SAFT-γ Mie model from SMILES and select a liquid branch:

```python
from thermoweave import SAFTgammaMie

model = SAFTgammaMie.from_smiles(
    {"water": "O", "ethanol": "CCO"}, pressure_Pa=101325.0
)
T, x = 298.15, [0.8, 0.2]
rho = model.density(T, x)              # mol/m³
Vm = 1.0 / rho                        # m³/mol
P_check = model.pressure(T, x, rho)    # Pa
print(rho, Vm, P_check)
```

The assignment report lists groups and atom matches. Inspect it before using
the molecule. Manual group definitions are an option in the
[SAFT setup guide](../models/saft-gamma-mie.md). A density root selects a branch;
use an equilibrium calculation to establish phase coexistence.
The [EoS theory chapter](../theory/equations-of-state.md) derives the pressure
relation. [Notebook 03](../notebooks/03_saft_eos_properties.ipynb) covers both
liquid and vapour roots.

## Calculate activities and excess properties

For an NRTL calculation, load available pair parameters or supply explicit
matrices. The following example needs JAX but no external COSMO files:

```python
import numpy as np
from thermoweave import NRTL

model = NRTL.from_database(["water", "ethanol"])
T, x = 298.15, [0.4, 0.6]
ln_gamma = model.ln_activity_coefficients(T, x)
gamma = np.exp(ln_gamma)
activities = model.activities(T, x)
gE_over_RT = model.reduced_excess_gibbs(T, x)
HE = model.excess_enthalpy(T, x)              # J/mol
CpE = model.excess_heat_capacity(T, x)        # J/(mol K)
print(gamma, activities, gE_over_RT, HE, CpE)
```

`ln_activity_coefficients` returns natural logarithms. Model input conventions
and parameter sources are documented in the [NRTL guide](../models/nrtl.md);
[NRTL theory](../theory/nrtl.md) explains the equations and temperature terms.

For SPT predictions use `NRTL.from_spt({"water": "O", "ethanol": "CCO"})`.
The [SPT guide](../models/spt-nrtl.md) explains download/cache settings,
provenance, offline use and unknown validity ranges. COSMO-RS and HANNA use the
same activity interface after their separate model setup.

## Evaluate a composition grid

Use the model's batch API to reduce Python overhead:

```python
xs = np.linspace(0.05, 0.95, 50)
X = np.column_stack([xs, 1.0-xs])
ln_gamma_grid = model.ln_activity_coefficients_batch(T, X)
```

NRTL and SAFT accept a scalar T or one T per row. The first JAX evaluation
includes compilation; subsequent calls of the same shape reuse compiled
kernels. Keep a model object for repeated calculations. Public methods validate
inputs and return NumPy values. For differentiation inside your own `jit` or
`grad`, use the model's pure JAX kernels as described in its model guide.

## Compute a bubble pressure

Continue with the water/ethanol NRTL model above. Supply pure saturation
pressures at the same temperature:

```python
from thermoweave.equilibrium.vle import bubble_pressure

# Illustrative supplied values at 298.15 K, in model component order.
psat_Pa = np.array([3169.0, 7870.0])
result = bubble_pressure(model, x, T, psat_Pa)
print(result.pressure_Pa)
print(result.vapor_composition)
```

This convenience solver assumes ideal vapour and neglects the Poynting
correction. Saturation pressures are independent inputs. For cited Antoine
correlations with explicit temperature intervals, use
[notebook 05](../notebooks/05_vapour_liquid_equilibrium.ipynb) or
[13](../notebooks/13_nrtl_and_parameter_fitting.ipynb).
The [phase-equilibrium chapter](../theory/phase-equilibria.md#vapourliquid-equilibrium)
explains the underlying modified Raoult law.

## Calculate solubility and SLLE

A pure-solid SLE calculation also needs melting data. For benzene/water:

```python
from thermoweave import FusionProperties, SAFTgammaMie
from thermoweave.equilibrium.sle import solubility

benzene_water = SAFTgammaMie.from_smiles(
    {"benzene": "c1ccccc1", "water": "O"}, pressure_Pa=101325.0
)
fusion = FusionProperties(
    melting_temperature_K=278.69,
    enthalpy_of_fusion_J_mol=9866.3,
)
saturation = solubility(benzene_water, 0, 275.0, fusion)
print(saturation.composition)
```

The fusion values are the selected benzene values cited in the tutorial's
[NIST source](https://webbook.nist.gov/cgi/cbook.cgi?ID=C71432&Mask=4).
This calculation uses a pure solid and constant fusion enthalpy, ΔCp=0. A
solubility root alone does not select the stable assemblage when a liquid split
or competing solid is possible.

For coupled SLLE use [notebook 10](../notebooks/10_binary_slle_saft.ipynb) for a
binary invariant and [11](../notebooks/11_ternary_slle_saft.ipynb) for a ternary
tie triangle. [Notebook 12](../notebooks/12_binary_ternary_slle_cosmors.ipynb)
uses the real COSMO-RS backend. These workflows explicitly define the liquid
model, solid Gibbs energy, feed and solver precision, then check phase amounts,
material balances, isoactivity and solid saturation.

## Fit, save and reproduce

[NRTLFitProblem](../advanced/nrtl-fitting.md) selects coefficients and combines
activity, VLE, enthalpy and tie-line measurements with exact JAX Jacobians.
Start with a small identifiable parameter set and keep validation data apart
from fitting data. [Notebook 13](../notebooks/13_nrtl_and_parameter_fitting.ipynb)
contains a complete fit with held-out checks.

```python
model.to_json("water-ethanol-nrtl.json")
restored = NRTL.from_json("water-ethanol-nrtl.json")
```

The JSON stores component order, all temperature coefficients and available
provenance. Keep experimental records and validation results with your project.
See [API and units](../api.md) for other entry points and
[derivative theory](../theory/derivatives.md) for interpretation of the returned
caloric and response quantities.
