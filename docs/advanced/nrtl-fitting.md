# Fit NRTL parameters

The NRTL helpers fit bounded interaction coefficients with vectorized JAX
residuals and exact AD parameter Jacobians. They return the fitted model,
residuals, Jacobian, rank/condition diagnostics, local covariance and a report.
There is no finite-difference parameter Jacobian in the optimizer.

## Start with ln-gamma data

Given `T` (a scalar or one temperature per row), `X` (M×N full liquid mole
fractions) and measured `ln_gamma` (M×N natural logarithms):

```python
from thermoweave import NRTL
from thermoweave.nrtl import fit_nrtl

initial = NRTL(["water", "ethanol"], a=0., alpha=0.3)
result = fit_nrtl(initial, T, X, ln_gamma, fit_parameters=("a",))
print(result.report())
if not result.success:
    raise RuntimeError(result.message)
fitted = result.model
result.save("fitted-nrtl.json")
```

This fits both directed off-diagonal a entries. Alpha stays fixed by default.
`fit_parameters=("a", "b")` fits both temperature terms; `fit_alpha=True`
adds one shared alpha value per unordered pair. For individual entries,
custom bounds or multiple data types, build a problem explicitly.

## Select parameters and combine datasets

```python
from thermoweave.nrtl import NRTLFitProblem

problem = NRTLFitProblem(initial)
problem.vary("a", "water", "ethanol", bounds=(-5., 10.))
problem.vary("a", "ethanol", "water", bounds=(-5., 10.))
problem.vary("b", "water", "ethanol", bounds=(-3000., 3000.))
problem.vary("b", "ethanol", "water", bounds=(-3000., 3000.))
problem.add_ln_gamma(T, X, ln_gamma, label="activity measurements")
# Optional additional measurements, with their own T and X grids:
problem.add_excess_enthalpy(T_H, X_H, H_E_J_mol, weight=10., label="calorimetry")
result = problem.fit(starts=4, seed=0, max_nfev=1000)
```

Names or zero-based indices select entries. a/b remain directed. To fit one
nonrandomness value in both directions, use
`problem.vary("alpha", 0, 1, bounds=(0.1, 0.6), symmetric=True)`.
If the initial two directions differ, also supply `start=` explicitly.
Defaults are a∈[−20,20], b∈[−20000,20000] K, alpha∈[0,1]; choose bounds
appropriate to your chemistry and temperature range. `start=` overrides the
model's initial entry. Multistart uses seeded uniform samples inside finite
bounds; it is an optimization aid, not a global-optimum guarantee.

| Dataset method | Inputs / assumption | Residual before weighting |
|---|---|---|
| `add_ln_gamma(T, X, ln_gamma)` | Natural logarithms; optional `component=` for an M-vector of a single species | predicted − observed ln γ |
| `add_activity_coefficients(T, X, gamma)` | Positive γ; converted to natural log | predicted − observed ln γ |
| `add_excess_enthalpy(T, X, H_E_J_mol)` | Molar J/mol | (predicted − observed) Hᴱ/(RT) |
| `add_bubble_pressure(T, X, P_Pa, psat_Pa)` | Positive measured P and supplied pure saturation pressures | ln(P predicted/P observed) |
| `add_vle(T, X, Y, P_Pa, psat_Pa)` | Full liquid/vapour compositions, ideal vapour, no Poynting correction | ln γ − ln[yP/(x Pˢᵃᵗ)] |
| `add_lle(T, X_alpha, X_beta)` | Measured distinct liquid tie lines | ln(xᵅγᵅ) − ln(xᵝγᵝ) |

`psat_Pa` is an N-vector or M×N array in component order. The VLE helpers are
for conditions where ideal-vapour modified Raoult law is appropriate. They do
not infer saturation pressures or fugacity corrections.

Missing activity/enthalpy measurements can be NaN, and zero weights omit
entries. VLE conversion omits zero x/y entries; LLE compares components present
in both phases. A ternary fit may include binary-edge rows with a zero third
mole fraction and NaN for its unmeasured ln-gamma. Positive weights and target
arrays must broadcast to the dataset's residual shape. `weight` is a **relative
inverse-variance weight on the normalized residual scale above**; its square
root multiplies the residual. For example, convert a dimensional enthalpy
uncertainty to uncertainty in Hᴱ/(RT) before assigning its inverse variance.
Weights are not automatically estimated from the data.

## Identifiability and validation

At a single T, activity-only data constrain a+b/T, not a and b separately.
The helper rejects freeing both for the same directed pair unless there are
multiple temperatures or excess-enthalpy data. A narrow temperature interval,
limited composition range or fitting alpha can still create strong parameter
correlations. Start with fixed alpha, adequate composition coverage and held-out
temperatures/compositions. A numerical success flag alone is insufficient.

`result.rank`, `condition_number`, `jacobian`, `residuals` and
`standard_errors` make those checks accessible. Covariance is the local linear
least-squares estimate, scaled by residual variance, available only with full
rank, positive residual degrees of freedom and linear loss. Otherwise it is
NaN. Rank-deficient fits issue a warning. Bounds, data uncertainty and model
error can make local standard errors optimistic. SciPy robust `loss=` options
are supported; their covariance is deliberately not reported. The report labels
the initial quadratic cost and final optimized objective separately.

For your own diagnostics, `problem.residuals(theta)` and
`problem.jacobian(theta)` use the parameter order of the `vary` calls. Editing
the problem invalidates its compiled residual. Within an optimization, residual
and Jacobian evaluations at the same parameters share a cached JAX evaluation.

LLE equality residuals alone can also fit metastable or unstable tie lines.
After fitting, use [stability and phase flash](../capabilities.md) checks, verify
material balances and validate against independent data. NRTL does not supply
solid fusion data; an SLLE fit requires those separately. Fitting a parameter
set to another model is model reduction, not experimental validation.
