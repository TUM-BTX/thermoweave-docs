# Neutral Parametrization

ThermoWeave fits continuous neutral OpenCOSMO-RS parameters against the bulk
corpus evaluators. Every candidate is an in-memory `Parametrization`; no JSON
file is rewritten during optimization. The C++ legacy engine loads the required
molecules afresh for each distinct candidate. This is slower than reusing stale
profiles, but correct for preprocessing parameters such as `Rav` and
`Rav_corr`.

```python
from thermoweave import (
    CorpusObjective, FitParameter, Log, LossConfig, OptimizationConfig,
    ParameterSpace, fit_parameters, load_parametrization,
)

base = load_parametrization("default_orca")
space = ParameterSpace([
    FitParameter("Aeff", "parameters.Aeff", 4.0, 8.0),
    # Bounds are physical; the C++ backend stores this as ln_alpha.
    FitParameter("alpha", "parameters.ln_alpha", 0.2, 5.0, Log()),
])

objective = CorpusObjective(
    corpus_paths,
    component_database,
    base,
    space,
    loss_config=LossConfig(
        weights={"IDAC": 1.0, "AC": 1.0, "logK": 1.0,
                 "LLE_NIST": 1.0, "LLE_DECHEMA": 1.0,
                 "dGsolvation": 1.0},
        scales={"IDAC": 1.0, "AC": 1.0, "logK": 1.0,
                "LLE_NIST": 1.0, "LLE_DECHEMA": 1.0,
                "dGsolvation": 1.0},
    ),
)

result = fit_parameters(
    objective,
    config=OptimizationConfig(method="Nelder-Mead", maxiter=200),
)
result.to_json("fit-result.json")
optimized = result.optimized_parametrization
optimized.to_json("optimized-parametrization.json")
```

The optimized parametrization file can be loaded again with the same
`load_parametrization("optimized-parametrization.json")` function. This
ThermoWeave v1 format stores the already-adapted C++ options/parameters exactly;
Backend JSON inputs continue to be delegated to the validated C++ loader.

Available serial methods are bounded `Nelder-Mead`, `L-BFGS-B`, and seeded
`differential_evolution`. The objective is the sum of weighted, scaled
per-property MSEs: IDAC/AC in `ln(gamma)`, partition/LLE data in `log10(K)`, and
dGsolvation in kcal/mol. Candidate scorer errors, non-finite predictions, or
changed scored-entry counts receive the configured failure value and cannot
improve a fit by dropping difficult records.

Canonical selectors include `Aeff`, `alpha`, `CHB`, `CHBT`, `sigma_HB`, `Rav`,
`Rav_corr`, `f_corr`, `m_vdW`, `E_F_corr`, numeric combinatorial fields, and
dGsolv calibration parameters. `tau_Z(Z, lower, upper)` defines an atomic
dGsolv tau parameter. Use explicit scientifically meaningful bounds.

Discrete switches, ion parameters, ME-PDH, reactions, VLE fitting, and parallel
candidate evaluation are intentionally excluded from this first neutral fitter.
