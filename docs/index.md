---
title: ThermoWeave
hide:
  - toc
---

<section class="tw-hero" markdown="1">
<div markdown="1">
<span class="tw-kicker">ThermoWeave documentation</span>
<h1>Thermodynamics,<span>from theory to calculation.</span></h1>
<p>Understand the models. Build a mixture. Calculate properties and phase equilibria with SAFT-γ Mie, NRTL, openCOSMO-RS and HANNA.</p>
<div class="tw-actions" markdown="1">

[Read the theory](theory.md){ .md-button .md-button--primary }
[Start calculating](guide/index.md){ .md-button }

</div>
</div>
<div class="tw-model-map">
<svg viewBox="0 0 400 278" role="img" aria-labelledby="model-map-title model-map-description">
<title id="model-map-title">Two model families, a common calculation interface</title>
<desc id="model-map-description">Equations of state and excess Gibbs energy models provide chemical potentials and activities for property and phase equilibrium calculations.</desc>
<defs><marker id="tw-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10Z" fill="var(--tw-accent)"/></marker></defs>
<text x="200" y="17" text-anchor="middle" class="map-label">FROM A MODEL TO AN EQUILIBRIUM</text>
<rect x="12" y="36" width="170" height="63" rx="9" class="map-node"/>
<rect x="218" y="36" width="170" height="63" rx="9" class="map-node"/>
<text x="97" y="61" text-anchor="middle" font-weight="600">Equation of state</text>
<text x="97" y="82" text-anchor="middle" class="map-label">SAFT-γ Mie</text>
<text x="303" y="61" text-anchor="middle" font-weight="600">Excess Gibbs energy</text>
<text x="303" y="82" text-anchor="middle" class="map-label">NRTL · COSMO-RS · HANNA</text>
<path d="M97 99v23q0 12 12 12h78M303 99v23q0 12-12 12h-78" class="map-line"/>
<path d="M200 134v15" class="map-line" marker-end="url(#tw-arrow)"/>
<rect x="91" y="155" width="218" height="43" rx="9" class="map-node"/>
<text x="200" y="181" text-anchor="middle" font-weight="600">Chemical potentials &amp; activities</text>
<path d="M200 198v22" class="map-line" marker-end="url(#tw-arrow)"/>
<rect x="36" y="227" width="328" height="41" rx="9" class="map-result"/>
<text x="200" y="253" text-anchor="middle" font-weight="600">VLE · LLE · SLE · SLLE</text>
</svg>
<p>Different physical descriptions, connected through a common thermodynamic interface.</p>
</div>
</section>

<div class="tw-section-heading">
<h2>Choose your starting point</h2>
<p>Understand an equation, or put a model to work.</p>
</div>

<div class="tw-routes" markdown="1">
<section class="tw-route" markdown="1">

<span class="tw-kicker">01 / Theory</span>

### How the models work

Physical assumptions, thermodynamic potentials and the equations that connect molecular interactions to phase behaviour.

- [Equations of state and SAFT](theory/equations-of-state.md)
- [Excess Gibbs energy and NRTL](theory/excess-gibbs.md)
- [Stability, coexistence and SLLE](theory/phase-equilibria.md)

</section>
<section class="tw-route" markdown="1">

<span class="tw-kicker">02 / Practical guide</span>

### Run a calculation

Install the library, define components and parameters, then calculate properties, fit a model or solve a phase equilibrium.

- [Install on Linux, macOS or Windows](installation.md)
- [Choose and set up a model](guide/index.md#choose-a-model)
- [Calculate properties and equilibria](guide/calculations.md)

</section>
</div>

<div class="tw-section-heading">
<h2>Learn by running the models</h2>
<p><a href="tutorials/">Explore the tutorial collection →</a></p>
</div>

<div class="tw-lesson-grid" markdown="1">
<section class="tw-lesson" markdown="1">

### [Binary & ternary SLLE](tutorials.md#solidliquidliquid-equilibrium)

Phase boundaries, liquid splitting and solid–liquid–liquid coexistence with actual SAFT and COSMO-RS models.

</section>
<section class="tw-lesson" markdown="1">

### [NRTL & parameter fitting](notebooks/13_nrtl_and_parameter_fitting.ipynb)

Activities, excess properties and VLE, followed by a fitted NRTL representation of SAFT predictions.

</section>
<section class="tw-lesson" markdown="1">

### [SPT-NRTL predictions](notebooks/14_spt_nrtl_parameters.ipynb)

Load published parameter predictions, inspect their provenance and work with the full temperature dependence.

</section>
</div>

## A first calculation

After [installation](installation.md), construct a water/ethanol model from SMILES.
The same object supplies liquid density, molar volume, pressure and activities.

```python title="first_calculation.py"
from thermoweave import SAFTgammaMie

model = SAFTgammaMie.from_smiles(
    {"water": "O", "ethanol": "CCO"}, pressure_Pa=101325.0
)
T, x = 298.15, [0.8, 0.2]
rho = model.density(T, x)                # mol/m³
volume = 1.0 / rho                      # m³/mol
pressure = model.pressure(T, x, rho)     # Pa
ln_gamma = model.ln_activity_coefficients(T, x)
print(rho, volume, pressure, ln_gamma)
```

The printed assignment report shows how atoms were mapped to SAFT groups.
Manual group definitions are also supported. Continue with the
[calculation guide](guide/calculations.md) or the
[quickstart notebook](notebooks/00_quickstart_and_units.ipynb).

## Access and reproducibility

The [ThermoWeave library repository](https://github.com/TUM-BTX/ThermoWeave)
is private; obtain access from the TUM-BTX maintainers before cloning it.
The [practical guide](guide/index.md) identifies the parameters, backend
installations and external inputs needed by each model.

The notebooks show saved calculations with their inputs and parameter sources.
COSMO conformer databases, neural-network weights and external engines are
obtained separately. See [capabilities and assumptions](capabilities.md) when
interpreting model predictions and numerical stability checks.
