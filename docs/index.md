# ThermoWeave

**Thermodynamic models and phase-equilibrium calculations in Python.**

ThermoWeave provides a native SAFT-γ Mie equation of state, a JAX NRTL activity model, adapters for
openCOSMO-RS and HANNA, and a common interface for activities, stability,
solubility and multiphase equilibrium calculations.

<div class="grid cards" markdown>

- **Install on your computer**

    Set up a named Conda environment and select the right instructions for
    Linux, Windows or macOS.

    [Start the installation](installation.md)

- **Calculate binary and ternary SLLE**

    Follow actual SAFT and COSMO-RS calculations, including phase compositions,
    phase amounts, binary boundaries and ternary tie triangles.

    [Choose a tutorial](tutorials.md#solidliquidliquid-equilibrium)

- **Understand the models**

    Learn which properties each model supplies, how molecules are defined and
    which parameters and external data are required.

    [NRTL](models/nrtl.md) · [SAFT-γ Mie](models/saft-gamma-mie.md) · [openCOSMO-RS](models/opencosmors.md)

- **Look up an API or equation**

    Check units, reference states, thermodynamic relations and calculation
    assumptions before interpreting a result.

    [API guide](api.md) · [Theory](theory.md) · [References](references.md)

</div>

## A first calculation

After [installation](installation.md), construct a water/ethanol model from SMILES:

```python
from thermoweave import SAFTgammaMie

model = SAFTgammaMie.from_smiles(
    {"water": "O", "ethanol": "CCO"}, pressure_Pa=101325.0
)
T, x = 298.15, [0.8, 0.2]
rho = model.density(T, x)                 # mol/m³
volume = 1.0 / rho                       # m³/mol
pressure = model.pressure(T, x, rho)     # Pa
ln_gamma = model.ln_activity_coefficients(T, x)
print(rho, volume, pressure, ln_gamma)
```

The group assignment prints its matching rules and atom labels for inspection.
Manual group counts remain available. The bundled SAFT data require no external
COSMO database.

## Access and reproducibility

The [ThermoWeave library repository](https://github.com/TUM-BTX/ThermoWeave)
is private; ask the TUM-BTX maintainers for access before cloning it. The
openCOSMO-RS backend has a separate installation and access requirement.
Read the [platform guide](installation.md#choose-your-platform) before installing
optional compiled software.

The rendered notebooks show saved calculations with identified parameters and
inputs. Reproducing COSMO-RS results requires your own compatible conformer
files; the site does not distribute molecular databases, neural-network weights
or external engines. Model predictions are distinguished from experimental
validation in the [capabilities guide](capabilities.md).
