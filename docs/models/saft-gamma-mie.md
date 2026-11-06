# SAFT-γ Mie

ThermoWeave implements SAFT-γ Mie as a native JAX Helmholtz equation of state.
It supplies pressure, density roots, fugacity coefficients, liquid activities
and derivatives. The bundled base parameter table comes from Haslam et al.
(2020); see the [scientific references](../references.md).

For the molecular potential, energy contributions and association equations,
read [SAFT-γ Mie theory](../theory/saft-gamma-mie.md).

## Standard model and research extensions

The default Helmholtz contributions are **monomer, chain and association**.
Wertheim TPT1 association is part of the standard formulation. Experimental
hydration-network and steric-hindrance corrections exist as explicit opt-in
extensions; the shipped tables leave them empty, so the standard tutorial
calculations do not activate them.

This is a native implementation with documented fixes and regression checks,
rather than an untouched distribution of another package. See the
[capabilities](../capabilities.md) for assumptions and validation limits.

## Define molecules automatically

```python
from thermoweave import SAFTgammaMie

model = SAFTgammaMie.from_smiles(
    {"water": "O", "ethanol": "CCO"}, pressure_Pa=101325.0
)
```

RDKit identifies supported functional groups. The report prints group counts,
labelled atoms, matching rules and parameter references. Inspect it before
using an assignment for a new chemical family. Unsupported or ambiguous
fragmentations fail explicitly.

## Define molecules manually

```python
model = SAFTgammaMie(
    {"water": {"H2O": 1}, "ethanol": {"CH3": 1, "CH2OH": 1}},
    pressure_Pa=101325.0,
)
```

Manual construction does not require RDKit. EOS evaluations still require JAX.
The `saft-smiles` extra installs both. Named parameter extensions are loaded
explicitly, for example `GroupDatabase.default("wehbe2023", "tenberg2025")`;
they add referenced groups rather than silently replacing base parameters.

## Calculate properties

```python
T, x = 298.15, [0.8, 0.2]
rho = model.density(T, x)                 # mol/m³, liquid branch
volume = 1.0 / rho                       # m³/mol
P = model.pressure(T, x, rho)            # Pa
ln_gamma = model.ln_activity_coefficients(T, x)
```

Use the [API guide](../api.md) for derivatives, fugacity and response functions.
The [binary and ternary SLLE tutorials](../tutorials.md#solidliquidliquid-equilibrium)
combine the same model with measured pure-solid fusion inputs.
