# SAFT-γ Mie

SAFT—Statistical Associating Fluid Theory—constructs a fluid Helmholtz energy
from a molecular representation of interacting segments. SAFT-γ Mie makes that
representation group based: reusable functional groups describe molecules and
their unlike interactions. The original formulation is given by
[Papaioannou et al. (2014)](https://doi.org/10.1063/1.4851455), with the Mie
perturbation treatment developed by
[Lafitte et al. (2013)](https://doi.org/10.1063/1.4819786).

## Molecular representation

A molecule is specified by counts of functional groups, such as two CH₃ and
four CH₂ groups for n-hexane. Each group supplies segment size, interaction
energy, potential exponents and, where applicable, association sites. Segment
multiplicity and shape information enter the molecular averages.

This representation makes parameter transfer between molecules possible.
Transferability still depends on the fitted parameter set and chemical
coverage. Different molecular structures can have the same group counts;
group recognition does not guarantee discrimination between positional isomers.

The parameter tables express sigma in Å and epsilon/kB in K. The assembled EoS
and its property API use SI. Unlike dispersion or association parameters can
be independently fitted; combining rules are modelling assumptions where
explicit interactions are unavailable. The [parameter references](../references.md)
identify the source collections used by ThermoWeave.

## The Mie pair potential

For two segments separated by distance r,

$$u_{kl}(r)=C_{kl}\epsilon_{kl}
\left[\left(\frac{\sigma_{kl}}{r}\right)^{\lambda^r_{kl}}
-\left(\frac{\sigma_{kl}}{r}\right)^{\lambda^a_{kl}}\right],$$

$$C_{kl}=\frac{\lambda^r_{kl}}{\lambda^r_{kl}-\lambda^a_{kl}}
\left(\frac{\lambda^r_{kl}}{\lambda^a_{kl}}\right)^{{\lambda^a_{kl}}/
(\lambda^r_{kl}-\lambda^a_{kl})}.$$

Sigma sets the zero-crossing distance, epsilon the well depth, and the
repulsive/attractive exponents set the shape and range of the interaction.
The normalization C makes the minimum equal to −epsilon. Variable exponents
provide more flexibility than fixing one potential shape for every group.

## Energy contributions

The reduced residual Helmholtz energy is

$$a^{\mathrm{res}}=a^{\mathrm{monomer}}+
 a^{\mathrm{chain}}+a^{\mathrm{association}}.$$

The monomer term describes the reference fluid of unconnected segments. It
uses a hard-sphere reference and a perturbation expansion through third order
for attractive Mie interactions. Schematically, with $\beta=1/(k_BT)$,

$$a^{\mathrm{monomer}}=\bar m
\left[a^{\mathrm{hs}}+\beta a_1+\beta^2a_2+\beta^3a_3\right].$$

The perturbation coefficients depend on density, composition and group
interactions. The chain term accounts for connecting segments into molecules;
its contact-correlation structure has the form

$$a^{\mathrm{chain}}=-\sum_i x_i(m_i-1)\ln g^{\mathrm{Mie}}_{ii}.$$

The effective segment count and molecular Mie contact quantities are assembled
from each molecule's group representation. Exact mixing and contact functions
are part of the cited formulation, rather than independent fitted corrections
to pressure.

## Association sites and mass action

Directional bonding, such as hydrogen bonding, is represented by association
sites. Let $X_{iA}$ denote the fraction of sites of type A on component i that
remain unbonded. A standard first-order Wertheim site treatment gives

$$X_{iA}=\left[1+\rho_N\sum_j x_j\sum_B n_{jB}
 X_{jB}\Delta_{iA,jB}\right]^{-1},$$

$$a^{\mathrm{association}}=\sum_i x_i\sum_A n_{iA}
\left(\ln X_{iA}-\frac{X_{iA}}{2}+\frac12\right).$$

Here $\rho_N$ is number density and $n_{iA}$ is a site's multiplicity per
molecule. Delta combines bonding volume, association energy and the reference
fluid's contact structure. Its dimensions match the number-density convention.
The equations are coupled because a bond consumes sites on both partners.

These standard association equations are part of baseline SAFT. Additional
network or steric model options change its assumptions and should be recorded
with a calculation. See [Wertheim's original theory](https://doi.org/10.1007/BF01017362)
and the [model setup guide](../models/saft-gamma-mie.md).

## From molecular energy to a calculation

Pressure and fugacity follow by differentiating this one residual Helmholtz
function. Density and site fractions are implicit solutions; their dependence
on temperature, composition and parameters must be included in derivatives.
A group assignment only constructs the molecular input—it does not establish
which phase is stable or validate the chosen parameters.

**Use in Python:** [automatic/manual group assignment](../models/saft-gamma-mie.md),
[notebook 02](../notebooks/02_saft_molecules_and_groups.ipynb),
[EoS properties](../notebooks/03_saft_eos_properties.ipynb) and
[binary/ternary SLLE](../tutorials.md#solidliquidliquid-equilibrium).
