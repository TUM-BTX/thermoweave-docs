# NRTL and SPT-NRTL

NRTL—Non-Random Two-Liquid—is an excess-Gibbs model based on local composition.
A molecule's immediate environment need not have the same composition as the
bulk liquid when unlike interactions differ from like interactions. NRTL uses
directed pair parameters and a nonrandomness parameter to represent that
preference. The original model is due to
[Renon and Prausnitz (1968)](https://doi.org/10.1002/aic.690140124).

## Local-composition weights

Let $\tau_{ij}$ be a dimensionless directed interaction parameter. Define

$$G_{ij}=\exp(-\alpha_{ij}\tau_{ij}),\qquad
D_i=\sum_j x_jG_{ji},$$

$$q_i=\frac{\sum_j x_j\tau_{ji}G_{ji}}{D_i}.$$

NRTL's excess energy is then

$$\frac{g^E}{RT}=\sum_i x_i q_i.$$

The weighting changes the contribution of neighbours around a reference
component. The two directions $\tau_{ij}$ and $\tau_{ji}$ are independent;
interchanging them changes an asymmetric mixture's predicted behaviour.
Alpha is commonly fixed and symmetric for a pair, while ThermoWeave also
accepts explicit directed matrices.

## Activity coefficients

Differentiating the total excess energy gives the closed-form result

$$\ln\gamma_i=q_i+\sum_j\frac{x_jG_{ij}}{D_j}
(\tau_{ij}-q_j).$$

Because the energy and activities share this construction, they satisfy the
[fixed-T/P consistency relations](excess-gibbs.md). The same equations apply
to binary and multicomponent mixtures. Combining separately fitted binary
pairs into a ternary model is an assumption to validate against ternary data.

## Temperature functions and units

ThermoWeave supports

$$\tau_{ij}(T)=a_{ij}+b_{ij}/T+l_{ij}\ln(T/\mathrm K)+d_{ij}T,$$

$$\alpha_{ij}(T)=\alpha^0_{ij}+e_{ij}T.$$

| Term | Python coefficient | Units |
|---|---|---|
| a | `a` | dimensionless |
| b | `b` | K |
| l | `tau_log` | dimensionless |
| d | `tau_linear` | 1/K |
| α⁰ | `alpha` | dimensionless |
| e | `alpha_linear` | 1/K |

The added logarithmic/linear terms default to zero, giving the familiar a+b/T
form with constant alpha. The temperature derivatives of all terms—including
alpha(T)—contribute to excess enthalpy and heat capacity. A parameter set's
temperature function and units must be checked before importing values from
another program. Energy-valued interaction coefficients cannot be placed
directly in dimensionless a entries.

## Fitting and identifiability

At a single temperature, activity measurements constrain the effective
$\tau_{ij}(T)$, not a and b independently. Allowing further temperature terms
requires additional independent information. Multiple temperatures, broad
composition coverage and excess-enthalpy data can help distinguish their
effects; narrow ranges can still leave strongly correlated coefficients.

Start with a simple parameterization and inspect fitted Jacobian rank,
conditioning and held-out errors before adding terms. An improved training
fit alone does not establish reliable extrapolation. Tie-line equality also
needs a [stability check](phase-equilibria.md#liquidliquid-equilibrium-and-stability)
when parameters are intended for LLE or SLLE.

## What SPT-NRTL adds

[SPT-NRTL](https://doi.org/10.1016/j.fluid.2023.113731) predicts NRTL parameters
from molecular SMILES with a transformer. Its thermodynamic output is still an
NRTL function, so the energy/activity relations are preserved. The published
collection uses the full temperature functions above.

These are model-predicted parameters with a common method reference. The CSVs
do not provide individual experimental references or validated temperature
intervals for each pair. Global training-data coverage does not establish a
pair-specific validity range. A deterministic source-row choice in ThermoWeave
also keeps an assembled model invariant when the user reorders its components.

**Use in Python:** [NRTL setup and conventions](../models/nrtl.md),
[SPT collection access](../models/spt-nrtl.md),
[fitting guide](../advanced/nrtl-fitting.md),
[notebook 13](../notebooks/13_nrtl_and_parameter_fitting.ipynb) and
[notebook 14](../notebooks/14_spt_nrtl_parameters.ipynb).
