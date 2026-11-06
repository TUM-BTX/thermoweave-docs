# NRTL

NRTL (Non-Random Two-Liquid) is a native, differentiable liquid excess-Gibbs
model. It supplies activity coefficients, excess Gibbs energy, excess enthalpy
and excess heat capacity. Binary and multicomponent mixtures use the same code.
It works with ThermoWeave's VLE, LLE, SLE and ReducedHELD interfaces; SLLE also
requires a solid Gibbs-energy model and appropriate parameters.

NRTL is an empirical mixture model: specify interaction parameters for your
component pairs or load available pairs from the bundled collection. SMILES
alone do not determine NRTL coefficients. It supplies no density, volume or
PVT equation of state; use SAFT for those properties.

## Install and calculate

The standard `environment.yml` includes NRTL. In an existing environment,
run from the ThermoWeave checkout:

```text
python -m pip install -e ".[nrtl]"
```

JAX CPU support determines the supported platforms, as for SAFT; see
[installation](../installation.md#choose-your-platform). Julia, COSMO files
and external model engines are not required.

```python
import numpy as np
from thermoweave import NRTL

model = NRTL.from_database(["water", "ethanol"])
T, x = 298.15, [0.4, 0.6]
print(model.a, model.b, model.alpha, model.reference)
print(model.ln_activity_coefficients(T, x))  # [0.47780840, 0.13717350]
print(model.activities(T, x))
print(model.reduced_excess_gibbs(T, x))      # gE/(RT)
print(model.excess_enthalpy(T, x))           # J/mol
print(model.excess_heat_capacity(T, x))      # J/(mol K)

X = np.array([[0.2, 0.8], [0.5, 0.5], [0.8, 0.2]])
print(model.ln_activity_coefficients_batch(T, X))
# A temperature per row is also supported:
print(model.ln_activity_coefficients_batch([290., 300., 310.], X))
```

`pressure_Pa` is accepted by the activity API for compatibility and has no
influence on this pressure-independent gE model. Activities use pure-liquid
standard states. The first evaluation compiles JAX kernels.

## Equations and matrix conventions

ThermoWeave follows the directed convention used by
[Clapeyron's NRTL implementation](https://github.com/ClapeyronThermo/Clapeyron.jl/blob/cb620c1af72b7bcea8407e4f970dbae64a7f8c9d/src/models/Activity/NRTL/NRTL.jl):

$$\tau_{ij}=a_{ij}+b_{ij}/T+l_{ij}\ln(T/\mathrm{K})+d_{ij}T,$$
$$\alpha_{ij}(T)=\alpha^0_{ij}+e_{ij}T,\qquad
G_{ij}=\exp[-\alpha_{ij}(T)\tau_{ij}].$$

The original a+b/T convention is recovered by the default zero values of
`tau_log` (l), `tau_linear` (d) and `alpha_linear` (e). This preserves existing
parameter sets. These extensions also support the full
[SPT-NRTL prediction collection](spt-nrtl.md).

$$D_i=\sum_j x_jG_{ji},\qquad
q_i=\frac{\sum_j x_j\tau_{ji}G_{ji}}{D_i},\qquad
\frac{g^E}{RT}=\sum_i x_iq_i,$$

$$\ln\gamma_i=q_i+\sum_j\frac{x_jG_{ij}}{D_j}(\tau_{ij}-q_j).$$

Component order is the order in `components`. `a[i,j]` and `b[i,j]` are directed;
the opposite direction is a separate parameter. **Do not transpose matrices
when importing Clapeyron a/b data.** `a`, `tau_log` and the `alpha` intercept are dimensionless; **b is in
kelvin**, T is in K. `tau_linear` and `alpha_linear` have units 1/K. Energy-valued parameters from other software must first be
converted to this exact convention. A common choice is symmetric, fixed
`alpha=0.3`; explicit matrices also permit directed alpha. Evaluation checks
that the effective alpha(T) remains nonnegative.

```python
model = NRTL(
    ["water", "ethanol"],
    a=[[0., 3.458], [-0.801, 0.]],
    b=[[0., -586.1], [246.2, 0.]],
    alpha=0.3,
)
```

All tau-coefficient diagonals must be zero. A scalar fills off-diagonal entries with zero
diagonals. `c` aliases `alpha`; specify one of them. `tau` aliases a constant a
matrix with the other tau terms zero and cannot be combined with explicit tau coefficients. Parameters are copied and
read-only: use `model.with_parameters(a=..., b=..., tau_log=..., tau_linear=..., alpha=..., alpha_linear=...)` for a new model.

The bundled CSV is a snapshot of the
[Clapeyron NRTL collection](https://github.com/ClapeyronThermo/Clapeyron.jl/blob/cb620c1af72b7bcea8407e4f970dbae64a7f8c9d/database/Activity/NRTL/NRTL_unlike.csv).
It retains the table's aliases and is available offline. The upstream `source`
column is empty for all 32 binary pairs; original per-pair citations and
temperature validity limits are unknown. `model.reference` identifies the
source table, and `model.metadata` records these gaps explicitly. Every
directed pair must exist; missing pairs raise an error. Some source pairs list
different nonrandomness coefficients in opposite directions. Loading these
requires an explicit `alpha=` choice after checking the source; the loader
does not silently select one. Combining binary fits into a ternary model is
an assumption to validate against mixture data, not a guaranteed prediction.

## Derivatives and JAX performance

Public methods return NumPy values and evaluate in a scoped float64 context,
without changing the caller's global JAX precision setting. Closed-form
activity kernels are shared across models, compiled once per array shape and
dtype, and vectorized across composition/temperature rows. At a fixed T the
model caches temperature terms, avoiding their reconstruction during flashes.
Column scaling of G cancels analytically in the ratios and reduces exponential
overflow. Extreme parameters that still produce nonfinite results raise an
error rather than being silently clipped.

- `ln_activity_coefficients_jacobian(T, x)` returns
  $\partial\ln\gamma_i/\partial n_j$ at unit total amount, consistent with SAFT.
- `ln_activity_coefficients_temperature_derivative(T, x)` holds x fixed.
- $H^E=-RT^2\partial(g^E/RT)/\partial T$ and
  $C_p^E=-R[2T\partial(g^E/RT)/\partial T+T^2\partial^2(g^E/RT)/\partial T^2]$.

For an entire calculation inside JAX, call `thermoweave.nrtl.kernels` directly:

```python
import jax
import jax.numpy as jnp
from thermoweave.nrtl.kernels import NRTLParameters, ln_activity_coefficients

jax.config.update("jax_enable_x64", True)  # set once before tracing your code
params = NRTLParameters(jnp.asarray(model.a), jnp.asarray(model.b),
                        jnp.asarray(model.alpha))
compiled = jax.jit(ln_activity_coefficients)
lng = compiled(params, 298.15, jnp.array([0.4, 0.6]))
```

The kernels accept normalized fractions or nonnegative amounts with positive
total; validate these before tracing. The public interface validates mole
fractions. Use the pure kernels rather than the NumPy wrapper inside `jit`,
`grad` or `vmap`. Fit residuals and their exact parameter Jacobians are JIT
compiled and batched; SciPy only manages the outer bounded least-squares steps.

## Choosing temperature complexity

The extra terms preserve imported SPT predictions exactly and can improve
fits when data span a sufficiently broad temperature interval. More free terms
do not automatically improve physical accuracy or extrapolation. For your own
regressions, start with a+b/T and fixed alpha, add terms only when independent
validation and caloric data support them, and inspect parameter correlations.
The [fitting guide](../advanced/nrtl-fitting.md) explains identifiability checks.

## Fit and save parameters

Use `fit_nrtl` for ln-gamma arrays or `NRTLFitProblem` for selected coefficients
and mixed property datasets. See the [fitting guide](../advanced/nrtl-fitting.md)
and [notebook 13](../notebooks/13_nrtl_and_parameter_fitting.ipynb), which evaluates
water/ethanol NRTL, calculates VLE and fits a compact NRTL representation of
actual SAFT predictions.

```python
model.to_json("water-ethanol-nrtl.json")
reloaded = NRTL.from_json("water-ethanol-nrtl.json")
```

The self-contained v2 JSON stores the ordered names, all six coefficient
matrices, convention schema, reference and metadata. Existing v1 JSON files
remain loadable with zero-valued extensions. Keep the data source and fit validation with your results.

The formulation is due to [Renon and Prausnitz (1968)](https://doi.org/10.1002/aic.690140124).
Clapeyron's MIT notice is preserved in [third-party notices](../third-party-notices.md).
