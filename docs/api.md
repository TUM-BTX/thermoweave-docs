# API guide

## Shared conventions

- Temperature: K. Pressure: Pa. Energy: J/mol unless explicitly dimensionless.
- `x`: all component mole fractions, in insertion order, nonnegative, sum 1.
- `ln_activity_coefficients`: natural logarithms, not γ and not log10.
- `reduced_excess_gibbs` / `reduced_mixing_gibbs`: molar energy divided by RT.
- SAFT density: **molar** density in mol/m³. `Vm = 1/rho` gives m³/mol.
- SAFT activity coefficients: pure-liquid standard state at the same T and P.
- `phase="liquid"` or `phase="vapor"` chooses a density branch; it does not
  establish the globally stable phase assemblage.

## Models

```python
from thermoweave import ThermodynamicModel, SAFTgammaMie, NRTL, CosmoRSModel, HannaModel
from thermoweave.saft import GroupDatabase, assign_groups, missing_interactions
```

`SAFTgammaMie(components, pressure_Pa=..., database=...)` accepts names mapped
to SMILES or manual group dictionaries. `from_smiles` is a convenience constructor.
`add_component(name, groups_or_smiles)` extends it. `groups` exposes counts;
`assignments[name].describe()` retrieves an automatic assignment report.
`report_assignment=False` silences reports. Database extensions are explicit:
`GroupDatabase.default("wehbe2023", "tenberg2025")`.

| Calculation | Call |
|---|---|
| Molar density | `model.density(T, x, pressure_Pa=P, phase="liquid")` |
| Pressure at density | `model.pressure(T, x, rho)` |
| Fugacity coefficients | `model.ln_fugacity_coefficients(T, x, P, phase="vapor")` |
| Activities | `model.activities(T, x)` |
| Batch activity coefficients | `model.ln_activity_coefficients_batch(T, X)` |
| Composition Jacobian | `model.ln_activity_coefficients_jacobian(T, x)` |
| Residual Helmholtz energy | `model.residual_helmholtz(T, x, rho)` |
| Monomer/chain/association parts | `model.residual_helmholtz_contributions(T, x, rho)` |
| Helmholtz derivatives | `model.residual_helmholtz_derivatives(T, x, rho)` |
| Unbonded site fractions | `model.non_bonded_site_fractions(T, x, rho)` |
| KB integrals/response data | `model.kirkwood_buff_integrals(T, x)` |

The KB result contains `G` and `partial_volumes` in cm³/mol, `V` in cm³/mol,
and `kappa_T` in 1/GPa. Core EOS methods use SI. No separate `molar_volume`
method is required. Temperature derivatives and caloric residual/excess
quantities can be built with the differentiable `thermoweave.saft.kernels`;
notebook 04 gives the exact formulas. Absolute enthalpy/heat capacity also
needs an ideal-gas reference model, which is not supplied automatically.

## NRTL activity model

`NRTL(components, a=..., b=..., alpha=0.3)` uses directed
`tau=a+b/T+tau_log*ln(T/K)+tau_linear*T` and `alpha(T)=alpha+alpha_linear*T`.
Extension coefficients default to zero; b is in K and both linear slopes are in 1/K. `NRTL.from_database(names)` loads
available directed pairs from a pinned Clapeyron snapshot. It supplies the
shared activity/batch/energy API and exact composition/temperature derivatives,
`excess_enthalpy` (J/mol), `excess_heat_capacity` (J/(mol K)) and JSON save/load.
The batch API accepts a scalar temperature or one value per row.
`NRTL.from_spt({"water": "O", "ethanol": "CCO"})` loads full
[SPT-NRTL predictions](models/spt-nrtl.md) with verified caching and metadata.
`interaction_parameters(T)` returns effective tau and alpha matrices. JSON v2
stores every coefficient; legacy v1 files remain readable.
See [the model guide](models/nrtl.md) for complete conventions.

```python
from thermoweave.nrtl import NRTLFitProblem, NRTLFitResult, fit_nrtl, SPTNRTLDatabase
```

The [fitting guide](advanced/nrtl-fitting.md) documents mixed property data,
selected parameters, bounds, weights and identifiability diagnostics.

## Equilibrium and evaluation

```python
from thermoweave import tpd_stability, solve_binary_lle, CEMSettings, solve_cem
from thermoweave.equilibrium.vle import bubble_pressure, dew_pressure
from thermoweave.equilibrium.sle import solubility, dissolution_temperature
from thermoweave.equilibrium.reduced_held import ReducedChart, ReducedHELD, Solid
from thermoweave.saft.fitting import FitProblem
from thermoweave.evaluation.metrics import mae, rmse, r_squared
```

Equilibrium APIs predate a single argument-order convention. Follow the calls
in notebooks 05–08 or inspect each function's docstring. In particular,
`tpd_stability(model, z, T)` and `solubility(model, solute_index, T, fusion)`
have different argument order. Solvers that do not accept pressure use the
SAFT model's configured pressure.
