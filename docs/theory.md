# Theory

Understand what each model describes, how its thermodynamic potential is
constructed, and how that potential determines observable properties and
phase equilibria. The chapters develop the equations and their assumptions;
the [practical guide](guide/index.md) shows how to use them in Python.

## A reading path

| Chapter | Main question |
|---|---|
| [Thermodynamic foundations](theory/foundations.md) | What are chemical potentials, reference states and mixing energies? |
| [Equations of state](theory/equations-of-state.md) | How does a Helmholtz model give pressure, density and fugacity? |
| [SAFT-γ Mie](theory/saft-gamma-mie.md) | How do segments, chain connectivity and association build an EoS? |
| [Excess Gibbs energy models](theory/excess-gibbs.md) | How does gE determine activity coefficients and liquid nonideality? |
| [NRTL and SPT-NRTL](theory/nrtl.md) | What do local compositions and directed pair parameters mean? |
| [COSMO-RS and learned models](theory/cosmors-and-learned-models.md) | How do surface interactions or learned representations provide activities? |
| [Phase equilibria and SLLE](theory/phase-equilibria.md) | How do chemical-potential equality, stability and material balances fit together? |
| [Derivatives and consistency](theory/derivatives.md) | How are excess enthalpy, heat capacity and response functions obtained? |

## Chemical potentials and gE models

For the pure-liquid standard state,

$$\mu_i=\mu_i^{\mathrm{pure,L}}+RT\ln(x_i\gamma_i).$$

An excess-Gibbs model specifies the nonideal part of liquid mixing. An equation
of state describes a fluid's density dependence as well. Both can provide the
chemical potentials needed by phase-equilibrium algorithms, but their inputs,
physical assumptions and available properties differ. Start with
[foundations](theory/foundations.md) and [gE models](theory/excess-gibbs.md).

## SAFT-γ Mie: a Helmholtz equation of state

SAFT builds a residual Helmholtz energy from segment interactions, chain
formation and association. The [SAFT chapter](theory/saft-gamma-mie.md) explains
the Mie potential, functional groups and association-site equations.

## Properties from Helmholtz derivatives

Pressure, fugacity and residual enthalpy follow from derivatives of the same
energy. Learn the [EoS relations](theory/equations-of-state.md), then the
[derivative and consistency checks](theory/derivatives.md).

## Phase and reaction equilibrium

Equal chemical potentials identify coexistence candidates. Global stability
and material balances decide which phase assemblage can represent the feed.
The [phase-equilibrium chapter](theory/phase-equilibria.md) connects VLE, LLE,
SLE and coupled liquid/solid flashes. Reactive/electrolyte workflows have
additional reference-state and conservation requirements; see
[capabilities](capabilities.md) and the labelled analytic exercises.

## Binary versus ternary SLLE

A binary solid–liquid–liquid invariant occurs at a particular temperature at
fixed pressure. A ternary system can occupy a three-phase tie triangle at
fixed T/P. The [SLLE explanation](theory/phase-equilibria.md#binary-and-ternary-slle)
connects the phase rule to the phase compositions and amounts returned by
[tutorials 10–12](tutorials.md#solidliquidliquid-equilibrium).
